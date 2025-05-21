# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2025 becon GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
Implementation of all API routes for Isms Reports
"""
import logging
import re
from flask import abort

from cmdb.manager.extendable_options_manager import ExtendableOptionsManager
from cmdb.manager.isms_manager.risk_matrix_manager import RiskMatrixManager
from cmdb.manager.isms_manager.risk_assessment_manager import RiskAssessmentManager
from cmdb.manager.isms_manager.control_measure_manager import ControlMeasureManager
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager.query_builder.builder_parameters import BuilderParameters

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsReportBuilder
from cmdb.models.extendable_option_model import OptionType

from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import DefaultResponse

from cmdb.errors.manager.risk_assessment_manager import RiskAssessmentManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

isms_report_blueprint = APIBlueprint('isms_report', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@isms_report_blueprint.route('/risk_matrix', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@isms_report_blueprint.protect(auth=True, right='base.isms.report.view')
def get_isms_risk_matrix_report(request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve the IsmsRiskMatrix report

    Args:
        request_user (CmdbUser): CmdbUser requesting the RiskMatrix report

    Returns:
        DefaultResponse: The RiskMatrix report as a dictionary
    """
    try:
        risk_assessment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.RISK_ASSESSMENT,
                                                                            request_user)
        risk_matrix_manager: RiskMatrixManager = ManagerProvider.get_manager(
                                                                    ManagerType.RISK_MATRIX,
                                                                    request_user)
        extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(
                                                                                ManagerType.EXTENDABLE_OPTIONS,
                                                                                request_user)

        isms_report_builder = IsmsReportBuilder(
            risk_assessment_manager,
            risk_matrix_manager,
            extendable_options_manager
        )

        risk_matrix_report = isms_report_builder.build_risk_matrix_report()

        return DefaultResponse(risk_matrix_report).make_response()
    except Exception as err:
        LOGGER.error("[get_isms_risk_matrix_report] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving the RiskMatrix report!")


@isms_report_blueprint.route('/risk_treatment_plan', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@isms_report_blueprint.protect(auth=True, right='base.isms.report.view')
def get_isms_risk_treatment_plan_report(request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve the Risk Treatment Plan report

    Args:
        request_user (CmdbUser): CmdbUser requesting the Risk Treatment Plan report

    Returns:
        DefaultResponse: The Risk Treatment Plan report as a dictionary
    """
    try:
        risk_assessment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.RISK_ASSESSMENT,
                                                                            request_user)

        query_pipeline = [
            # Step 0: Get all IsmsRiskAssessments
            {
                "$match": {}
            },
            # Step 1: Lookup associated Risk
            {
                "$lookup": {
                    "from": "isms.risk",
                    "localField": "risk_id",
                    "foreignField": "public_id",
                    "as": "risk"
                }
            },
            {"$unwind": {"path": "$risk", "preserveNullAndEmptyArrays": True}},

            # Step 2: Lookup implementation status (ExtendableOption)
            {
                "$lookup": {
                    "from": "framework.extendableOptions",
                    "localField": "implementation_status",
                    "foreignField": "public_id",
                    "as": "implementation_status"
                }
            },
            {"$unwind": {"path": "$implementation_status", "preserveNullAndEmptyArrays": True}},

            # Step 3: Lookup risk treatment option (ExtendableOption)
            {
                "$lookup": {
                    "from": "framework.extendableOptions",
                    "localField": "treatment_option_id",
                    "foreignField": "public_id",
                    "as": "treatment_option"
                }
            },
            {"$unwind": {"path": "$treatment_option", "preserveNullAndEmptyArrays": True}},

            # Step 4: Lookup Object or ObjectGroup based on object_id_ref_type
            {
                "$lookup": {
                    "from": "framework.objects",
                    "localField": "object_id",
                    "foreignField": "public_id",
                    "as": "object"
                }
            },
            {
                "$lookup": {
                    "from": "framework.objectGroups",
                    "localField": "object_id",
                    "foreignField": "public_id",
                    "as": "object_group"
                }
            },

            # Step 5: Lookup type label if object is used
            {
                "$lookup": {
                    "from": "framework.types",
                    "localField": "object.type_id",
                    "foreignField": "public_id",
                    "as": "object_type"
                }
            },

            # Step 6: Lookup person/personGroup
            {
                "$lookup": {
                    "from": "management.person",
                    "localField": "responsible_for_implementation_id",
                    "foreignField": "public_id",
                    "as": "responsible_person"
                }
            },
            {
                "$lookup": {
                    "from": "management.personGroup",
                    "localField": "responsible_for_implementation_id",
                    "foreignField": "public_id",
                    "as": "responsible_person_group"
                }
            },

            # Step 7: Lookup risk class matrix values
            {
                "$lookup": {
                    "from": "isms.riskMatrix",
                    "let": {
                        "likelihood_id": "$likelihood_id",
                        "impact_id": "$maximum_impact_id"
                    },
                    "pipeline": [
                        {"$match": {"public_id": 1}},
                        {"$unwind": "$risk_matrix"},
                        {"$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$risk_matrix.likelihood_id", "$$likelihood_id"]},
                                    {"$eq": ["$risk_matrix.impact_id", "$$impact_id"]}
                                ]
                            }
                        }},
                        {"$replaceRoot": {"newRoot": "$risk_matrix"}}
                    ],
                    "as": "risk_before"
                }
            },
            {"$unwind": {"path": "$risk_before", "preserveNullAndEmptyArrays": True}},

            {
                "$lookup": {
                    "from": "isms.riskClass",
                    "localField": "risk_before.risk_class_id",
                    "foreignField": "public_id",
                    "as": "risk_before_class"
                }
            },
            {"$unwind": {"path": "$risk_before_class", "preserveNullAndEmptyArrays": True}},

            # Step 8: Repeat for risk after treatment
            {
                "$lookup": {
                    "from": "isms.riskMatrix",
                    "let": {
                        "likelihood_id": "$post_likelihood_id",
                        "impact_id": "$post_impact_id"
                    },
                    "pipeline": [
                        {"$match": {"public_id": 1}},
                        {"$unwind": "$risk_matrix"},
                        {"$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$risk_matrix.likelihood_id", "$$likelihood_id"]},
                                    {"$eq": ["$risk_matrix.impact_id", "$$impact_id"]}
                                ]
                            }
                        }},
                        {"$replaceRoot": {"newRoot": "$risk_matrix"}}
                    ],
                    "as": "risk_after"
                }
            },
            {"$unwind": {"path": "$risk_after", "preserveNullAndEmptyArrays": True}},

            {
                "$lookup": {
                    "from": "isms.riskClass",
                    "localField": "risk_after.risk_class_id",
                    "foreignField": "public_id",
                    "as": "risk_after_class"
                }
            },
            {"$unwind": {"path": "$risk_after_class", "preserveNullAndEmptyArrays": True}},

            # Step 9: Lookup assigned control measures
            {
                "$lookup": {
                    "from": "isms.controlMeasureAssignment",
                    "localField": "public_id",
                    "foreignField": "risk_assessment_id",
                    "as": "control_assignments"
                }
            },
            {
                "$lookup": {
                    "from": "isms.controlMeasure",
                    "localField": "control_assignments.control_measure_id",
                    "foreignField": "public_id",
                    "as": "control_measures"
                }
            },

            # Step 10: Project final fields
            {
                "$project": {
                    "_id": 0,
                    "risk_name": "$risk.name",
                    "risk_identifier": "$risk.identifier",
                    "risk_category": "$risk.category_id",  # Optional: Join with ExtendableOption for name
                    "protection_goals": "$risk.protection_goals",  # Could join for names

                    "object": {
                        "$cond": [
                            {"$eq": ["$object_id_ref_type", "OBJECT_GROUP"]},
                            {"$arrayElemAt": ["$object_group.name", 0]},
                            {"$arrayElemAt": ["$object.public_id", 0]}
                        ]
                    },
                    "object_type": {
                        "$cond": [
                            {"$eq": ["$object_id_ref_type", "OBJECT_GROUP"]},
                            "Object group",
                            {"$arrayElemAt": ["$object_type.label", 0]}
                        ]
                    },

                    "risk_before": {
                        "value": "$risk_before.calculated_value",
                        "color": "$risk_before_class.color"
                    },
                    "risk_after": {
                        "value": "$risk_after.calculated_value",
                        "color": "$risk_after_class.color"
                    },

                    "risk_treatment_option": "$treatment_option.value",
                    "implementation_status": "$implementation_status.value",
                    "planned_implementation_date": 1,

                    "responsible_person": {
                        "$cond": [
                            {"$eq": ["$responsible_for_implementation_id_ref_type", "PERSON"]},
                            {"$arrayElemAt": ["$responsible_person.display_name", 0]},
                            {"$arrayElemAt": ["$responsible_person_group.name", 0]}
                        ]
                    },

                    "control_measures": "$control_measures.title"
                }
            }
        ]

        results = risk_assessment_manager.iterate_items(BuilderParameters(query_pipeline))

        # TODO: Replace Object public_id with Summary line

        return DefaultResponse(results).make_response()
    except RiskAssessmentManagerIterationError as err:
        LOGGER.error(
            "[get_isms_risk_treatment_plan_report] RiskAssessmentManagerIterationError: %s. Type: %s", err, type(err)
        )
        abort(500, "Failed to iterate components for Risk Treatment Plan report!")
    except Exception as err:
        LOGGER.error("[get_isms_risk_treatment_plan_report] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving the Risk Treatment Plan report!")


@isms_report_blueprint.route('/soa', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@isms_report_blueprint.protect(auth=True, right='base.isms.report.view')
def get_isms_soa_report(request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve the Statement of Applicability(SOA) report

    Args:
        request_user (CmdbUser): CmdbUser requesting the SOA report

    Returns:
        DefaultResponse: The SOA report as a dictionary
    """
    try:
        control_measure_manager: ControlMeasureManager = ManagerProvider.get_manager(
                                                                            ManagerType.CONTROL_MEASURE,
                                                                            request_user)
        extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(
                                                                                ManagerType.EXTENDABLE_OPTIONS,
                                                                                request_user)

        # Get all implementation states for IsmsControlMeasures
        all_implementation_states = extendable_options_manager.get_many(
                                                                filter={'option_type':OptionType.IMPLEMENTATION_STATE}
                                                               )

        # Create a lookup map from public_id to value for implementation states
        implementation_state_lookup = {
            option['public_id']: option['value'] for option in all_implementation_states
        }

        all_control_meassures = control_measure_manager.get_many()

        # Replace implementation_state public_id with its corresponding value
        for cm in all_control_meassures:
            original_id = cm.get('implementation_state')
            if original_id in implementation_state_lookup:
                cm['implementation_state'] = implementation_state_lookup[original_id]

        all_sources = extendable_options_manager.get_many(
                                                    filter={'option_type':OptionType.CONTROL_MEASURE}
                                                 )

        # Create a lookup map from public_id to value for sources
        source_lookup = {
            option['public_id']: option['value'] for option in all_sources
        }

        # Replace source public_id with its corresponding value
        for cm in all_control_meassures:
            source_id = cm.get('source')
            if source_id in source_lookup:
                cm['source'] = source_lookup[source_id]

        # Order all control measures
        all_control_meassures.sort(key=sort_key)

        return DefaultResponse(all_control_meassures).make_response()
    except Exception as err:
        LOGGER.error("[get_isms_soa_report] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving the SOA report!")


@isms_report_blueprint.route('/risk_assessments', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@isms_report_blueprint.protect(auth=True, right='base.isms.report.view')
def get_isms_risk_assessments_report(request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve the Statement of Applicability(SOA) report

    Args:
        request_user (CmdbUser): CmdbUser requesting the SOA report

    Returns:
        DefaultResponse: The SOA report as a dictionary
    """
    try:
        risk_assessment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.RISK_ASSESSMENT,
                                                                            request_user)

        pipeline = [

            # 1. Lookup risk info
            {
                '$lookup': {
                    'from': 'isms.risk',
                    'localField': 'risk_id',
                    'foreignField': 'public_id',
                    'as': 'risk'
                }
            },
            {'$unwind': '$risk'},

            # 2. Lookup risk category option
            {
                '$lookup': {
                    'from': 'framework.extendableOptions',
                    'let': {'cat_id': '$risk.category_id'},
                    'pipeline': [
                        {'$match': {'$expr': {'$and': [
                            {'$eq': ['$public_id', '$$cat_id']},
                            {'$eq': ['$optiontype', 'RISK']}
                        ]}}}
                    ],
                    'as': 'risk_category'
                }
            },
            {'$unwind': {'path': '$risk_category', 'preserveNullAndEmptyArrays': True}},

            # 3. Lookup protection goals
            {
                '$lookup': {
                    'from': 'isms.protectionGoal',
                    'localField': 'risk.protection_goals',
                    'foreignField': 'public_id',
                    'as': 'protection_goals'
                }
            },

            # 4. Lookup implementation status
            {
                '$lookup': {
                    'from': 'framework.extendableOptions',
                    'let': {'impl_id': '$implementation_status'},
                    'pipeline': [
                        {'$match': {'$expr': {'$and': [
                            {'$eq': ['$public_id', '$$impl_id']},
                            {'$eq': ['$optiontype', 'IMPLEMENTATION_STATE']}
                        ]}}}
                    ],
                    'as': 'implementation_status_option'
                }
            },
            {'$unwind': {'path': '$implementation_status_option', 'preserveNullAndEmptyArrays': True}},

            # 5. Lookup impact categories (sorted)
            {
                '$lookup': {
                    'from': 'isms.impactCategory',
                    'pipeline': [{'$sort': {'sort': 1}}],
                    'as': 'impact_categories'
                }
            },

            # 6. Lookup all impacts (for name and calculation_basis)
            {
                '$lookup': {
                    'from': 'isms.impact',
                    'as': 'all_impacts',
                    'pipeline': []
                }
            },

            # 7. Lookup all likelihoods
            {
                '$lookup': {
                    'from': 'isms.likelihood',
                    'as': 'all_likelihoods',
                    'pipeline': []
                }
            },

            # 8. Persons & groups lookups (risk assessor, risk owner, interviewed, responsible, auditor)
            # Risk assessor person
            {
                '$lookup': {
                    'from': 'management.person',
                    'localField': 'risk_assessor_id',
                    'foreignField': 'public_id',
                    'as': 'risk_assessor_person'
                }
            },
            {'$unwind': {'path': '$risk_assessor_person', 'preserveNullAndEmptyArrays': True}},

            # Risk owner (person or group)
            {
                '$facet': {
                    'risk_owner_person': [
                        {'$match': {'risk_owner_id_ref_type': 'person'}},
                        {
                            '$lookup': {
                                'from': 'management.person',
                                'localField': 'risk_owner_id',
                                'foreignField': 'public_id',
                                'as': 'risk_owner_person'
                            }
                        },
                        {'$unwind': {'path': '$risk_owner_person', 'preserveNullAndEmptyArrays': True}},
                    ],
                    'risk_owner_group': [
                        {'$match': {'risk_owner_id_ref_type': 'group'}},
                        {
                            '$lookup': {
                                'from': 'management.personGroup',
                                'localField': 'risk_owner_id',
                                'foreignField': 'public_id',
                                'as': 'risk_owner_group'
                            }
                        },
                        {'$unwind': {'path': '$risk_owner_group', 'preserveNullAndEmptyArrays': True}},
                    ],
                    'rest': [
                        {'$match': {}}
                    ]
                }
            },
            # After facet, merge risk_owner_person or risk_owner_group into unified field later in code or client

            # Interviewed persons lookup
            {
                '$lookup': {
                    'from': 'management.person',
                    'localField': 'interviewed_persons',
                    'foreignField': 'public_id',
                    'as': 'interviewed_persons_data'
                }
            },

            # Responsible persons (person or group)
            {
                '$facet': {
                    'responsible_persons_person': [
                        {'$match': {'responsible_persons_id_ref_type': 'person'}},
                        {
                            '$lookup': {
                                'from': 'management.person',
                                'localField': 'responsible_persons_id',
                                'foreignField': 'public_id',
                                'as': 'responsible_persons_person'
                            }
                        },
                        {'$unwind': {'path': '$responsible_persons_person', 'preserveNullAndEmptyArrays': True}},
                    ],
                    'responsible_persons_group': [
                        {'$match': {'responsible_persons_id_ref_type': 'group'}},
                        {
                            '$lookup': {
                                'from': 'management.personGroup',
                                'localField': 'responsible_persons_id',
                                'foreignField': 'public_id',
                                'as': 'responsible_persons_group'
                            }
                        },
                        {'$unwind': {'path': '$responsible_persons_group', 'preserveNullAndEmptyArrays': True}},
                    ],
                    'rest': [
                        {'$match': {}}
                    ]
                }
            },

            # Auditor person or group
            {
                '$facet': {
                    'auditor_person': [
                        {'$match': {'auditor_id_ref_type': 'person'}},
                        {
                            '$lookup': {
                                'from': 'management.person',
                                'localField': 'auditor_id',
                                'foreignField': 'public_id',
                                'as': 'auditor_person'
                            }
                        },
                        {'$unwind': {'path': '$auditor_person', 'preserveNullAndEmptyArrays': True}},
                    ],
                    'auditor_group': [
                        {'$match': {'auditor_id_ref_type': 'group'}},
                        {
                            '$lookup': {
                                'from': 'management.personGroup',
                                'localField': 'auditor_id',
                                'foreignField': 'public_id',
                                'as': 'auditor_group'
                            }
                        },
                        {'$unwind': {'path': '$auditor_group', 'preserveNullAndEmptyArrays': True}},
                    ],
                    'rest': [
                        {'$match': {}}
                    ]
                }
            },

            # 9. Lookup assigned object and type label
            {
                '$lookup': {
                    'from': 'framework.objects',
                    'localField': 'object_id',
                    'foreignField': 'public_id',
                    'as': 'assigned_object'
                }
            },
            {'$unwind': {'path': '$assigned_object', 'preserveNullAndEmptyArrays': True}},
            {
                '$lookup': {
                    'from': 'framework.types',
                    'localField': 'assigned_object.type_id',
                    'foreignField': 'public_id',
                    'as': 'assigned_object_type'
                }
            },
            {'$unwind': {'path': '$assigned_object_type', 'preserveNullAndEmptyArrays': True}},

            # 10. Map priority int to string
            {
                '$addFields': {
                    'priority_str': {
                        '$switch': {
                            'branches': [
                                {'case': {'$eq': ['$priority', 1]}, 'then': 'Low'},
                                {'case': {'$eq': ['$priority', 2]}, 'then': 'Medium'},
                                {'case': {'$eq': ['$priority', 3]}, 'then': 'High'},
                                {'case': {'$eq': ['$priority', 4]}, 'then': 'Very High'},
                            ],
                            'default': 'Unknown'
                        }
                    }
                }
            },

            # 11. Process risk_calculation_before impacts: map impact_ids to names and set 'Unrated' if null
            {
                '$addFields': {
                    'risk_calculation_before.impacts': {
                        '$map': {
                            'input': '$risk_calculation_before.impacts',
                            'as': 'impact_item',
                            'in': {
                                'impact_category_id': '$$impact_item.impact_category_id',
                                'impact_category_name': {
                                    '$arrayElemAt': [
                                        {
                                            '$filter': {
                                                'input': '$impact_categories',
                                                'cond': {
                                                    '$eq': [
                                                        '$$this.public_id',
                                                        '$$impact_item.impact_category_id'
                                                    ]
                                                }
                                            }
                                        }, 0, {}
                                    ]
                                }.get('name', 'Unknown'),
                                'impact_name': {
                                    '$let': {
                                        'vars': {
                                            'imp': {
                                                '$arrayElemAt': [
                                                    {
                                                        '$filter': {
                                                            'input': '$all_impacts',
                                                            'cond': {
                                                                '$eq': [
                                                                    '$$this.public_id',
                                                                    '$$impact_item.impact_id'
                                                                ]
                                                            }
                                                        }
                                                    }, 0
                                                ]
                                            }
                                        },
                                        'in': {
                                            '$cond': [
                                                {'$ifNull': ['$$imp', False]},
                                                '$$imp.name',
                                                'Unrated'
                                            ]
                                        }
                                    }
                                }
                            }
                        }
                    },
                    # Similar mapping for likelihood name before
                    'risk_calculation_before.likelihood_name': {
                        '$let': {
                            'vars': {
                                'likelihood_obj': {
                                    '$arrayElemAt': [
                                        {
                                            '$filter': {
                                                'input': '$all_likelihoods',
                                                'cond': {
                                                    '$eq': [
                                                        '$$this.public_id',
                                                        '$risk_calculation_before.likelihood_id'
                                                    ]
                                                }
                                            }
                                        }, 0
                                    ]
                                }
                            },
                            'in': {
                                '$cond': [
                                    {'$ifNull': ['$$likelihood_obj', False]},
                                    '$$likelihood_obj.name',
                                    'Unrated'
                                ]
                            }
                        }
                    },

                    # Similarly for risk_calculation_after impacts
                    'risk_calculation_after.impacts': {
                        '$map': {
                            'input': '$risk_calculation_after.impacts',
                            'as': 'impact_item',
                            'in': {
                                'impact_category_id': '$$impact_item.impact_category_id',
                                'impact_category_name': {
                                    '$arrayElemAt': [
                                        {
                                            '$filter': {
                                                'input': '$impact_categories',
                                                'cond': {
                                                    '$eq': [
                                                        '$$this.public_id',
                                                        '$$impact_item.impact_category_id'
                                                    ]
                                                }
                                            }
                                        }, 0, {}
                                    ]
                                }.get('name', 'Unknown'),
                                'impact_name': {
                                    '$let': {
                                        'vars': {
                                            'imp': {
                                                '$arrayElemAt': [
                                                    {
                                                        '$filter': {
                                                            'input': '$all_impacts',
                                                            'cond': {
                                                                '$eq': [
                                                                    '$$this.public_id',
                                                                    '$$impact_item.impact_id'
                                                                ]
                                                            }
                                                        }
                                                    }, 0
                                                ]
                                            }
                                        },
                                        'in': {
                                            '$cond': [
                                                {'$ifNull': ['$$imp', False]},
                                                '$$imp.name',
                                                'Unrated'
                                            ]
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'risk_calculation_after.likelihood_name': {
                        '$let': {
                            'vars': {
                                'likelihood_obj': {
                                    '$arrayElemAt': [
                                        {
                                            '$filter': {
                                                'input': '$all_likelihoods',
                                                'cond': {
                                                    '$eq': [
                                                        '$$this.public_id',
                                                        '$risk_calculation_after.likelihood_id'
                                                    ]
                                                }
                                            }
                                        }, 0
                                    ]
                                }
                            },
                            'in': {
                                '$cond': [
                                    {'$ifNull': ['$$likelihood_obj', False]},
                                    '$$likelihood_obj.name',
                                    'Unrated'
                                ]
                            }
                        }
                    },
                }
            },

            # 12. Final project: select and rename all needed fields for the report
            {
                '$project': {
                    '_id': 0,

                    # Risk main info
                    'risk_title': '$risk.name',
                    'risk_category': '$risk_category.name',

                    # Protection goals as list of names
                    'protection_goals': {'$map': {
                        'input': '$protection_goals',
                        'as': 'pg',
                        'in': '$$pg.name'
                    }},

                    # Implementation status label
                    'implementation_status': '$implementation_status_option.name',

                    # Priority string
                    'priority': '$priority_str',

                    # Assigned object & type
                    'assigned_object': '$assigned_object.name',
                    'assigned_object_type': '$assigned_object_type.label',

                    # Risk assessor name
                    'risk_assessor': '$risk_assessor_person.name',

                    # Interviewed persons names
                    'interviewed_persons': {'$map': {
                        'input': '$interviewed_persons_data',
                        'as': 'person',
                        'in': '$$person.name'
                    }},

                    # Impact categories full list (optional)
                    'impact_categories': '$impact_categories',

                    # Risk calculations before and after (impacts + likelihood)
                    'risk_calculation_before': '$risk_calculation_before',
                    'risk_calculation_after': '$risk_calculation_after',

                    # Add other fields as needed...

                }
            }
        ]

        results = risk_assessment_manager.iterate_items(BuilderParameters(pipeline))

        # TODO: Replace Object public_id with Summary line

        return DefaultResponse(results).make_response()
    except Exception as err:
        LOGGER.error("[get_isms_soa_report] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving the RiskAssessment report!")

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

def sort_key(cm: dict) -> tuple:
    """
    Sort key function for Control Measures
    - First, prioritize sources where source = "ISO 27001:2022"
    - Then, sort by the identifier
    - If identifier is empty, place it last
    
    Args:
        cm (dict): Control Measure data containing 'source' and 'identifier'.

    Returns:
        tuple: A tuple that will be used for sorting:
            (priority_for_source, priority_for_empty_identifier, sorted_identifier)
    """
    # 1. Put ISO 27001:2022 first
    source_priority: int = 0 if cm.get('source') == 'ISO 27001:2022' else 1

    # 2. Identifiers that are empty or missing should come last
    identifier = cm.get('identifier')
    identifier_is_empty = not identifier or not identifier.strip()

    # This ensures that empty identifiers get a higher "penalty"
    empty_priority: int = 1 if identifier_is_empty else 0

    # 3. Convert the identifier into a list of integers for numeric sorting
    identifier_sort_value: list[int] = [int(part) if part.isdigit() else part
                                        for part in re.split(r'(\D+|\d+)', identifier or '')]

    return (source_priority, empty_priority, identifier_sort_value)

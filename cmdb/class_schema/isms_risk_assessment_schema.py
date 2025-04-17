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
The schema of an IsmsRiskAssessment
"""
# -------------------------------------------------------------------------------------------------------------------- #
# pylint: disable=R0801
def get_isms_risk_assessment_schema() -> dict:
    """
    Returns the IsmsRiskAssessment schema

    Returns:
        dict: Schema of the IsmsRiskAssessment
    """
    return {
        'public_id': {
            'type': 'integer',
            'min': 1,
        },
        'risk_id': { # public_id of referenced IsmsRisk
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'object_id_ref_type': { # ObjectReferenceType Enum
            'type': 'string',
            'required': True,
            'empty': False
        },
        'object_id': { # public_id of referenced CmdbObject or CmdbObjectGroup (dependening on 'object_reference_type')
            'type': 'integer',
            'min': 1,
            'required': True,
            'empty': False
        },
        ### Risk calculation before treatment ###
        'risk_calculation_before': {
            'type': 'dict',
            'required': True,
            'empty': False,
            'schema': {
                'impacts': { # All impact category sliders
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'impact_category_id': { # public_id of IsmsImpactCategory
                                'type': 'integer',
                            },
                            'impact_id':{ # public_id of IsmsImpact (empty = unrated)
                                'type': 'integer',
                            }
                        }
                    }
                },
                'likelihood_id': { # public_id of IsmsLikelihood (empty = unrated)
                    'type': 'integer',
                },
                'likelihood_value': { # calculation_basis of selected IsmsLikelihood
                    'type':'float',
                    'min': 0.0
                },
                'maximum_impact_id': { # public_id of the maximum IsmsImpact
                    'type': 'integer',
                },
                'maximum_impact_value': { # Maximum calculation_basis of the impact sliders
                    'type':'float',
                    'min': 0.0
                },
                'risk_level_value': { # The calculated risk value
                    'type':'float',
                    'min': 0.0
                }
            }
        },
        'risk_assessor_id': { # public_id of CmdbPerson
            'type': 'integer',
            'min': 1,
        },
        'risk_owner_id_ref_type': { # PersonReferenceType Enum
            'type': 'string',
        },
        'risk_owner_id': { # public_id of CmdbPerson or CmdbPersonGroup
            'type': 'integer',
            'min': 1,
        },
        'interviewed_persons': { # Multiselect of CmdbPersons
            'type': 'list',
            'nullable': True
        },
        'risk_assessment_date': { # Date of risk calculation before treatment
            'type': 'dict',
            'required': True,
            'empty': False
        },
        'additional_info': { # Additional information field value
            'type': 'string'
        },
        ### Risk treatment ###
        'risk_treatment_option': { # TreatmentOption Enum
            'type': 'string',
        },
        'responsible_persons_id_ref_type': { # PersonReferenceType Enum
            'type': 'string',
        },
        'responsible_persons_id': { # public_id of CmdbPerson or CmdbPersonGroup
            'type': 'integer',
            'min': 1,
        },
        'risk_treatment_description': { # Additional information text area field
            'type': 'string'
        },
        'planned_implementation_date': { # Date of planned implementation
            'type': 'dict',
            'nullable': True
        },
        'implementation_status': { # public_id of CmdbExtendableOption 'IMPLEMENTATION_STATE'
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'finished_implementation_date': { # Date of finished implementation
            'type': 'dict',
            'nullable': True
        },
        'required_resources': { # Required resources text area field
            'type': 'string'
        },
        'costs_for_implementation': { # Costs for implementation
            'type': 'float'
        },
        'costs_for_implementation_currency': { # Costs for implementation currency
            'type': 'string'
        },
        'priority': { # Priority enum (1 = Low, 2 = Medium, 3 = High, 4 = Very high)
            'type': 'integer'
        },
        ### Risk calculation after treatment
        'risk_calculation_after': {
            'type': 'dict',
            'required': True,
            'empty': False,
            'schema': {
                'impacts': { # All impact category sliders
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'impact_category_id': { # public_id of IsmsImpactCategory
                                'type': 'integer',
                            },
                            'impact_id':{ # public_id of IsmsImpact (empty = unrated)
                                'type': 'integer',
                            }
                        }
                    }
                },
                'likelihood_id': { # public_id of IsmsLikelihood (empty = unrated)
                    'type': 'integer',
                },
                'likelihood_value': { # calculation_basis of selected IsmsLikelihood
                    'type':'float',
                    'min': 0.0
                },
                'maximum_impact_id': { # public_id of the maximum IsmsImpact
                    'type': 'integer',
                },
                'maximum_impact_value': { # Maximum calculation_basis of the impact sliders
                    'type':'float',
                    'min': 0.0
                },
                'risk_level_value': { # The calculated risk value
                    'type':'float',
                    'min': 0.0
                }
            }
        },
        ### Checking the effectiveness of the measures ###
        'audit_done_date': { # Audit done date
            'type': 'dict',
            'nullable': True
        },
        'auditor_id_ref_type': { # PersonReferenceType Enum
            'type': 'string',
        },
        'auditor_id': { # public_id of CmdbPerson or CmdbPersonGroup
            'type': 'integer',
            'min': 1,
        },
        'audit_result': { # Audit result text area field
            'type': 'string'
        }
    }

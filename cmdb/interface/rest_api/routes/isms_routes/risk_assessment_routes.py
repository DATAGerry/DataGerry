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
Implementation of all API routes for the IsmsRiskAssessments
"""
import logging
from flask import request, abort
from werkzeug.exceptions import HTTPException

from cmdb.manager import RiskAssessmentManager, ObjectGroupsManager, ObjectsManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsRiskAssessment, IsmsControlMeasureAssignment
from cmdb.models.object_group_model import ObjectGroupMode

from cmdb.framework.results import IterationResult
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses.response_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import (
    InsertSingleResponse,
    GetMultiResponse,
    GetSingleResponse,
    UpdateSingleResponse,
    DeleteSingleResponse,
)

from cmdb.errors.manager.risk_assessment_manager import (
    RiskAssessmentManagerInsertError,
    RiskAssessmentManagerGetError,
    RiskAssessmentManagerUpdateError,
    RiskAssessmentManagerDeleteError,
    RiskAssessmentManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

risk_assessment_blueprint = APIBlueprint('risk_assessment', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@risk_assessment_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@risk_assessment_blueprint.protect(auth=True, right='base.isms.riskAssessment.add')
@risk_assessment_blueprint.validate(IsmsRiskAssessment.SCHEMA)
def insert_isms_risk_assessment(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert an IsmsRiskAssessment into the database

    Args:
        data (IsmsRiskAssessment.SCHEMA): Data of the IsmsRiskAssessment which should be inserted
        request_user (CmdbUser): User requesting this data

    Returns:
        InsertSingleResponse: The new IsmsRiskAssessment and its public_id
    """
    try:
        risk_assessment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.RISK_ASSESSMENT,
                                                                            request_user
                                                                         )
        cm_assignment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.CONTROL_MEASURE_ASSIGNMENT,
                                                                            request_user
                                                                       )
        try:
            data['costs_for_implementation'] = float(f"{float(data['costs_for_implementation']):.2f}")
        except Exception:
            abort(400, "The 'Cost for Implementation' could not be converted to a float!")

        cm_assignments = data.pop('control_measure_assignments', None)

        result_id = risk_assessment_manager.insert_item(data)

        # Create all provided ControlMeasureAssignments if there are any
        if cm_assignments:
            for cma in cm_assignments:
                cma['risk_assessment_id'] = result_id

                cm_assignment_manager.insert_item(cma)

        created_risk_assessment = risk_assessment_manager.get_item(result_id, as_dict=True)

        if not created_risk_assessment:
            abort(404, "Could not retrieve the created RiskAssessment from the database!")

        return InsertSingleResponse(created_risk_assessment, result_id).make_response()
    except HTTPException as http_err:
        raise http_err
    except RiskAssessmentManagerInsertError as err:
        LOGGER.error("[insert_isms_risk_assessment] RiskAssessmentManagerInsertError: %s", err, exc_info=True)
        abort(400, "Failed to insert the new RiskAssessment in the database!")
    except RiskAssessmentManagerGetError as err:
        LOGGER.error("[insert_isms_risk_assessment] RiskAssessmentManagerGetError: %s", err, exc_info=True)
        abort(400, "Failed to retrieve the created RiskAssessment from the database!")
    except Exception as err:
        LOGGER.error("[insert_isms_risk_assessment] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while creating the RiskAssessment!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@risk_assessment_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@risk_assessment_blueprint.protect(auth=True, right='base.isms.riskAssessment.view')
@risk_assessment_blueprint.parse_collection_parameters()
def get_isms_risk_assessments(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple IsmsRiskAssessments

    Args:
        params (CollectionParameters): Filter for requested IsmsRiskAssessments
        request_user (CmdbUser): User requesting this data

    Returns:
        GetMultiResponse: All the IsmsRiskAssessments matching the CollectionParameters
    """
    try:
        body = request.method == 'HEAD'
        risk_assessment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.RISK_ASSESSMENT,
                                                                            request_user
                                                                         )

        object_groups_manager: ObjectGroupsManager = ManagerProvider.get_manager(
                                                                            ManagerType.OBJECT_GROUP,
                                                                            request_user
                                                                         )

        objects_manager: ObjectsManager = ManagerProvider.get_manager(
                                                            ManagerType.OBJECTS,
                                                            request_user
                                                          )

        # Add RiskAssessments from ObjectGroups
        # # STEP 1: Extract object_id from the fixed filter
        original_filter = params.filter or {}
        clauses = original_filter.get('$and', [])
        object_id = None

        for clause in clauses:
            if 'object_id' in clause:
                object_id = clause['object_id']
                break

        # STEP 2: Enhance the filter if object_id was found
        if object_id is not None:
            target_object = objects_manager.get_object(object_id)

            if target_object is not None:
                type_id = target_object['type_id']

                # Find all STATIC groups containing this CmdbObject
                static_groups = object_groups_manager.find(criteria={
                    'group_type': ObjectGroupMode.STATIC,
                    'assigned_ids': object_id
                })

                static_group_ids = [g['public_id'] for g in static_groups]

                # Find all DYNAMIC groups that include this CmdbType
                dynamic_groups = object_groups_manager.find(criteria={
                    'group_type': ObjectGroupMode.DYNAMIC,
                    'assigned_ids': type_id
                })
                dynamic_group_ids = [g['public_id'] for g in dynamic_groups]

                all_group_ids = static_group_ids + dynamic_group_ids

                # STEP 3: Build enhanced filter
                params.filter = {
                    '$or': [
                        {'$and': [{'object_id_ref_type': 'OBJECT'}, {'object_id': object_id}]},
                        {'$and': [{'object_id_ref_type': 'OBJECT_GROUP'}, {'object_id': {'$in': all_group_ids}}]}
                    ]
                }

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))
        iteration_result: IterationResult[IsmsRiskAssessment] = risk_assessment_manager.iterate_items(builder_params)
        risk_assessments_list = [IsmsRiskAssessment.to_json(risk_assessment) for risk_assessment
                                 in iteration_result.results]

        api_response = GetMultiResponse(risk_assessments_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)

        return api_response.make_response()
    except RiskAssessmentManagerIterationError as err:
        LOGGER.error("[get_isms_risk_assessments] RiskAssessmentManagerIterationError: %s", err, exc_info=True)
        abort(400, "Failed to retrieve RiskAssessments from the database!")
    except Exception as err:
        LOGGER.error("[get_isms_risk_assessments] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving RiskAssessments!")


@risk_assessment_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@risk_assessment_blueprint.protect(auth=True, right='base.isms.riskAssessment.view')
def get_isms_risk_assessment(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single IsmsRiskAssessment

    Args:
        public_id (int): public_id of the IsmsRiskAssessment
        request_user (CmdbUser): User requesting this data

    Returns:
        GetSingleResponse: The requested IsmsRiskAssessment
    """
    try:
        risk_assessment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.RISK_ASSESSMENT,
                                                                            request_user
                                                                         )

        requested_risk_assessment = risk_assessment_manager.get_item(public_id, as_dict=True)

        if requested_risk_assessment:
            return GetSingleResponse(requested_risk_assessment, body = request.method == 'HEAD').make_response()

        abort(404, f"The RiskAssessment with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except RiskAssessmentManagerGetError as err:
        LOGGER.error("[get_isms_risk_assessment] RiskAssessmentManagerGetError: %s", err, exc_info=True)
        abort(400, f"Failed to retrieve the RiskAssessment with ID: {public_id} from the database!")
    except Exception as err:
        LOGGER.error("[get_isms_risk_assessment] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, f"An internal server error occured while retrieving the RiskAssessment with ID: {public_id}!")

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@risk_assessment_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@risk_assessment_blueprint.protect(auth=True, right='base.isms.riskAssessment.edit')
@risk_assessment_blueprint.validate(IsmsRiskAssessment.SCHEMA)
def update_isms_risk_assessment(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single IsmsRiskAssessment

    Args:
        public_id (int): public_id of the IsmsRiskAssessment which should be updated
        data (IsmsRiskAssessment.SCHEMA): New IsmsRiskAssessment data
        request_user (CmdbUser): User requesting this data

    Returns:
        UpdateSingleResponse: The new data of the IsmsRiskAssessment
    """
    try:
        risk_assessment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.RISK_ASSESSMENT,
                                                                            request_user
                                                                         )
        cm_assignment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.CONTROL_MEASURE_ASSIGNMENT,
                                                                            request_user
                                                                       )

        to_update_risk_assessment = risk_assessment_manager.get_item(public_id)

        if not to_update_risk_assessment:
            abort(404, f"The RiskAssessment with ID:{public_id} was not found!")

        try:
            data['costs_for_implementation'] = float(f"{float(data['costs_for_implementation']):.2f}")
        except Exception:
            abort(400, "The 'Cost for Implementation' could not be converted to a float!")

        # Handle ControlMeasureAssignments
        cm_assignments: dict = data.pop('control_measure_assignments', [])

        # Handle created ControlMeasureAssignments
        if cm_assignments.get('created'):
            created_cm_assignments: list[dict] = cm_assignments.get('created')

            for created_cma in created_cm_assignments:
                cm_assignment_manager.insert_item(created_cma)

        # Handle updated ControlMeasureAssignments
        if cm_assignments.get('updated'):
            update_cm_assignments: list[dict] = cm_assignments.get('updated')

            for updated_cma in update_cm_assignments:
                cm_assignment_manager.update_item(updated_cma.get('public_id'),
                                                  IsmsControlMeasureAssignment.from_data(updated_cma))

        # Handle deleted ControlMeasureAssignments
        if cm_assignments.get('deleted'):
            deleted_cma_ids = cm_assignments.get('deleted')

            for deleted_cma_id in deleted_cma_ids:
                cm_assignment_manager.delete_item(deleted_cma_id)

        # Update the actual RiskAssessment
        risk_assessment_manager.update_item(public_id, IsmsRiskAssessment.from_data(data))

        return UpdateSingleResponse(data).make_response()
    except HTTPException as http_err:
        raise http_err
    except RiskAssessmentManagerGetError as err:
        LOGGER.error("[update_isms_risk_assessment] RiskAssessmentManagerGetError: %s", err, exc_info=True)
        abort(400, f"Failed to retrieve the RiskAssessment with ID: {public_id} from the database!")
    except RiskAssessmentManagerUpdateError as err:
        LOGGER.error("[update_isms_risk_assessment] RiskAssessmentManagerUpdateError: %s", err, exc_info=True)
        abort(400, f"Failed to update the RiskAssessment with ID: {public_id}!")
    except Exception as err:
        LOGGER.error("[update_isms_risk_assessment] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, f"An internal server error occured while updating the RiskAssessment with ID: {public_id}!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@risk_assessment_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@risk_assessment_blueprint.protect(auth=True, right='base.isms.riskAssessment.delete')
def delete_isms_risk_assessment(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single IsmsRiskAssessment

    Args:
        public_id (int): public_id of the IsmsRiskAssessment which should be deleted
        request_user (CmdbUser): User requesting this data

    Returns:
        DeleteSingleResponse: The deleted IsmsRiskAssessment data
    """
    try:
        risk_assessment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.RISK_ASSESSMENT,
                                                                            request_user
                                                                         )

        to_delete_risk_assessment = risk_assessment_manager.get_item(public_id)

        if not to_delete_risk_assessment:
            abort(404, f"The RiskAssessment with ID:{public_id} was not found!")

        risk_assessment_manager.delete_with_followup(public_id)

        return DeleteSingleResponse(to_delete_risk_assessment).make_response()
    except HTTPException as http_err:
        raise http_err
    except RiskAssessmentManagerDeleteError as err:
        LOGGER.error("[delete_isms_risk_assessment] RiskAssessmentManagerDeleteError: %s", err, exc_info=True)
        abort(400, f"Failed to delete the RiskAssessment with ID:{public_id}!")
    except RiskAssessmentManagerGetError as err:
        LOGGER.error("[delete_isms_risk_assessment] RiskAssessmentManagerGetError: %s", err, exc_info=True)
        abort(400, f"Failed to retrieve the RiskAssessment with ID:{public_id} from the database!")
    except Exception as err:
        LOGGER.error("[delete_isms_risk_assessment] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, f"An internal server error occured while deleting the RiskAssessment with ID: {public_id}!")

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
Implementation of all API routes for the IsmsControlMeassureAssignments
"""
import logging
from flask import request, abort
from werkzeug.exceptions import HTTPException

from cmdb.manager import ControlMeassureAssignmentManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsControlMeassureAssignment

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

from cmdb.errors.manager.control_meassure_assignment_manager import (
    ControlMeassureAssignmentManagerInsertError,
    ControlMeassureAssignmentManagerGetError,
    ControlMeassureAssignmentManagerUpdateError,
    ControlMeassureAssignmentManagerDeleteError,
    ControlMeassureAssignmentManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

control_meassure_assignment_blueprint = APIBlueprint('control_meassure_assignment', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@control_meassure_assignment_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_assignment_blueprint.protect(auth=True, right='base.isms.controlMeassureAssignment.add')
@control_meassure_assignment_blueprint.validate(IsmsControlMeassureAssignment.SCHEMA)
def insert_isms_control_meassure_assignment(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert an IsmsControlMeassureAssignment into the database

    Args:
        data (IsmsControlMeassureAssignment.SCHEMA): Data of the IsmsControlMeassureAssignment which should be inserted
        request_user (CmdbUser): User requesting this data

    Returns:
        InsertSingleResponse: The new IsmsControlMeassureAssignment and its public_id
    """
    try:
        c_m_assignment_manager: ControlMeassureAssignmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.CONTROL_MEASSURE_ASSIGNMENT,
                                                                            request_user
                                                                         )

        result_id = c_m_assignment_manager.insert_item(data)

        created_control_meassure_assignment = c_m_assignment_manager.get_item(result_id, as_dict=True)

        if created_control_meassure_assignment:
            return InsertSingleResponse(created_control_meassure_assignment, result_id).make_response()

        abort(404, "Could not retrieve the created ControlMeassure Assignment from the database!")
    except HTTPException as http_err:
        raise http_err
    except ControlMeassureAssignmentManagerInsertError as err:
        LOGGER.error(
            "[insert_isms_control_meassure_assignment] ControlMeassureAssignmentManagerInsertError: %s",
            err,
            exc_info=True
        )
        abort(400, "Failed to insert the new ControlMeassure Assignment in the database!")
    except ControlMeassureAssignmentManagerGetError as err:
        LOGGER.error(
            "[insert_isms_control_meassure_assignment] ControlMeassureAssignmentManagerGetError: %s", err, exc_info=True
        )
        abort(400, "Failed to retrieve the created ControlMeassure Assignment from the database!")
    except Exception as err:
        LOGGER.error("[insert_isms_control_meassure_assignment] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while creating the ControlMeassure Assignment!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@control_meassure_assignment_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_assignment_blueprint.protect(auth=True, right='base.isms.controlMeassureAssignment.view')
@control_meassure_assignment_blueprint.parse_collection_parameters()
def get_isms_control_meassure_assignments(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple IsmsControlMeassureAssignments

    Args:
        params (CollectionParameters): Filter for requested IsmsControlMeassureAssignments
        request_user (CmdbUser): User requesting this data

    Returns:
        GetMultiResponse: All the IsmsControlMeassureAssignments matching the CollectionParameters
    """
    try:
        body = request.method == 'HEAD'

        c_m_assignment_manager: ControlMeassureAssignmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.CONTROL_MEASSURE_ASSIGNMENT,
                                                                            request_user
                                                                         )

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[IsmsControlMeassureAssignment] = c_m_assignment_manager.iterate_items(
                                                                                                    builder_params
                                                                                                  )
        control_meassure_assignments_list = [IsmsControlMeassureAssignment.to_json(control_meassure_assignment) for
                                             control_meassure_assignment in iteration_result.results]

        api_response = GetMultiResponse(control_meassure_assignments_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)

        return api_response.make_response()
    except ControlMeassureAssignmentManagerIterationError as err:
        LOGGER.error(
            "[get_isms_control_meassure_assignments] ControlMeassureAssignmentManagerIterationError: %s",
            err,
            exc_info=True
        )
        abort(400, "Failed to retrieve ControlMeassure Assignments from the database!")
    except Exception as err:
        LOGGER.error("[get_isms_control_meassure_assignments] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving ControlMeassure Assignments!")


@control_meassure_assignment_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_assignment_blueprint.protect(auth=True, right='base.isms.controlMeassureAssignment.view')
def get_isms_control_meassure_assignment(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single IsmsControlMeassureAssignment

    Args:
        public_id (int): public_id of the IsmsControlMeassureAssignment
        request_user (CmdbUser): User requesting this data

    Returns:
        GetSingleResponse: The requested IsmsControlMeassureAssignment
    """
    try:
        c_m_assignment_manager: ControlMeassureAssignmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.CONTROL_MEASSURE_ASSIGNMENT,
                                                                            request_user
                                                                         )

        requested_control_meassure_assignment = c_m_assignment_manager.get_item(public_id, as_dict=True)

        if requested_control_meassure_assignment:
            return GetSingleResponse(requested_control_meassure_assignment,
                                     body = request.method == 'HEAD').make_response()

        abort(404, f"The ControlMeassure Assignment with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except ControlMeassureAssignmentManagerGetError as err:
        LOGGER.error(
            "[get_isms_control_meassure_assignment] ControlMeassureAssignmentManagerGetError: %s", err, exc_info=True
        )
        abort(400, f"Failed to retrieve the ControlMeassure Assignment with ID: {public_id} from the database!")
    except Exception as err:
        LOGGER.error("[get_isms_control_meassure_assignment] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(
            500,
            f"An internal server error occured while retrieving the ControlMeassure Assignment with ID: {public_id}!"
        )

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@control_meassure_assignment_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_assignment_blueprint.protect(auth=True, right='base.isms.controlMeassureAssignment.edit')
@control_meassure_assignment_blueprint.validate(IsmsControlMeassureAssignment.SCHEMA)
def update_isms_control_meassure_assignment(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single IsmsControlMeassureAssignment

    Args:
        public_id (int): public_id of the IsmsControlMeassureAssignment which should be updated
        data (IsmsControlMeassureAssignment.SCHEMA): New IsmsControlMeassureAssignment data
        request_user (CmdbUser): User requesting this data

    Returns:
        UpdateSingleResponse: The new data of the IsmsControlMeassureAssignment
    """
    try:
        c_m_assignment_manager: ControlMeassureAssignmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.CONTROL_MEASSURE_ASSIGNMENT,
                                                                            request_user
                                                                         )

        to_update_control_meassure_assignment = c_m_assignment_manager.get_item(public_id)

        if not to_update_control_meassure_assignment:
            abort(404, f"The ControlMeassure Assignment with ID:{public_id} was not found!")

        c_m_assignment_manager.update_item(public_id, IsmsControlMeassureAssignment.from_data(data))

        return UpdateSingleResponse(data).make_response()
    except HTTPException as http_err:
        raise http_err
    except ControlMeassureAssignmentManagerGetError as err:
        LOGGER.error(
            "[update_isms_control_meassure_assignment] ControlMeassureAssignmentManagerGetError: %s", err, exc_info=True
        )
        abort(400, f"Failed to retrieve the ControlMeassure Assignment with ID: {public_id} from the database!")
    except ControlMeassureAssignmentManagerUpdateError as err:
        LOGGER.error(
            "[update_isms_control_meassure_assignment] ControlMeassureAssignmentManagerUpdateError: %s",
            err,
            exc_info=True
        )
        abort(400, f"Failed to update the ControlMeassure Assignment with ID: {public_id}!")
    except Exception as err:
        LOGGER.error("[update_isms_control_meassure_assignment] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500,
            f"An internal server error occured while updating the ControlMeassure Assignment with ID: {public_id}!"
        )

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@control_meassure_assignment_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_assignment_blueprint.protect(auth=True, right='base.isms.controlMeassureAssignment.delete')
def delete_isms_control_meassure_assignment(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single IsmsControlMeassureAssignment

    Args:
        public_id (int): public_id of the IsmsControlMeassureAssignment which should be deleted
        request_user (CmdbUser): User requesting this data

    Returns:
        DeleteSingleResponse: The deleted IsmsControlMeassureAssignment data
    """
    try:
        c_m_assignment_manager: ControlMeassureAssignmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.CONTROL_MEASSURE_ASSIGNMENT,
                                                                            request_user
                                                                         )

        to_delete_control_meassure_assignment = c_m_assignment_manager.get_item(public_id)

        if not to_delete_control_meassure_assignment:
            abort(404, f"The ControlMeassure Assignment with ID:{public_id} was not found!")

        c_m_assignment_manager.delete_item(public_id)

        return DeleteSingleResponse(to_delete_control_meassure_assignment).make_response()
    except HTTPException as http_err:
        raise http_err
    except ControlMeassureAssignmentManagerDeleteError as err:
        LOGGER.error(
            "[delete_isms_control_meassure_assignment] ControlMeassureAssignmentManagerDeleteError: %s",
            err,
            exc_info=True
        )
        abort(400, f"Failed to delete the ControlMeassure Assignment with ID:{public_id}!")
    except ControlMeassureAssignmentManagerGetError as err:
        LOGGER.error(
            "[delete_isms_control_meassure_assignment] ControlMeassureAssignmentManagerGetError: %s",
            err,
            exc_info=True
        )
        abort(400, f"Failed to retrieve the ControlMeassure Assignment with ID:{public_id} from the database!")
    except Exception as err:
        LOGGER.error(
            "[delete_isms_control_meassure_assignment] Exception: %s. Type: %s", err, type(err),
            exc_info=True
        )
        abort(500,
            f"An internal server error occured while deleting the ControlMeassure Assignment with ID: {public_id}!"
        )

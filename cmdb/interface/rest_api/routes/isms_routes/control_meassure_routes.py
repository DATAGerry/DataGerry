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
Implementation of all API routes for the IsmsControlMeassures
"""
import logging
from flask import request, abort
from werkzeug.exceptions import HTTPException

from cmdb.manager import ControlMeassureManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsControlMeassure

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

from cmdb.errors.manager.control_meassure_manager import (
    ControlMeassureManagerInsertError,
    ControlMeassureManagerGetError,
    ControlMeassureManagerUpdateError,
    ControlMeassureManagerDeleteError,
    ControlMeassureManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

control_meassure_blueprint = APIBlueprint('control_meassure', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@control_meassure_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_blueprint.protect(auth=True, right='base.isms.controlMeassure.add')
@control_meassure_blueprint.validate(IsmsControlMeassure.SCHEMA)
def insert_isms_control_meassure(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert an IsmsControlMeassure into the database

    Args:
        data (IsmsControlMeassure.SCHEMA): Data of the IsmsControlMeassure which should be inserted
        request_user (CmdbUser): User requesting this data

    Returns:
        InsertSingleResponse: The new IsmsControlMeassure and its public_id
    """
    try:
        control_meassure_manager: ControlMeassureManager = ManagerProvider.get_manager(ManagerType.CONTROL_MEASSURE,
                                                                                       request_user)

        result_id: int = control_meassure_manager.insert_item(data)

        created_control_meassure: dict = control_meassure_manager.get_item(result_id, as_dict=True)

        if created_control_meassure:
            return InsertSingleResponse(created_control_meassure, result_id).make_response()

        abort(404, "Could not retrieve the created ControlMeassure from the database!")
    except HTTPException as http_err:
        raise http_err
    except ControlMeassureManagerInsertError as err:
        LOGGER.error("[insert_isms_control_meassure] ControlMeassureManagerInsertError: %s", err, exc_info=True)
        abort(400, "Could not insert the new ControlMeassure in the database!")
    except ControlMeassureManagerGetError as err:
        LOGGER.error("[insert_isms_control_meassure] ControlMeassureManagerGetError: %s", err, exc_info=True)
        abort(400, "Failed to retrieve the created ControlMeassure from the database!")
    except Exception as err:
        LOGGER.error("[insert_isms_control_meassure] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while creating the ControlMeassure!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@control_meassure_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_blueprint.protect(auth=True, right='base.isms.controlMeassure.view')
@control_meassure_blueprint.parse_collection_parameters()
def get_isms_control_meassures(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple IsmsControlMeassures

    Args:
        params (CollectionParameters): Filter for requested IsmsControlMeassures
        request_user (CmdbUser): User requesting this data

    Returns:
        GetMultiResponse: All the IsmsControlMeassures matching the CollectionParameters
    """
    try:
        body = request.method == 'HEAD'

        control_meassure_manager: ControlMeassureManager = ManagerProvider.get_manager(ManagerType.CONTROL_MEASSURE,
                                                                                       request_user)

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[IsmsControlMeassure] = control_meassure_manager.iterate_items(builder_params)
        control_meassures_list = [IsmsControlMeassure.to_json(control_meassure) for control_meassure
                                  in iteration_result.results]

        api_response = GetMultiResponse(control_meassures_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)

        return api_response.make_response()
    except ControlMeassureManagerIterationError as err:
        LOGGER.error("[get_isms_control_meassures] ControlMeassureManagerIterationError: %s", err, exc_info=True)
        abort(400, "Failed to retrieve ControlMeassures from the database!")
    except Exception as err:
        LOGGER.error("[get_isms_control_meassures] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving ControlMeassures!")


@control_meassure_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_blueprint.protect(auth=True, right='base.isms.controlMeassure.view')
def get_isms_control_meassure(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single IsmsControlMeassure

    Args:
        public_id (int): public_id of the IsmsControlMeassure
        request_user (CmdbUser): User requesting this data

    Returns:
        GetSingleResponse: The requested IsmsControlMeassure
    """
    try:
        control_meassure_manager: ControlMeassureManager = ManagerProvider.get_manager(ManagerType.CONTROL_MEASSURE,
                                                                                       request_user)

        requested_control_meassure = control_meassure_manager.get_item(public_id, as_dict=True)

        if requested_control_meassure:
            return GetSingleResponse(requested_control_meassure, body = request.method == 'HEAD').make_response()

        abort(404, f"The ControlMeassure with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except ControlMeassureManagerGetError as err:
        LOGGER.error("[get_isms_control_meassure] ControlMeassureManagerGetError: %s", err, exc_info=True)
        abort(400, f"Failed to retrieve the ControlMeassure with ID: {public_id} from the database!")
    except Exception as err:
        LOGGER.error("[get_isms_control_meassure] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, f"An internal server error occured while retrieving the ControlMeassure with ID: {public_id}!")

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@control_meassure_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_blueprint.protect(auth=True, right='base.isms.controlMeassure.edit')
@control_meassure_blueprint.validate(IsmsControlMeassure.SCHEMA)
def update_isms_control_meassure(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single IsmsControlMeassure

    Args:
        public_id (int): public_id of the IsmsControlMeassure which should be updated
        data (IsmsControlMeassure.SCHEMA): New IsmsControlMeassure data
        request_user (CmdbUser): User requesting this data

    Returns:
        UpdateSingleResponse: The new data of the IsmsControlMeassure
    """
    try:
        control_meassure_manager: ControlMeassureManager = ManagerProvider.get_manager(ManagerType.CONTROL_MEASSURE,
                                                                                       request_user)

        to_update_control_meassure = control_meassure_manager.get_item(public_id)

        if not to_update_control_meassure:
            abort(404, f"The ControlMeassure with ID:{public_id} was not found!")

        control_meassure_manager.update_item(public_id, IsmsControlMeassure.from_data(data))

        return UpdateSingleResponse(data).make_response()
    except HTTPException as http_err:
        raise http_err
    except ControlMeassureManagerGetError as err:
        LOGGER.error("[update_isms_control_meassure] ControlMeassureManagerGetError: %s", err, exc_info=True)
        abort(400, f"Failed to retrieve the ControlMeassure with ID: {public_id} from the database!")
    except ControlMeassureManagerUpdateError as err:
        LOGGER.error("[update_isms_control_meassure] ControlMeassureManagerUpdateError: %s", err, exc_info=True)
        abort(400, f"Failed to update the ControlMeassure with ID: {public_id}!")
    except Exception as err:
        LOGGER.error("[update_isms_control_meassure] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, f"An internal server error occured while updating the ControlMeassure with ID: {public_id}!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@control_meassure_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@control_meassure_blueprint.protect(auth=True, right='base.isms.controlMeassure.delete')
def delete_isms_control_meassure(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single IsmsControlMeassure

    Args:
        public_id (int): public_id of the IsmsControlMeassure which should be deleted
        request_user (CmdbUser): User requesting this data

    Returns:
        DeleteSingleResponse: The deleted IsmsControlMeassure data
    """
    try:
        control_meassure_manager: ControlMeassureManager = ManagerProvider.get_manager(ManagerType.CONTROL_MEASSURE,
                                                                                       request_user)

        to_delete_control_meassure = control_meassure_manager.get_item(public_id, as_dict=True)

        if not to_delete_control_meassure:
            abort(404, f"The ControlMeassure with ID:{public_id} was not found!")

        control_meassure_manager.delete_item(public_id)

        return DeleteSingleResponse(to_delete_control_meassure).make_response()
    except HTTPException as http_err:
        raise http_err
    except ControlMeassureManagerDeleteError as err:
        LOGGER.error("[delete_isms_control_meassure] ControlMeassureManagerDeleteError: %s", err, exc_info=True)
        abort(400, f"Failed to delete the ControlMeassure with ID:{public_id}!")
    except ControlMeassureManagerGetError as err:
        LOGGER.error("[delete_isms_control_meassure] ControlMeassureManagerGetError: %s", err, exc_info=True)
        abort(400, f"Failed to retrieve the ControlMeassure with ID:{public_id} from the database!")
    except Exception as err:
        LOGGER.error("[delete_isms_control_meassure] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, f"An internal server error occured while deleting the ControlMeassure with ID: {public_id}!")

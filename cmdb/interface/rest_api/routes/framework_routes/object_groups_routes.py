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
Implementation of all API routes for the CmdbObjectGroups
"""
import logging
from flask import request, abort
from werkzeug.exceptions import HTTPException

from cmdb.manager import ObjectGroupsManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.object_group_model import CmdbObjectGroup

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

from cmdb.errors.manager.object_groups_manager import (
    ObjectGroupsManagerInsertError,
    ObjectGroupsManagerGetError,
    ObjectGroupsManagerUpdateError,
    ObjectGroupsManagerDeleteError,
    ObjectGroupsManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

object_group_blueprint = APIBlueprint('object_group', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@object_group_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@object_group_blueprint.protect(auth=True, right='base.framework.objectGroup.add')
@object_group_blueprint.validate(CmdbObjectGroup.SCHEMA)
def insert_cmdb_object_group(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert an CmdbObjectGroup into the database

    Args:
        data (CmdbObjectGroup.SCHEMA): Data of the CmdbObjectGroup which should be inserted
        request_user (CmdbUser): User requesting this data

    Returns:
        InsertSingleResponse: The new CmdbObjectGroup and its public_id
    """
    try:
        object_groups_manager: ObjectGroupsManager = ManagerProvider.get_manager(
                                                                            ManagerType.OBJECT_GROUP,
                                                                            request_user
                                                                         )

        result_id: int = object_groups_manager.insert_object_group(data)

        created_object_group: dict = object_groups_manager.get_object_group(result_id)

        if created_object_group:
            return InsertSingleResponse(created_object_group, result_id).make_response()

        return abort(404, "Could not retrieve the created ObjectGroup from the database!")
    except HTTPException as http_err:
        raise http_err
    except ObjectGroupsManagerInsertError as err:
        LOGGER.error("[insert_cmdb_object_group] ObjectGroupsManagerInsertError: %s", err, exc_info=True)
        return abort(400, "Could not insert the new ObjectGroup in the database!")
    except ObjectGroupsManagerGetError as err:
        LOGGER.error("[insert_cmdb_object_group] ObjectGroupsManagerGetError: %s", err, exc_info=True)
        return abort(400, "Failed to retrieve the created ObjectGroup from the database!")
    except Exception as err:
        LOGGER.error("[insert_cmdb_object_group] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "An internal server error occured while creating the ObjectGroup!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@object_group_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@object_group_blueprint.protect(auth=True, right='base.framework.objectGroup.view')
@object_group_blueprint.parse_collection_parameters()
def get_cmdb_object_groups(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple CmdbObjectGroups

    Args:
        params (CollectionParameters): Filter for requested CmdbObjectGroups
        request_user (CmdbUser): User requesting this data

    Returns:
        GetMultiResponse: All the CmdbObjectGroups matching the CollectionParameters
    """
    try:
        body = request.method == 'HEAD'

        object_groups_manager: ObjectGroupsManager = ManagerProvider.get_manager(
                                                                            ManagerType.OBJECT_GROUP,
                                                                            request_user
                                                                         )

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbObjectGroup] = object_groups_manager.iterate(builder_params)
        object_groups_list = [CmdbObjectGroup.to_json(object_group) for object_group
                                 in iteration_result.results]

        api_response = GetMultiResponse(object_groups_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)

        return api_response.make_response()
    except ObjectGroupsManagerIterationError as err:
        LOGGER.error("[get_cmdb_object_groups] ObjectGroupsManagerIterationError: %s", err, exc_info=True)
        return abort(400, "Failed to retrieve ObjectGroups from the database!")
    except Exception as err:
        LOGGER.error("[get_cmdb_object_groups] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


@object_group_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@object_group_blueprint.protect(auth=True, right='base.framework.objectGroup.view')
def get_cmdb_object_group(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single CmdbObjectGroup

    Args:
        public_id (int): public_id of the CmdbObjectGroup
        request_user (CmdbUser): User requesting this data

    Returns:
        GetSingleResponse: The requested CmdbObjectGroup
    """
    try:
        object_groups_manager: ObjectGroupsManager = ManagerProvider.get_manager(
                                                                            ManagerType.OBJECT_GROUP,
                                                                            request_user
                                                                         )

        requested_object_group = object_groups_manager.get_object_group(public_id)

        if requested_object_group:
            return GetSingleResponse(requested_object_group, body = request.method == 'HEAD').make_response()

        return abort(404, f"The ObjectGroup with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except ObjectGroupsManagerGetError as err:
        LOGGER.error("[get_cmdb_object_group] ObjectGroupsManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the ObjectGroup with ID: {public_id} from the database!")
    except Exception as err:
        LOGGER.error("[get_cmdb_object_group] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@object_group_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@object_group_blueprint.protect(auth=True, right='base.framework.objectGroup.edit')
@object_group_blueprint.validate(CmdbObjectGroup.SCHEMA)
def update_cmdb_object_group(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single CmdbObjectGroup

    Args:
        public_id (int): public_id of the CmdbObjectGroup which should be updated
        data (CmdbObjectGroup.SCHEMA): New CmdbObjectGroup data
        request_user (CmdbUser): User requesting this data

    Returns:
        UpdateSingleResponse: The new data of the CmdbObjectGroup
    """
    try:
        object_groups_manager: ObjectGroupsManager = ManagerProvider.get_manager(
                                                                            ManagerType.OBJECT_GROUP,
                                                                            request_user
                                                                         )

        to_update_object_group = object_groups_manager.get_object_group(public_id)

        if not to_update_object_group:
            return abort(404, f"The ObjectGroup with ID:{public_id} was not found!")

        object_group = CmdbObjectGroup.from_data(data)

        object_groups_manager.update_object_group(public_id, object_group)

        return UpdateSingleResponse(data).make_response()
    except HTTPException as http_err:
        raise http_err
    except ObjectGroupsManagerGetError as err:
        LOGGER.error("[update_cmdb_object_group] ObjectGroupsManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the ObjectGroup with ID: {public_id} from the database!")
    except ObjectGroupsManagerUpdateError as err:
        LOGGER.error("[update_cmdb_object_group] ObjectGroupsManagerUpdateError: %s", err, exc_info=True)
        return abort(400, f"Failed to update the ObjectGroup with ID: {public_id}!")
    except Exception as err:
        LOGGER.error("[update_cmdb_object_group] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@object_group_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@object_group_blueprint.protect(auth=True, right='base.framework.objectGroup.delete')
def delete_cmdb_object_group(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single CmdbObjectGroup

    Args:
        public_id (int): public_id of the CmdbObjectGroup which should be deleted
        request_user (CmdbUser): User requesting this data

    Returns:
        DeleteSingleResponse: The deleted CmdbObjectGroup data
    """
    try:
        object_groups_manager: ObjectGroupsManager = ManagerProvider.get_manager(
                                                                            ManagerType.OBJECT_GROUP,
                                                                            request_user
                                                                         )

        to_delete_object_group = object_groups_manager.get_object_group(public_id)

        if not to_delete_object_group:
            return abort(404, f"The ObjectGroup with ID:{public_id} was not found!")

        object_groups_manager.delete_object_group(public_id)

        return DeleteSingleResponse(to_delete_object_group).make_response()
    except HTTPException as http_err:
        raise http_err
    except ObjectGroupsManagerDeleteError as err:
        LOGGER.error("[delete_cmdb_object_group] ObjectGroupsManagerDeleteError: %s", err, exc_info=True)
        return abort(400, f"Failed to delete the ObjectGroup with ID:{public_id}!")
    except ObjectGroupsManagerGetError as err:
        LOGGER.error("[delete_cmdb_object_group] ObjectGroupsManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the ObjectGroup with ID:{public_id} from the database!")
    except Exception as err:
        LOGGER.error("[delete_cmdb_object_group] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

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
"""document"""
#TODO: DOCUMENT-FIX
import logging
from flask import request, abort
from werkzeug.exceptions import HTTPException

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager import (
    GroupsManager,
    UsersManager,
)

from cmdb.framework.results import IterationResult
from cmdb.models.group_model import CmdbUserGroup, GroupDeleteMode
from cmdb.models.user_model import CmdbUser
from cmdb.models.right_model.all_rights import flat_rights_tree, __all__ as rights
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.rest_api.responses.response_parameters.group_parameters import GroupDeletionParameters
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import (
    DeleteSingleResponse,
    UpdateSingleResponse,
    InsertSingleResponse,
    GetMultiResponse,
    GetSingleResponse,
)

from cmdb.errors.manager.groups_manager import (
    GroupsManagerDeleteError,
    GroupsManagerGetError,
    GroupsManagerInsertError,
    GroupsManagerIterationError,
    GroupsManagerUpdateError,
)
from cmdb.manager.users_manager import (
    UsersManagerGetError,
    UsersManagerUpdateError,
    UsersManagerDeleteError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

groups_blueprint = APIBlueprint('groups', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@groups_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@groups_blueprint.protect(auth=True, right='base.user-management.group.add')
@groups_blueprint.validate(CmdbUserGroup.SCHEMA)
def insert_user_group(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` to insert a single CmdbUserGroup

    Args:
        `data` (CmdbUserGroup.SCHEMA): Data of the new CmdbUserGroup

    Returns:
        `InsertSingleResponse`: The public_id and the newly created CmdbUserGroup
    """
    try:
        groups_manager: GroupsManager = ManagerProvider.get_manager(ManagerType.GROUPS_MANAGER, request_user)

        result_id = groups_manager.insert_group(data)
        group = groups_manager.get_group(result_id)

        api_response = InsertSingleResponse(result_id=result_id, raw=CmdbUserGroup.to_dict(group))

        return api_response.make_response()
    except GroupsManagerInsertError as err:
        LOGGER.error("[insert_user_group] %s", err, exc_info=True)
        return abort(400, "Could not insert the new user group in the database!")
    except GroupsManagerGetError as err:
        LOGGER.error("[insert_user_group] %s", err, exc_info=True)
        return abort(400, "Could not retrieve the created user group from the database!")
    except Exception as err:
        LOGGER.error("[insert_user_group] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@groups_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@groups_blueprint.protect(auth=True, right='base.user-management.group.view')
@groups_blueprint.parse_collection_parameters()
def get_user_groups(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple CmdbUserGroups

    Args:
        `params` (CollectionParameters): Filter for requested CmdbUserGroups

    Returns:
        `GetMultiResponse`: All the CmdbUserGroups matching the CollectionParameters
    """
    try:
        groups_manager: GroupsManager = ManagerProvider.get_manager(ManagerType.GROUPS_MANAGER, request_user)

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbUserGroup] = groups_manager.iterate(builder_params)
        groups = [CmdbUserGroup.to_dict(group) for group in iteration_result.results]

        api_response = GetMultiResponse(groups,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        body=request.method == 'HEAD')

        return api_response.make_response()
    except GroupsManagerIterationError as err:
        LOGGER.error("[get_user_groups] %s", err, exc_info=True)
        return abort(400, "Could not iterate the user groups!")
    except Exception as err:
        LOGGER.error("[get_user_groups] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


@groups_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@groups_blueprint.protect(auth=True, right='base.user-management.group.view')
def get_user_group(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single CmdbUserGroup

    Args:
        `public_id` (int): public_id of the requested CmdbUserGroup

    Returns:
        `GetSingleResponse`: The requested CmdbUserGroup
    """
    try:
        groups_manager: GroupsManager = ManagerProvider.get_manager(ManagerType.GROUPS_MANAGER, request_user)

        group = groups_manager.get_group(public_id)

        api_response = GetSingleResponse(CmdbUserGroup.to_dict(group), body=request.method == 'HEAD')

        return api_response.make_response()
    except GroupsManagerGetError as err:
        LOGGER.error("[get_user_group] %s", err, exc_info=True)
        return abort(400, "Could not retrieve the user group!")
    except Exception as err:
        LOGGER.error("[get_user_group] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@groups_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@groups_blueprint.protect(auth=True, right='base.user-management.group.edit')
@groups_blueprint.validate(CmdbUserGroup.SCHEMA)
def update_user_group(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route fto update a single CmdbUserGroup

    Args:
        `public_id` (int): public_id of the CmdbUserGroup which should be updated
        `data` (CmdbUserGroup.SCHEMA): New version for the CmdbUserGroup

    Returns:
        `UpdateSingleResponse`: The new version of the CmdbUserGroup
    """
    try:
        groups_manager: GroupsManager = ManagerProvider.get_manager(ManagerType.GROUPS_MANAGER, request_user)

        group = CmdbUserGroup.from_data(data=data, rights=flat_rights_tree(rights))
        group_dict = CmdbUserGroup.to_dict(group)
        group_dict['rights'] = [right.get('name') for right in group_dict.get('rights', [])]

        #TODO: ERROR-FIX (Add try/except block)
        groups_manager.update_group(public_id, group_dict)

        api_response = UpdateSingleResponse(group_dict)

        return api_response.make_response()
    except GroupsManagerUpdateError as err:
        LOGGER.error("[update_user_group] %s", err, exc_info=True)
        return abort(400, f"User group with public_id:{public_id} could not be updated!")
    except Exception as err:
        LOGGER.error("[update_user_group] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@groups_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@groups_blueprint.protect(auth=True, right='base.user-management.group.delete')
@groups_blueprint.parse_parameters(GroupDeletionParameters)
def delete_user_group(public_id: int, params: GroupDeletionParameters, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single CmdbUserGroup

    Args:
        `public_id` (int): public_id of the CmdbUserGroup
        `params` (GroupDeletionParameters): Optional action parameters for handling users when the group is deleted

    Returns:
        `DeleteSingleResponse`: The deleted CmdbUserGroup
    """
    try:
        groups_manager: GroupsManager = ManagerProvider.get_manager(ManagerType.GROUPS_MANAGER, request_user)
        users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)


        # Check if action is set
        #TODO: REFACTOR-FIX (give the user handling an own function)
        if params.action:
            users_in_group: list[CmdbUser] = users_manager.get_many_users({'group_id': public_id})

            if len(users_in_group) > 0:
                if params.action == GroupDeleteMode.MOVE.value:
                    if params.group_id:
                        for user in users_in_group:
                            user.group_id = int(params.group_id)

                            try:
                                users_manager.update_user(user.public_id, user)
                            except UsersManagerUpdateError as err:
                                LOGGER.error("[delete_user_group]  %s", err)
                                return abort(400, f"Could not move user: {user.public_id} to \
                                                    group: {params.group_id}")

                if params.action == GroupDeleteMode.DELETE.value:
                    for user in users_in_group:
                        try:
                            users_manager.delete_user(user.public_id)
                        except UsersManagerDeleteError as err:
                            LOGGER.error("[delete_user_group]  %s", err)
                            return abort(400, f'Could not delete user with ID: {user.public_id} !')

        deleted_group = groups_manager.delete_group(public_id)

        api_response = DeleteSingleResponse(raw=CmdbUserGroup.to_dict(deleted_group))

        return api_response.make_response()
    except HTTPException as http_err:
        raise http_err
    except UsersManagerGetError as err:
        LOGGER.error("[delete_user_group] %s", err, exc_info=True)
        return abort(400, "Could not retrieve users which are in the user group!")
    except GroupsManagerDeleteError as err:
        LOGGER.error("[delete_user_group] %s", err, exc_info=True)
        return abort(400, "Could not delete the user group!")
    except Exception as err:
        LOGGER.error("[update_user_group] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

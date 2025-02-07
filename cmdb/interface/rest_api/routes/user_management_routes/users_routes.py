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
Implementation of all API routes for CmdbUsers
"""
import json
import logging
from datetime import datetime, timezone
from flask import abort, request, current_app
from werkzeug.exceptions import HTTPException

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager import (
    SecurityManager,
    UsersManager,
)

from cmdb.framework.results import IterationResult
from cmdb.models.user_model import CmdbUser
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.rest_api.responses import (
    DeleteSingleResponse,
    UpdateSingleResponse,
    InsertSingleResponse,
    GetMultiResponse,
    GetSingleResponse,
)

from cmdb.errors.manager.users_manager import (
    UsersManagerGetError,
    UsersManagerInsertError,
    UsersManagerIterationError,
    UsersManagerUpdateError,
    UsersManagerDeleteError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

users_blueprint = APIBlueprint('users', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@users_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.SUPER_ADMIN)
@users_blueprint.protect(auth=True, right='base.user-management.user.add')
@users_blueprint.validate(CmdbUser.SCHEMA)
def insert_user(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert a CmdbUser into the database

    Args:
        `data` (CmdbUser.SCHEMA): Data of a new CmdbUser

    Returns:
        `InsertSingleResponse`: Insert response with the new CmdbUser and the corresponding public_id
    """
    #TODO: REFATOR-FIX
    try:
        users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)
        security_manager: SecurityManager = ManagerProvider.get_manager(ManagerType.SECURITY_MANAGER, request_user)

        user_password = data['password']
        data['password'] = security_manager.generate_hmac(data['password'])
        data['registration_time'] = datetime.now(timezone.utc)

        try:
            if current_app.cloud_mode:
                # Confirm database is available from the request
                data['database'] = request_user.database
        except KeyError:
            return abort(400, "The database of the user could not be retrieved!")

        try:
            if current_app.cloud_mode:
                # Confirm an email was provided when creating the user
                user_email = data['email']

                if not user_email:
                    raise KeyError
        except KeyError:
            LOGGER.error("[insert_user] No email was provided!")
            return abort(400, "The email is mandatory to create a new user!")

        # Check if email already exists
        try:
            if current_app.cloud_mode:
                user_with_given_email = users_manager.get_user_by({'email': user_email})

                if user_with_given_email:
                    return abort(400, "The email is already in use!")
        except UsersManagerGetError:
            pass

        if current_app.cloud_mode and current_app.local_mode:
            # Open file and check if user exists
            with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
                users_data = json.load(users_file)

                if user_email in users_data:
                    return abort(400, "A user with this email already exists!")

            # Create the user in the dict
            users_data[user_email] = {
                "user_name": data["user_name"],
                "password": user_password,
                "email": data["email"],
                "database": data["database"]
            }

            with open('etc/test_users.json', 'w', encoding='utf-8') as cur_users_file:
                json.dump(users_data, cur_users_file, ensure_ascii=False, indent=4)

        result_id = users_manager.insert_user(data)

        #Confirm that user is created
        user = users_manager.get_user(result_id)

        api_response = InsertSingleResponse(CmdbUser.to_dict(user), result_id)

        return api_response.make_response()
    except HTTPException as http_err:
        raise http_err
    except UsersManagerInsertError as err:
        LOGGER.error("[insert_user] %s", err, exc_info=True)
        return abort(400, "Could not create the user in database!")
    except UsersManagerGetError as err:
        LOGGER.error("[insert_user] %s", err, exc_info=True)
        return abort(500, "Could not retrieve the created user from the database!")
    except Exception as err:
        LOGGER.error("[insert_user] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@users_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@users_blueprint.protect(auth=True, right='base.user-management.user.view')
@users_blueprint.parse_collection_parameters()
def get_users(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for retrieving multiple CmdbUsers with a filter

    Args:
        `params` (CollectionParameters): Passed parameters over the http query string

    Returns:
        `GetMultiResponse`: The CmdbUsers matching the given filter
    """
    try:
        users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbUser] = users_manager.iterate(builder_params)
        users = [CmdbUser.to_dict(user) for user in iteration_result.results]

        api_response = GetMultiResponse(users,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        body=request.method == 'HEAD')

        return api_response.make_response()
    except UsersManagerIterationError as err:
        LOGGER.error("[get_users] %s", err, exc_info=True)
        return abort(400, "Could not iterate the requested users!")
    except Exception as err:
        LOGGER.error("[get_users] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")




@users_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@users_blueprint.protect(auth=True, right='base.user-management.user.view', excepted={'public_id': 'public_id'})
def get_user(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for a single CmdbUser

    Args:
        `public_id` (int): public_id of the requested CmdbUser

    Returns:
        `GetSingleResponse`: Raw data of the requested CmdbUser
    """
    try:
        users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)

        user: CmdbUser = users_manager.get_user(public_id)

        api_response = GetSingleResponse(CmdbUser.to_dict(user), body=request.method == 'HEAD')

        return api_response.make_response()
    except UsersManagerGetError as err:
        LOGGER.error("[get_user] %s", err, exc_info=True)
        return abort(404, f"Could not retrieve the user with public_id: {public_id}")
    except Exception as err:
        LOGGER.error("[get_user] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")



# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@users_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.SUPER_ADMIN)
@users_blueprint.protect(auth=True, right='base.user-management.user.edit', excepted={'public_id': 'public_id'})
@users_blueprint.validate(CmdbUser.SCHEMA)
def update_user(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single CmdbUser

    Args:
        `public_id` (int): public_id of the CmdbUser which should be updated
        `data` (CmdbUser.SCHEMA): New values for the CmdbUser

    Returns:
        `UpdateSingleResponse`: The updated raw data of the CmdbUser
    """
    try:
        users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)

        user = CmdbUser.from_data(data=data)
        users_manager.update_user(public_id, user)

        api_response = UpdateSingleResponse(CmdbUser.to_dict(user))

        return api_response.make_response()
    except UsersManagerUpdateError as err:
        LOGGER.error("[update_user] %s", err, exc_info=True)
        return abort(400, f"Could not update the user with public_id: {public_id}!")
    except Exception as err:
        LOGGER.error("[update_user] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


@users_blueprint.route('/<int:public_id>/password', methods=['PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.SUPER_ADMIN)
@users_blueprint.protect(auth=True, right='base.user-management.user.edit', excepted={'public_id': 'public_id'})
def change_user_password(public_id: int, request_user: CmdbUser):
    """
    HTTP `PATCH` route for changing the password of a CmdbUser

    Args:
        `public_id` (int): public_id of the CmdbUser

    Returns:
        `UpdateSingleResponse`:  The CmdbUser with new password
    """
    try:
        users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)
        security_manager: SecurityManager = ManagerProvider.get_manager(ManagerType.SECURITY_MANAGER, request_user)

        user = users_manager.get_user(public_id)

        password = security_manager.generate_hmac(request.json.get('password'))
        user.password = password
        users_manager.update_user(public_id, user)

        api_response = UpdateSingleResponse(CmdbUser.to_dict(user))

        return api_response.make_response()
    except UsersManagerGetError as err:
        LOGGER.error("[change_user_password] %s", err, exc_info=True)
        return abort(404, f"Could not retrieve the user with public_id: {public_id}")
    except UsersManagerUpdateError as err:
        LOGGER.error("[update_user] %s", err, exc_info=True)
        return abort(400, f"Could not change the password for user with public_id: {public_id}!")
    except Exception as err:
        LOGGER.error("[update_user] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@users_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.SUPER_ADMIN)
@users_blueprint.protect(auth=True, right='base.user-management.user.delete')
def delete_user(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single CmdbUser

    Args:
        `public_id` (int): public_id of the CmdbUser

    Returns:
        `DeleteSingleResponse`: Raw data of the deleted CmdbUser
    """
    try:
        users_manager: UsersManager = ManagerProvider.get_manager(ManagerType.USERS_MANAGER, request_user)

        deleted_group = users_manager.delete_user(public_id)

        api_response = DeleteSingleResponse(raw=CmdbUser.to_dict(deleted_group))

        return api_response.make_response()
    except UsersManagerDeleteError as err:
        LOGGER.error("[delete_user] %s", err, exc_info=True)
        return abort(400, f"Could not delete user with ID: {public_id} !")
    except UsersManagerGetError as err:
        LOGGER.error("[delete_user] %s", err, exc_info=True)
        return abort(404, f"Could not retrieve the user with ID: {public_id}")
    except Exception as err:
        LOGGER.error("[delete_user] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

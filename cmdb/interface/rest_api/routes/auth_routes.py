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
from typing import Tuple
from datetime import datetime, timezone
from flask import request, current_app, abort
from werkzeug.exceptions import HTTPException

from cmdb.database import MongoDatabaseManager
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager import (
    SecurityManager,
    SettingsReaderManager,
    SettingsWriterManager,
    UsersManager,
)

from cmdb.models.user_model import CmdbUser
from cmdb.security.auth.auth_settings import AuthSettingsDAO
from cmdb.security.auth.auth_module import AuthModule
from cmdb.security.token.generator import TokenGenerator
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import (
    insert_request_user,
    check_db_exists,
    init_db_routine,
    set_admin_user,
    retrive_user,
    check_user_in_service_portal,
    verify_api_access,
)
from cmdb.interface.rest_api.responses import DefaultResponse, LoginResponse

from cmdb.errors.manager.users_manager import UsersManagerInsertError, UsersManagerGetError
from cmdb.errors.provider import AuthenticationProviderNotActivated, AuthenticationProviderNotFoundError
from cmdb.errors.security.security_errors import (
    AuthSettingsInitError,
    InvalidCloudUserError,
    NoAccessTokenError,
    RequestTimeoutError,
    RequestError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

auth_blueprint = APIBlueprint('auth', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@auth_blueprint.route('/login', methods=['POST'])
def post_login():
    """document"""
    #TODO: DOCUMENT-FIX
    login_data = request.json

    if not login_data:
        return abort(400, 'No valid JSON data was provided')

    request_user_name: str = login_data['user_name']
    request_password: str = login_data['password']
    request_subscription = None

    if 'subscription' in login_data:
        request_subscription = login_data['subscription']

    users_manager = UsersManager(current_app.database_manager)
    security_manager = SecurityManager(current_app.database_manager)

    try:
        if current_app.cloud_mode:
            request_user_name = request_user_name.lower()
            user_data = check_user_in_service_portal(request_user_name, request_password)
            # LOGGER.debug(f"[post_login] user_data: {user_data}")

            if not user_data:
                LOGGER.error("Could not retrieve User from ServicePortal!")
                return abort(401, 'Could not login')

            user_database = None

            # If only one subscription directly login the user
            if len(user_data['subscriptions']) == 1:
                # LOGGER.debug("[post_login] only 1 subscription")
                user_database = user_data['subscriptions'][0]['database']

                if not check_db_exists(user_database):
                    init_db_routine(user_database)

                set_admin_user(user_data, user_data['subscriptions'][0])

            # In this case the user selected a subscription in the frontend
            elif request_subscription:
                # LOGGER.debug(f"[post_login] subscription from frontend: {request_subscription}")
                user_database = request_subscription['database']

                if not check_db_exists(user_database):
                    init_db_routine(user_database)

                set_admin_user(user_data, request_subscription)
            # User have multiple subscriptions, send them to frontend to select
            elif len(user_data['subscriptions']) > 1:
                # LOGGER.debug(f"[post_login] multiple_subscriptions: {user_data['subscriptions']}")
                return DefaultResponse(user_data['subscriptions']).make_response()
            # There are either no subscriptions or something went wrong => failed path
            else:
                LOGGER.error("[post_login] Error: Invalid data. No subscriptions!")
                return abort(401, "Invalid data. Could not login!")

            user = retrive_user(user_data, user_database)

            # User does not exist
            if not user:
                LOGGER.error("[post_login] Could not retrieve User from database!")
                return abort(401, 'Could not login!')

            current_app.database_manager.connector.set_database(user_database)
            token, token_issued_at, token_expire = generate_token_with_params(user,
                                                                              current_app.database_manager,
                                                                              True)

            login_response = LoginResponse(user, token, token_issued_at, token_expire)

            return login_response.make_response()

    except HTTPException as http_err:
        raise http_err
    except NoAccessTokenError as err:
        LOGGER.error("[post_login] NoAccessTokenError: %s", err)
        return abort(500, "No access token found!")
    except InvalidCloudUserError as err:
        LOGGER.error("[post_login] %s", err)
        return abort(403, "Invalid credentials!")
    except RequestTimeoutError as err:
        LOGGER.error("[post_login] RequestTimeoutError: %s", err)
        return abort(500, "Login request timed out!")
    except RequestError as err:
        LOGGER.error("[post_login] %s", err)
        return abort(500, "Login failed due a malformed request!")
    except UsersManagerGetError as err:
        LOGGER.error("[post_login] UsersManagerGetError: %s", err)
        return abort(500, "Could not login because user can't be retrieved from database!")
    except UsersManagerInsertError as err:
        LOGGER.error("[post_login] UsersManagerInsertError: %s", err)
        return abort(500, "Could not login because user can't be inserted in database!")
    except Exception as err: #pylint: disable=broad-exception-caught
        LOGGER.error("[post_login] Exception: %s, Type: %s", err, type(err))
        return abort(500, "Could not login")

    #PATH when its not cloud mode
    settings_reader = SettingsReaderManager(current_app.database_manager)

    auth_module = AuthModule(
        settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__),
        security_manager=security_manager,
        users_manager=users_manager)

    user_instance = None

    try:
        user_instance = auth_module.login(request_user_name, request_password)

        if user_instance:
            token, token_issued_at, token_expire = generate_token_with_params(user_instance,
                                                                              current_app.database_manager)

            login_response = LoginResponse(user_instance, token, token_issued_at, token_expire)

            return login_response.make_response()

        return abort(401, 'Could not login!')
    except (AuthenticationProviderNotFoundError, AuthenticationProviderNotActivated):
        #TODO: ERROR-FIX
        return abort(503)
    except Exception as err: #pylint: disable=broad-exception-caught
        LOGGER.debug("[post_login] Exception: %s, Type: %s", err, type(err))
        return abort(500, "Could not login")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@auth_blueprint.route('/settings', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_auth_settings(request_user: CmdbUser):
    """document"""
    #TODO: DOCUMENT-FIX
    settings_reader: SettingsReaderManager = ManagerProvider.get_manager(ManagerType.SETTINGS_READER,
                                                                               request_user)

    auth_settings = settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__)
    auth_module = AuthModule(auth_settings)
    api_response = DefaultResponse(auth_module.settings)

    return api_response.make_response()


@auth_blueprint.route('/providers', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_installed_providers(request_user: CmdbUser):
    """document"""
    #TODO: DOCUMENT-FIX
    provider_names: list[dict] = []

    settings_reader: SettingsReaderManager = ManagerProvider.get_manager(ManagerType.SETTINGS_READER,
                                                                               request_user)

    auth_module = AuthModule(
        settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__))

    for provider in auth_module.providers:
        provider_names.append({'class_name': provider.get_name(), 'external': provider.EXTERNAL_PROVIDER})

    api_response = DefaultResponse(provider_names)

    return api_response.make_response()


@auth_blueprint.route('/providers/<string:provider_class>', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_provider_config(provider_class: str, request_user: CmdbUser):
    """document"""
    #TODO: DOCUMENT-FIX
    settings_reader: SettingsReaderManager = ManagerProvider.get_manager(ManagerType.SETTINGS_READER,
                                                                               request_user)

    auth_module = AuthModule(
        settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__))

    try:
        provider_class_config = auth_module.get_provider(provider_class).get_config()
    except StopIteration:
        return abort(404, 'Provider not found')

    api_response = DefaultResponse(provider_class_config)

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@auth_blueprint.route('/settings', methods=['POST', 'PUT'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@auth_blueprint.protect(auth=True, right='base.system.edit')
def update_auth_settings(request_user: CmdbUser):
    """document"""
    #TODO: DOCUMENT-FIX
    new_auth_settings_values = request.get_json()

    settings_reader: SettingsReaderManager = ManagerProvider.get_manager(ManagerType.SETTINGS_READER,
                                                                               request_user)
    settings_writer: SettingsWriterManager = ManagerProvider.get_manager(ManagerType.SETTINGS_WRITER,
                                                                               request_user)

    if not new_auth_settings_values:
        return abort(400, 'No new data was provided')

    try:
        new_auth_setting_instance = AuthSettingsDAO(**new_auth_settings_values)
    except AuthSettingsInitError as err:
        LOGGER.debug("[update_auth_settings] Error: %s", err)
        return abort(500, "Could not initialise auth settings!")

    update_result = settings_writer.write(_id='auth', data=new_auth_setting_instance.__dict__)

    if update_result.acknowledged:
        api_response = DefaultResponse(settings_reader.get_section('auth'))
        return api_response.make_response()

    return abort(400, 'Could not update auth settings')

# ------------------------------------------------------ HELPERS ----------------------------------------------------- #

def generate_token_with_params(
        login_user: CmdbUser,
        database_manager: MongoDatabaseManager,
        cloud_mode: bool = False) -> Tuple[bytes, int, int]:
    """document"""
    #TODO: DOCUMENT-FIX
    tg = TokenGenerator(database_manager)

    user_data = {'public_id': login_user.get_public_id()}

    if cloud_mode:
        user_data['database'] = login_user.get_database()

    token: bytes = tg.generate_token(payload={'user': user_data})

    token_issued_at = int(datetime.now(timezone.utc).timestamp())
    token_expire = int(tg.get_expire_time().timestamp())

    return token, token_issued_at, token_expire

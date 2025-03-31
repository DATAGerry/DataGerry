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
Implementation of helper methods for API routes
"""
import os
import base64
import functools
import json
import logging
from datetime import datetime, timezone
from typing import Union, Optional
import requests
from flask import request, abort, current_app
from werkzeug._internal import _wsgi_decoding_dance

from cmdb.manager import (
    UsersManager,
    GroupsManager,
    SecurityManager,
    SettingsReaderManager,
)

from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.auth_method_enum import AuthMethod
from cmdb.security.auth.auth_module import AuthModule
from cmdb.security.token.validator import TokenValidator
from cmdb.security.token.generator import TokenGenerator
from cmdb.models.isms_model import IsmsProtectionGoal, IsmsRiskMatrix
from cmdb.models.extendable_option_model import CmdbExtendableOption
from cmdb.models.isms_model.isms_helper import (
    get_default_protection_goals,
    get_default_risk_matrix,
    get_predefined_isms_extendable_options,
)
from cmdb.models.group_model import CmdbUserGroup
from cmdb.models.location_model.cmdb_location import CmdbLocation
from cmdb.models.user_model import CmdbUser
from cmdb.models.section_template_model.cmdb_section_template import CmdbSectionTemplate
from cmdb.models.reports_model.cmdb_report_category import CmdbReportCategory
from cmdb.models.user_management_constants import (
    __FIXED_GROUPS__,
    __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION,
)
from cmdb.framework.constants import __COLLECTIONS__ as FRAMEWORK_CLASSES

from cmdb.errors.security import (
    TokenValidationError,
    InvalidCloudUserError,
    NoAccessTokenError,
    RequestTimeoutError,
    RequestError,
)
from cmdb.errors.database import SetDatabaseError, DatabaseNotFoundError
from cmdb.errors.manager.users_manager import UsersManagerInsertError, UsersManagerGetError
from cmdb.errors.manager.groups_manager import GroupsManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

DEFAULT_MIME_TYPE = 'application/json'
SERVICE_PORTAL_AUTH_URL = "https://service.datagerry.com/api/datagerry/auth"
SERVICE_PORTAL_API_AUTH_URL = "https://service.datagerry.com/api/datagerry/auth/subscription"
SERVICE_PORTAL_SYNC_URL = "https://service.datagerry.com/api/datagerry/config-item/update"

# -------------------------------------------------------------------------------------------------------------------- #

def user_has_right(required_right: str, request_user: CmdbUser = None) -> bool:
    """Check if a user has a specific right"""
    # Check right for cloud api routes
    if request_user:
        return validate_right_cloud_api(required_right, request_user)

    # OpenSource check for rights
    with current_app.app_context():
        users_manager = UsersManager(current_app.database_manager)
        groups_manager = GroupsManager(current_app.database_manager)

    token = parse_authorization_header(request.headers['Authorization'])

    try:
        decrypted_token = TokenValidator(current_app.database_manager).decode_token(token)
    except TokenValidationError as err:
        LOGGER.debug("[user_has_right] Error: %s", err)
        abort(401, "Invalid token!")

    try:
        user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']

        if current_app.cloud_mode:
            database = decrypted_token['DATAGERRY']['value']['user']['database']
            users_manager = UsersManager(current_app.database_manager, database)
            groups_manager = GroupsManager(current_app.database_manager, database)

        user = users_manager.get_user(user_id)
        group = groups_manager.get_group(user.group_id)
        right_status = group.has_right(required_right)

        if not right_status:
            right_status = group.has_extended_right(required_right)

        return right_status

    except Exception:
        return False


#@deprecated
def insert_request_user(func):
    """
    Helper function which auto injects the user from the token request
    """
    @functools.wraps(func)
    def get_request_user(*args, **kwargs):
        # LOGGER.debug("insert_request_user() called")
        with current_app.app_context():
            users_manager = UsersManager(current_app.database_manager)
        try:
            # If the request comes from API then the request user will be set in verify_api_access - method
            if current_app.cloud_mode and "x-api-key" in request.headers:
                return func(*args, **kwargs)

            token = parse_authorization_header(request.headers['Authorization'])

            with current_app.app_context():
                decrypted_token = TokenValidator(current_app.database_manager).decode_token(token)
        except TokenValidationError:
            #TODO: ERROR-FIX
            abort(401)
        except Exception as err:
            LOGGER.debug("[insert_request_user] Token Exception: %s, Type: %s", err, type(err))
            abort(401)

        try:
            user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']

            if current_app.cloud_mode:
                database = decrypted_token['DATAGERRY']['value']['user']['database']
                users_manager = UsersManager(current_app.database_manager, database)

            user = users_manager.get_user(user_id)

            if user:
                kwargs.update({'request_user': user})
            else:
                abort(401, "Invalid user!")
        except ValueError:
            abort(401)
        except Exception as err:
            LOGGER.debug("[insert_request_user] User Exception: %s, Type: %s", err, type(err))
            abort(401)

        return func(*args, **kwargs)

    return get_request_user


def verify_api_access(*, required_api_level: ApiLevel = None):
    """document"""
    #TODO: DOCUMENT-FIX
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # LOGGER.debug("verify_api_access() called")
            if not current_app.cloud_mode:
                return func(*args, **kwargs)

            try:
                auth_method = __get_request_auth_method()
                api_user_dict = __get_request_api_user()
                x_api_key = __get_x_api_key()

                if auth_method == AuthMethod.BASIC:
                    user_instance = check_user_in_service_portal(api_user_dict['email'],
                                                                 api_user_dict['password'],
                                                                 x_api_key)

                    # Set the user as request User
                    if required_api_level != ApiLevel.SUPER_ADMIN:
                        set_admin_user(user_instance, user_instance['subscriptions'][0])
                        user_model = retrive_user(user_instance, user_instance['subscriptions'][0]['database'])

                        if user_model:
                            kwargs.update({'request_user': user_model})
                        else:
                            abort(403, "User not found!")

                    if not __check_api_level(user_instance, required_api_level):
                        abort(403, "No permission for this action!")
            except Exception as err:
                LOGGER.warning("[verify_api_access] Exception: %s", err)
                abort(400, "Invalid request!")

            return func(*args, **kwargs)
        return wrapper

    return decorator


def __get_x_api_key() -> Optional[str]:
    """
    Retrieve the 'x-api-key' from the request headers

    Returns:
        Optional[str]: The value of the 'x-api-key' header if present, otherwise None
    """
    x_api_key = request.headers.get('x-api-key')

    return x_api_key


def __get_request_api_user() -> Optional[dict[str, str]]:
    """Retrieve the API user credentials from the 'Authorization' request header

    Extracts and decodes the 'Authorization' header to obtain Basic Authentication credentials

    Returns:
        Optional[dict[str, str]]: A dictionary containing 'email' and 'password' if authentication is Basic
        Returns None if the header is missing, improperly formatted, or uses an unsupported authentication type
    """
    try:
        value = _wsgi_decoding_dance(request.headers['Authorization'])

        try:
            auth_type, auth_info = value.split(None, 1)
            auth_type = auth_type.lower()
        except ValueError:
            auth_type = b"bearer"
            auth_info = value

        if auth_type in (b"basic","basic"):
            email, password = base64.b64decode(auth_info).split(b":", 1)

            with current_app.app_context():
                return {'email': email.decode("utf-8"), 'password': password.decode("utf-8")}

        return None
    except Exception as err:
        LOGGER.error("[__get_request_api_user] User Exception: %s, Type: %s", err, type(err))
        return None


def __get_request_auth_method() -> Optional["AuthMethod"]:
    """
    Determine the authentication method from the request headers

    This function checks the 'Authorization' header to determine whether the request uses 
    Basic Authentication or JWT-based authentication

    Returns:
        Optional[AuthMethod]: 
            - `AuthMethod.BASIC` if the 'Authorization' header starts with 'Basic '
            - `AuthMethod.JWT` if the header starts with 'Bearer '
            - Aborts the request with a 400 error if the auth method is invalid or missing
    """
    try:
        auth_header = request.headers.get('Authorization')

        if auth_header:
            if auth_header.startswith('Basic '):
                return AuthMethod.BASIC

            if auth_header.startswith('Bearer '):
                return AuthMethod.JWT

        abort(400, "Invalid auth method!")
    except Exception as err:
        LOGGER.debug("[__get_request_auth_method] Exception: %s, Type: %s", err, type(err))
        abort(400, "Invalid auth method!")


def __check_api_level(user_instance: dict = None, required_api_level: ApiLevel = ApiLevel.NO_API) -> bool:
    """
    Check if the user has the required API access level

    This function verifies whether a user has the necessary API level permissions.
    The check is only performed in cloud mode

    Args:
        user_instance (dict, optional): A dictionary containing user details, including API level
        required_api_level (ApiLevel): The minimum API level required for access

    Returns:
        bool: 
            - `True` if the API level requirement is met or cloud mode is disabled
            - `False` if the user does not have the required API level or an error occurs
    """
    # Only validate in cloud mode
    if not current_app.cloud_mode:
        return True

    if not user_instance or required_api_level == ApiLevel.LOCKED:
        return False

    try:
        if required_api_level == ApiLevel.SUPER_ADMIN:
            return user_instance['api_level'] >= required_api_level

        return user_instance['subscriptions'][0]['api_level'] >= required_api_level
    except Exception as err:
        LOGGER.debug("[__check_api_level] Exception: %s, Type: %s", err, type(err))
        return False


#@deprecated
def right_required(required_right: str):
    """wraps function for routes which requires a special user right
    requires: insert_request_user
    """
    def _page_right(func):
        @functools.wraps(func)
        def _decorate(*args, **kwargs):
            try:
                groups_manager = GroupsManager(current_app.database_manager)

                current_user: CmdbUser = kwargs['request_user']
            except KeyError:
                abort(400, 'No request user was provided')
            try:
                if current_app.cloud_mode:
                    groups_manager = GroupsManager(current_app.database_manager, current_user.database)

                group: CmdbUserGroup = groups_manager.get_group(current_user.group_id)
                has_right = group.has_right(required_right)

                if not has_right and not group.has_extended_right(required_right):
                    abort(403, 'Request user does not have the right for this action!')
            except GroupsManagerGetError:
                abort(404, "Group or right does not exist!")
            except Exception:
                abort(403, "Could not verify authorisation with the provided data!")

            return func(*args, **kwargs)

        return _decorate

    return _page_right


def parse_authorization_header(header):
    """
    Parses the HTTP Auth Header to a JWT Token
    Args:
        header: Authorization header of the HTTP Request
    Examples:
        request.headers['Authorization'] or something same
    Returns:
        Valid JWT token
    """
    if not header:
        return None

    value = _wsgi_decoding_dance(header)

    try:
        auth_type, auth_info = value.split(None, 1)
        auth_type = auth_type.lower()
    except ValueError:
        # Fallback for old versions
        auth_type = b"bearer"
        auth_info = value

    if auth_type in (b"basic","basic"):
        try:
            username, password = base64.b64decode(auth_info).split(b":", 1)

            with current_app.app_context():
                username = username.decode("utf-8")
                password = password.decode("utf-8")

                if current_app.cloud_mode:
                    user_data = check_user_in_service_portal(username, password)

                    if not user_data:
                        return None

                    if current_app.local_mode:
                        # Test API only with user with 1 subscription
                        current_app.database_manager.connector.set_database(user_data['subscriptions'][0]['database'])
                    else:
                        current_app.database_manager.connector.set_database(user_data['database'])

                users_manager = UsersManager(current_app.database_manager)
                security_manager = SecurityManager(current_app.database_manager)
                settings_reader = SettingsReaderManager(current_app.database_manager)

                auth_settings = settings_reader.get_all_values_from_section('auth',
                                                                            AuthModule.__DEFAULT_SETTINGS__)
                auth_module = AuthModule(auth_settings,
                                         security_manager=security_manager,
                                         users_manager=users_manager)

                try:
                    user_instance = auth_module.login(username, password)
                except Exception:
                    return None

                if user_instance:
                    tg = TokenGenerator(current_app.database_manager)

                    token_payload = {
                                        'user': {
                                            'public_id': user_instance.get_public_id()
                                        }
                                    }

                    if current_app.cloud_mode:
                        token_payload['user']['database'] = user_instance.database
                        return tg.generate_token(payload=token_payload)

                    return tg.generate_token(payload=token_payload)

                return None
        except SetDatabaseError as err:
            LOGGER.error("[parse_authorization_header] SetDatabaseError: %s", err)
            return None
        except Exception as err:
            LOGGER.error("[parse_authorization_header] Exception: %s", err)
            return None

    if auth_type in ("bearer", b"bearer"):
        try:
            with current_app.app_context():
                tv = TokenValidator(current_app.database_manager)
                decoded_token = tv.decode_token(auth_info)
                tv.validate_token(decoded_token)

            return auth_info
        except Exception:
            return None

    return None

# ------------------------------------------------------ HELPER ------------------------------------------------------ #

def validate_right_cloud_api(required_right: str, request_user: CmdbUser) -> bool:
    """
    Validate whether the user has the required rights in a cloud-based API

    This function checks if the given user has the necessary permissions within their group.
    It first verifies if the user has the direct right and then checks for extended rights

    Args:
        required_right (str): The permission right to be validated
        request_user (CmdbUser): The user whose rights need to be validated

    Returns:
        bool: 
            - `True` if the user has the required right or an extended right
            - `False` if the user lacks the required permissions or an error occurs
    """
    with current_app.app_context():
        groups_manager = GroupsManager(current_app.database_manager, request_user.database)

    try:
        group = groups_manager.get_group(request_user.group_id)
        right_status = group.has_right(required_right)

        if not right_status:
            right_status = group.has_extended_right(required_right)

        return right_status
    except Exception as err:
        LOGGER.debug("[validate_right_cloud_api] Exception: %s, Type: %s", err, type(err))
        return False


# TODO: UNUSED-FIX
def validate_password(user_name: str, password: str, database: str = None) -> Union[CmdbUser, None]:
    """document"""
    #TODO: DOCUMENT-FIX
    if database:
        users_manager = UsersManager(current_app.database_manager, database)
        security_manager = SecurityManager(current_app.database_manager, database)
        settings_reader = SettingsReaderManager(current_app.database_manager, database)
    else:
        users_manager = UsersManager(current_app.database_manager)
        security_manager = SecurityManager(current_app.database_manager)
        settings_reader = SettingsReaderManager(current_app.database_manager)

    auth_settings = settings_reader.get_all_values_from_section('auth', AuthModule.__DEFAULT_SETTINGS__)
    auth_module = AuthModule(auth_settings,
                                security_manager=security_manager,
                                users_manager=users_manager)

    try:
        # Returns the CmdbUser
        return auth_module.login(user_name, password)
    except Exception:
        return None


def check_user_in_service_portal(mail: str, password: str, x_api_key: str = None) -> Optional[dict]:
    """Check if a user exists in the service portal

    This function verifies user credentials in two modes:
    - **Local mode**: Loads test users from a JSON file and verifies credentials
    - **Cloud mode**: Validates user credentials via the service portal

    Args:
        mail (str): The user's email address
        password (str): The user's password
        x_api_key (Optional[str], optional): An optional API key for authentication. Defaults to None

    Raises:
        NoAccessTokenError: If the service portal authentication fails due to a missing access token
        InvalidCloudUserError: If the user is invalid in the cloud authentication system
        RequestTimeoutError: If the authentication request times out
        RequestError: For general request failures
        Exception: For any other unexpected errors

    Returns:
        Optional[Dict]: A dictionary representing the user if authentication is successful, otherwise None
    """
    if current_app.local_mode:
        try:
            with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
                users_data = json.load(users_file)

                if mail in users_data:
                    user = users_data[mail]

                    if user["password"] == password:
                        return user

                return None
        except Exception as err:
            LOGGER.debug("[check_user_in_service_portal] Exception: %s, Type: %s", err, type(err))
            return None

    # Validation through service portal
    try:
        user_data = validate_subscrption_user(mail, password, x_api_key)

        return user_data
    except (NoAccessTokenError, InvalidCloudUserError, RequestTimeoutError, RequestError) as err:
        raise err from err
    except Exception as err:
        #TODO: ERROR-FIX (proper exception required)
        raise Exception(err) from err


def check_db_exists(db_name: str) -> bool:
    """
    This function checks if a given database name exists within the current database manager

    Args:
        db_name (str): The name of the database to check

    Returns:
        bool: True if the database exists, False otherwise
    """
    return current_app.database_manager.check_database_exists(db_name)


def init_db_routine(db_name: str) -> None:
    """
    Creates a database with the given name and all corresponding collections

    Args:
        `db_name` (str): Name of the database
    """
    new_db = current_app.database_manager.create_database(db_name)
    current_app.database_manager.connector.set_database(new_db.name)

    with current_app.app_context():
        groups_manager = GroupsManager(current_app.database_manager)

    # Generate framework collections
    for collection in FRAMEWORK_CLASSES:
        current_app.database_manager.create_collection(collection.COLLECTION)
        # set unique indexes
        current_app.database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())

    # Generate user management collections
    for collection in USER_MANAGEMENT_COLLECTION:
        current_app.database_manager.create_collection(collection.COLLECTION)
        # set unique indexes
        current_app.database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())

    # Generate groups
    for group in __FIXED_GROUPS__:
        groups_manager.insert_group(group)

    # Generate the root location
    current_app.database_manager.set_root_location(CmdbLocation.COLLECTION, create=True)
    LOGGER.info("Created 'Root'-Location!")

    # Generate predefined section templates
    current_app.database_manager.init_predefined_templates(CmdbSectionTemplate.COLLECTION)

    # Generate 'General' report category
    current_app.database_manager.create_general_report_category(CmdbReportCategory.COLLECTION)

    # Create the default IsmsProtectionGoals
    default_protection_goals = get_default_protection_goals()

    for protection_goal in default_protection_goals:
        current_app.database_manager.insert(IsmsProtectionGoal.COLLECTION, protection_goal)
        LOGGER.info("Created ProtectionGoal '%s'!", protection_goal['name'])

    # Create the default IsmsRiskMatrix
    current_app.database_manager.insert(IsmsRiskMatrix.COLLECTION, get_default_risk_matrix())
    LOGGER.info("Created default RiskMatrix!")

    predefined_isms_options = get_predefined_isms_extendable_options()

    for predefined_isms_option in predefined_isms_options:
        current_app.database_manager.insert(CmdbExtendableOption.COLLECTION, predefined_isms_option)
        LOGGER.info("Created ISMS Option: '%s'!", predefined_isms_option['value'])


def set_admin_user(user_data: dict, subscription: dict):
    """Creates a new admin user"""
    with current_app.app_context():
        current_app.database_manager.connector.set_database(subscription['database'])
        users_manager = UsersManager(current_app.database_manager)
        scm = SecurityManager(current_app.database_manager)

    try:
        admin_user_from_db = None

        try:
            admin_user_from_db = users_manager.get_user_by({'email': user_data['email']})
        except UsersManagerGetError:
            pass

        if not admin_user_from_db:
            admin_user = CmdbUser(
                public_id = users_manager.get_next_public_id(),
                user_name = user_data['user_name'],
                email = user_data['email'],
                database = subscription['database'],
                active = True,
                api_level = int(subscription['api_level']),
                config_items_limit = int(subscription['config_item_limit']),
                group_id = 1,
                registration_time = datetime.now(timezone.utc),
                password = scm.generate_hmac(user_data['password']),
            )

            users_manager.insert_user(admin_user)
        else: # Update the database, api-level and config_items_limit of user
            admin_user_from_db.api_level = subscription['api_level']
            admin_user_from_db.database = subscription['database']
            admin_user_from_db.config_items_limit = subscription['config_item_limit']

            users_manager.update_user(admin_user_from_db.get_public_id(), admin_user_from_db)

    except UsersManagerGetError as err:
        raise UsersManagerGetError(err) from err
    except UsersManagerInsertError as err:
        raise UsersManagerInsertError(err) from err
    except Exception as err:
        LOGGER.debug("[set_admin_user] Exception: %s, Type: %s", err, type(err))
        raise UsersManagerInsertError(err) from err


def retrive_user(user_data: dict, database: str) -> Optional[dict]:
    """
    Retrieve a user from the database by email

    This function fetches a user from the database using the provided email from the user data

    Args:
        user_data (dict[str, str]): A dictionary containing user information (e.g., email)
        database (str): The name of the database to query

    Returns:
        Optional[dict]: A dictionary representing the user if found, or None if an error occurs
    """
    with current_app.app_context():
        users_manager = UsersManager(current_app.database_manager, database)

    try:
        return users_manager.get_user_by({'email': user_data['email']})
    except UsersManagerGetError as err:
        LOGGER.debug("[retrive_user] Exception: %s, Type: %s", err, type(err))
        return None


def delete_database(db_name: str) -> None:
    """
    Delete the specified database

    This function attempts to delete the database with the given name. It sets the appropriate database 
    in the database manager and then drops it using the `UsersManager`

    Args:
        db_name (str): The name of the database to be deleted

    Raises:
        DatabaseNotFoundError: If the database cannot be found or deleted
    """
    try:
        with current_app.app_context():
            current_app.database_manager.connector.set_database(db_name)
            users_manager = UsersManager(current_app.database_manager)

            users_manager.dbm.drop_database(db_name)
    except Exception as err:
        LOGGER.debug("[delete_database] Exception: %s, Type:%s", err, type(err))
        raise DatabaseNotFoundError(db_name) from err


def validate_subscrption_user(email: str, password: str, x_api_key: str = None) -> dict:
    """
    Validates the user credentials
    """
    x_access_token = os.getenv("X-ACCESS-TOKEN")

    if not x_access_token:
        raise NoAccessTokenError("No x-access-token provided!")

    headers = {
        "x-access-token": x_access_token
    }

    target = SERVICE_PORTAL_AUTH_URL

    payload = {
        "email": email,
        "password": password
    }

    if x_api_key:
        payload['x-api-key'] = x_api_key

        target = SERVICE_PORTAL_API_AUTH_URL

    try:
        response = requests.post(target, headers=headers, json=payload, timeout=3)

        if response.status_code == 200:
            return response.json()

        raise InvalidCloudUserError(response.json()['message'])
    except requests.exceptions.Timeout as err:
        raise RequestTimeoutError(err) from err
    except requests.exceptions.RequestException as err:
        raise RequestError(err) from err


def sync_config_items(email: str, database: str, config_item_count: int) -> bool:
    """
    Synchronize configuration items with the service portal

    This function sends a request to the service portal to sync configuration items for a specific 
    user and database. It is only executed in cloud mode. If the mode is local, the function simply 
    returns `True`

    Args:
        email (str): The email of the user
        database (str): The name of the database
        config_item_count (int): The number of configuration items to sync

    Returns:
        bool: 
            - `True` if the synchronization was successful
            - `False` if the request failed or an error occurred

    Raises:
        NoAccessTokenError: If the `X-ACCESS-TOKEN` environment variable is not set
    """
    # Just do this in cloud mode
    if current_app.local_mode:
        return True

    x_access_token = os.getenv("X-ACCESS-TOKEN")

    if not x_access_token:
        raise NoAccessTokenError("No x-access-token provided!")

    headers = {
        "x-access-token": x_access_token
    }

    payload = {
        "email": email,
        "database_name": database,
        "config_item_count": config_item_count
    }

    try:
        response = requests.post(SERVICE_PORTAL_SYNC_URL, headers=headers, json=payload, timeout=3)

        if response.status_code == 200:
            return True

        return False
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as err:
        LOGGER.error("[sync_config_items] Request Error: %s. Type: %s", err, type(err))
        return False

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
from typing import Optional
import time
import requests
from flask import request, abort, current_app
from werkzeug._internal import _wsgi_decoding_dance

from pymongo.errors import NetworkTimeout, AutoReconnect

from cmdb.database.database_services import CollectionValidator, DatabaseUpdater
from cmdb.manager import (
    UsersManager,
    GroupsManager,
    SecurityManager,
    SettingsManager,
)

from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.auth_method_enum import AuthMethod
from cmdb.security.auth.auth_module import AuthModule
from cmdb.security.token.validator import TokenValidator
from cmdb.security.token.generator import TokenGenerator

from cmdb.models.group_model import CmdbUserGroup
from cmdb.models.user_model import CmdbUser

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

# -------------------------------------------------------------------------------------------------------------------- #

def user_has_right(required_right: str, request_user: CmdbUser = None) -> bool:
    """
    Determine whether a user has the specified access right

    This function checks whether the user has the given `required_right` either via:
    - A provided `CmdbUser` object (typically used in cloud API contexts), or
    - A token extracted from the request's Authorization header in non-cloud or Open Source mode

    The function supports both basic and extended rights and includes handling for token validation
    and user/group resolution based on application mode (cloud or local).

    Args:
        required_right (str): The permission/right to verify
        request_user (CmdbUser, optional): The user object (if already available). If not provided,
                                           the user will be determined via the Authorization token

    Returns:
        bool: True if the user has the required right (or extended right), False otherwise

    Raises:
        Exception: If the token is missing or invalid (401 Unauthorized)
    """
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


def insert_request_user(func):
    """
    Decorator that injects the authenticated user into a route handler as `request_user`

    This decorator handles token extraction and validation from the `Authorization` header,
    retrieves the user based on the token contents, and adds the `request_user` keyword argument
    to the wrapped function. It supports both cloud and non-cloud modes

    In cloud mode, requests with an `x-api-key` header are assumed to have already been authenticated
    via a different mechanism and are passed through without further token validation

    Args:
        func (Callable): The route function to decorate

    Returns:
        Callable: The wrapped function with `request_user` injected, if authentication succeeds

    Raises:
        werkzeug.exceptions.HTTPException: Returns a 401 Unauthorized error if token validation fails
                                           or the user cannot be resolved.
    """
    @functools.wraps(func)
    def get_request_user(*args, **kwargs):
        with current_app.app_context():
            users_manager = UsersManager(current_app.database_manager)
        try:
            # If the request comes from API then the request_user will be set in verify_api_access - method
            if current_app.cloud_mode and "x-api-key" in request.headers:
                return func(*args, **kwargs)

            token = parse_authorization_header(request.headers['Authorization'])

            with current_app.app_context():
                decrypted_token = TokenValidator(current_app.database_manager).decode_token(token)
        except TokenValidationError:
            abort(401, "Invalid Token!")
        except Exception as err:
            LOGGER.debug("[insert_request_user] Exception: %s, Type: %s", err, type(err), exc_info=True)
            abort(401, "Token could not be validated!")

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
    """
    Decorator to verify API access based on authentication method and required API level

    Args:
        required_api_level (ApiLevel, optional): Minimum API access level required to execute the decorated function
    
    Behavior:
    - If the user does not meet the required API level, the request is aborted with a 403 status
    - If authentication fails or an error occurs, the request is aborted with a 400 status

    Returns:
        function: A decorated function with API access control
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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
                LOGGER.error("[verify_api_access] Exception: %s. Type: %s", err, type(err), exc_info=True)
                abort(400, "Failed to verify API access!")

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

                db_name = None
                if current_app.cloud_mode:
                    user_data = check_user_in_service_portal(username, password)

                    if not user_data:
                        return None

                    if current_app.local_mode:
                        # Test API only with user with 1 subscription
                        db_name = user_data['subscriptions'][0]['database']
                    else:
                        db_name = user_data['database']

                users_manager = UsersManager(current_app.database_manager, db_name)
                security_manager = SecurityManager(current_app.database_manager, db_name)
                settings_manager = SettingsManager(current_app.database_manager, db_name)

                auth_settings = settings_manager.get_all_values_from_section('auth', AuthModule.__DEFAULT_SETTINGS__)
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
        db_name (str): Name of the database
    """
    # Initialise the database
    collection_validator = CollectionValidator(db_name, current_app.database_manager)
    collection_validator.validate_collections()

    # Sets the update version to the newest version
    database_updater = DatabaseUpdater(current_app.database_manager, db_name)
    database_updater.set_update_version(database_updater.get_highest_update_version())


def set_admin_user(user_data: dict, subscription: dict):
    """Creates a new admin user"""
    with current_app.app_context():
        users_manager = UsersManager(current_app.database_manager, subscription['database'])
        scm = SecurityManager(current_app.database_manager, subscription['database'])

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
            users_manager = UsersManager(current_app.database_manager, db_name)

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

    target = os.getenv('SP_AUTH_URL')

    payload = {
        "email": email,
        "password": password
    }

    if x_api_key:
        payload['x-api-key'] = x_api_key

        target = os.getenv('SP_API_AUTH_URL')

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

    target = os.getenv('SP_CI_SYNC_URL')

    try:
        response = requests.post(target, headers=headers, json=payload, timeout=3)

        if response.status_code == 200:
            return True

        return False
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as err:
        LOGGER.error("[sync_config_items] Request Error: %s. Type: %s", err, type(err))
        return False


def mongo_retry(retries=3, delay=2):
    """
    Decorator to retry MongoDB operations in case of transient errors.
    
    Args:
        retries (int): Number of retries
        delay (int): Seconds between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except (NetworkTimeout, AutoReconnect) as e:
                    last_exception = e
                    time.sleep(delay)
            # After retries exhausted
            raise last_exception
        return wrapper
    return decorator

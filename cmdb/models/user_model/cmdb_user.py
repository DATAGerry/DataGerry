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
Represents a Cmdbuser in DataGerry
"""
import logging

from datetime import datetime, timezone
from dateutil.parser import parse

from cmdb.class_schema.cmdb_user_schema import get_cmdb_user_schema
from cmdb.models.cmdb_dao import CmdbDAO

from cmdb.errors.models.cmdb_user import (
    CmdbUserInitError,
    CmdbUserInitFromDataError,
    CmdbUserToJsonError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   CmdbUser - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class CmdbUser(CmdbDAO):
    """
    Implementation of a CmdbUser in DataGerry

    Extends: CmdbDAO
    """
    COLLECTION = 'management.users'
    MODEL = 'User'
    INDEX_KEYS = [
        {
            'keys': [('user_name', CmdbDAO.DAO_ASCENDING)],
            'name': 'user_name',
            'unique': True
        }
    ]

    DEFAULT_AUTHENTICATOR: str = 'LocalAuthenticationProvider'
    DEFAULT_GROUP: int = 2
    DEFAULT_API_LEVEL = 0
    DEFAULT_CONFIG_ITEMS_LIMIT = 1000

    SCHEMA: dict = get_cmdb_user_schema()

    #pylint: disable=too-many-arguments
    def __init__(self,
                 public_id: int,
                 user_name: str,
                 active: bool,
                 group_id: int = None,
                 registration_time: datetime = None,
                 password: str = None,
                 database: str = 'test',
                 api_level: int = 0,
                 config_items_limit: int = 1000,
                 image: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 email: str = None,
                 authenticator: str = None):
        """
        Initializes a CmdbUser

        Args:
            public_id (int): Unique identifier for the CmdbUser
            user_name (str): Username of the CmdbUser
            active (bool): Indicates if the CmdbUser is active
            group_id (int, optional): public_id of the CmdbUser's CmdbUserGroup. Defaults to None
            registration_time (datetime, optional):When the CmdbUser was created
            password (str, optional): CmdbUser's password
            database (str, optional): Name of the database the user belongs to. Defaults to 'test'
            api_level (int, optional): API access level of the CmdbUser. Defaults to 0
            config_items_limit (int, optional): Limit of configuration items. Defaults to 1000
            image (str, optional): URL or path to the CmdbUser's profile image. Defaults to None
            first_name (str, optional): First name of the CmdbUser. Defaults to None
            last_name (str, optional): Last name of the CmdbUser. Defaults to None
            email (str, optional): Email address of the CmdbUser. Defaults to None
            authenticator (str, optional): Authentication method for the CmdbUser. Defaults to a default authenticator

        Raises:
            CmdbUserInitError: WHen the initialisation of CmdbUser fails
        """
        try:
            self.user_name = user_name
            self.active = active
            self.group_id = group_id or CmdbUser.DEFAULT_GROUP
            self.authenticator = authenticator or CmdbUser.DEFAULT_AUTHENTICATOR
            self.registration_time = registration_time or datetime.now(timezone.utc)
            self.database = database
            self.api_level = api_level
            self.config_items_limit = config_items_limit
            self.email = email
            self.password = password
            self.image = image
            self.first_name = first_name or None
            self.last_name = last_name or None

            super().__init__(public_id=public_id)
        except Exception as err:
            raise CmdbUserInitError(err) from err


    def __str__(self) -> str:
        """
        Returns a string representation of the CmdbUser

        The output includes key attributes such as public_id, email,
        user_name, group_id, authenticator, and database.

        Returns:
            str: A formatted string representing the CmdbUser
        """
        return (
            f"User(\n"
            f"public_id: {self.public_id},\n"
            f"email: {self.email},\n"
            f"user_name: {self.user_name},\n"
            f"group_id: {self.group_id},\n"
            f"authenticator: {self.authenticator},\n"
            f"database: {self.database}\n"
            f")"
        )

# --------------------------------------------------- CLASS METHODS -------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "CmdbUser":
        """
        Initialises a CmdbUser from a dict

        Args:
            data (dict): Data with which the CmdbUser should be initialised

        Raises:
            CmdbUserInitFromDataError: If the initialisation with the given data fails

        Returns:
            CmdbUser: CmdbUser with the given data
        """
        try:
            reg_date = data.get('registration_time')

            if reg_date and isinstance(reg_date, str):
                reg_date = parse(reg_date, fuzzy=True)

            return cls(
                public_id = data.get('public_id'),
                user_name = data.get('user_name'),
                active = data.get('active'),
                database = data.get('database'),
                api_level = data.get('api_level', 0),
                config_items_limit = data.get('config_items_limit', 1000),
                group_id = data.get('group_id'),
                registration_time = reg_date,
                authenticator = data.get('authenticator'),
                email = data.get('email'),
                password = data.get('password'),
                image = data.get('image'),
                first_name = data.get('first_name'),
                last_name = data.get('last_name')
            )
        except Exception as err:
            raise CmdbUserInitFromDataError(err) from err


    @classmethod
    def to_json(cls, instance: "CmdbUser") -> dict:
        """
        Converts a CmdbUser into a json compatible dict

        Args:
            instance (CmdbUser): The CmdbUser which should be converted

        Raises:
            CmdbUserToJsonError: If the CmdbUser could not be converted to a json compatible dict

        Returns:
            dict: Json compatible dict of the CmdbUser values
        """
        try:
            return {
                'public_id': instance.public_id,
                'user_name': instance.user_name,
                'active': instance.active,
                'group_id': instance.group_id,
                'registration_time': instance.registration_time,
                'authenticator': instance.authenticator,
                'database': instance.database,
                'api_level': instance.api_level,
                'config_items_limit': instance.config_items_limit,
                'email': instance.email,
                'password': instance.password,
                'image': instance.image,
                'first_name': instance.first_name,
                'last_name': instance.last_name
            }
        except Exception as err:
            raise CmdbUserToJsonError(err) from err

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

    def get_database(self) -> str:
        """
        Retrives the database name of the CmdbUser

        Returns:
            str: Name of the database
        """
        return self.database


    def get_display_name(self) -> str:
        """
        Get the display name of the CmdbUser

        Returns:
            str: Display name of the CmdbUser
        """
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

        return self.user_name

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
This module contains the implementation of the UsersManager
"""
import logging
from typing import Union

from cmdb.database import MongoDatabaseManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.base_manager import BaseManager

from cmdb.models.user_model import CmdbUser
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import (
    ManagerDeleteError,
    ManagerGetError,
)
from cmdb.errors.manager.users_manager import (
    UsersManagerGetError,
    UsersManagerInsertError,
    UsersManagerDeleteError,
    UsersManagerUpdateError,
    UsersManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 UsersManager - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class UsersManager(BaseManager):
    """
    The UsersManager handles the interaction between the CmdbUsers-API and the database
    `Extends`: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the UsersManager

        Args:
            `dbm` (MongoDatabaseManager): Database interaction manager
            `database` (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE
        """
        if database:
            dbm.connector.set_database(database)

        super().__init__(CmdbUser.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_user(self, user: Union[CmdbUser, dict]) -> int:
        """
        Insert a single CmdbUser into the database

        Args:
            `user` (dict): Raw data of the CmdbUser

        Raises:
            `UsersManagerInsertError`: When the CmdbUser could not be inserted in the database
        Returns:
            `int`: The public_id of the created CmdbUser
        """
        #TODO: ERROR-FIX (try-catch block)
        try:
            if isinstance(user, CmdbUser):
                user = CmdbUser.to_data(user)

            return self.insert(user)
        except Exception as err: #TODO: ERROR-FIX(refactor when also catching the instance check)
            raise UsersManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_user(self, public_id: int) -> CmdbUser:
        """
        Retrieve a single CmdbUser by its public_id

        Args:
            `public_id` (int): public_id of the CmdbUser

        Raises:
            `UsersManagerGetError`: When CmdbUser could not be retrieved

        Returns:
            `CmdbUser`: The requested CmdbUser
        """
        try:
            requested_user = self.get_one(public_id)
        except ManagerGetError as err:
            raise UsersManagerGetError(err) from err

        #TODO: ERROR-FIX (try catch block)
        if requested_user:
            return CmdbUser.from_data(requested_user)

        raise UsersManagerGetError("User not found!")


    def get_user_by(self, query: dict) -> CmdbUser:
        """
        Get a single CmdbUser by a query

        Args:
            `query` (dict): Query filter of CmdbUser parameters

        Raises:
            `UsersManagerGetError`: When the CmdbUser could not be retrieved

        Returns:
            `CmdbUser`: CmdbUser matching the query
        """
        try:
            result = self.get(filter=query, limit=1)
            resource_result = next(iter(result.limit(-1)), None)

            if resource_result is None:
                raise UsersManagerGetError(f"No user found for query: {query}")

            return CmdbUser.from_data(resource_result)
        except Exception as err:
            raise UsersManagerGetError(err) from err


    def get_many_users(self, query: list = None) -> list[CmdbUser]:
        """
        Get multiple CmdbUsers by a query. Passing no query means all users

        Args:
            `query` (dict): A database query for filtering
        Raises:
            `UsersManagerGetError`: Raised when CmdbUsers cant be retrieved or not transformed into CmdbUser
        Returns:
            `list[CmdbUser]`: A list of all users which matches the query
        """
        query = query or {}

        try:
            results = self.get(filter=query)

            #TODO: ERROR-FIX (Specific error catch)
            return [CmdbUser.from_data(user) for user in results]
        except Exception as err:
            LOGGER.debug("[get_many_users] Error: %s, Type: %s", err, type(err))
            raise UsersManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbUser]:
        """
        Iterate CmdbUsers

        Args:
            `builder_params` (BuilderParameters): Filter for iteration

        Raises:
            UsersManagerIterationError: When the iteration failed
        Returns:
            `IterationResult`: IterationResult with CmdbUsers matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            #TODO: ERROR-FIX(IterationResult error catch)
            iteration_result: IterationResult[CmdbUser] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbUser)
        except Exception as err:
            raise UsersManagerIterationError(err) from err

        return iteration_result

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_user(self, public_id: int, user_data: Union[CmdbUser, dict]) -> None:
        """
        Update an existing CmdbUser

        Args:
            `public_id` (int): public_id of the CmdbUser
            `user(CmdbUser/dict)`: Instance or dict of CmdbUser

        Raises:
            `UsersManagerUpdateError`: When the CmdbUser could not be updated
        """
        try:
            #TODO: ERROR-FIX (Create error for this)
            if isinstance(user_data, CmdbUser):
                user_data = CmdbUser.to_dict(user_data)

            self.update(criteria={'public_id': public_id}, data=user_data)
        except Exception as err:
            raise UsersManagerUpdateError(err) from err


# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_user(self, public_id: int) -> CmdbUser:
        """
        Delete an existing CmdbUser with the given public_id

        Args:
            `public_id` (int): PublicID of the user

        Raises:
            `UsersManagerDeleteError`: When trying to delete the admin CmdbUser with public_id=1
            `UsersManagerDeleteError`: When the CmdbUser could not be deleted
            `UsersManagerGetError`: When CmdbUser which should be deleted could not be retrieved
            `UsersManagerGetError`: When no CmdbUser matches the public_id

        Returns:
            `CmdbUser`: Model of the deleted user
        """
        if public_id == 1:
            raise UsersManagerDeleteError("You can't delete the admin user")

        try:
            user = self.get_user(public_id)
        except UsersManagerGetError as err:
            raise UsersManagerGetError(f"Could not retrieve user with ID: {public_id}") from err

        try:
            if not self.delete({'public_id': public_id}):
                raise UsersManagerGetError(f"No user matched the public_id: {public_id}")

        except ManagerDeleteError as err:
            raise UsersManagerDeleteError(f"Could not delete user with ID: {public_id}") from err

        return user

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
"""TODO: document"""
import logging
from typing import Union

from cmdb.database import MongoDatabaseManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager import BaseManager

from cmdb.models.right_model.all_rights import flat_rights_tree, __all__ as rights
from cmdb.models.group_model import CmdbUserGroup
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import ManagerUpdateError, ManagerDeleteError
from cmdb.errors.manager.groups_manager import (
    GroupsManagerInsertError,
    GroupsManagerGetError,
    GroupsManagerIterationError,
    GroupsManagerUpdateError,
    GroupsManagerDeleteError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 GroupsManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class GroupsManager(BaseManager):
    """
    The GroupsManager handles the interaction between the CmdbUserGroup-API and the database
    `Extends`: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager = None, database :str = None):
        """
        Set the database connection for the GroupsManager

        Args:
            `dbm` (MongoDatabaseManager): Database interaction manager
            `database` (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE
        """
        self.rights = flat_rights_tree(rights)

        if database:
            dbm.connector.set_database(database)

        super().__init__(CmdbUserGroup.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_group(self, group: Union[CmdbUserGroup, dict]) -> int:
        """
        Insert a single CmdbUserGroup into the database

        Args:
            `group` (CmdbUserGroup / dict): data of the CmdbUserGroup which should be created

        Raises:
            `GroupsManagerInsertError`: When the CmdbUserGroup could not be inserted

        Returns:
            `int`: The public_id of the new inserted CmdbUserGroup
        """
        try:
            if isinstance(group, CmdbUserGroup):
                group = CmdbUserGroup.to_data(group)

            return self.insert(group)
        except Exception as err:
            raise GroupsManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_group(self, public_id: int) -> CmdbUserGroup:
        """
        Get a single CmdbUserGroup by its public_id

        Args:
            `public_id` (int): ID of the group.

        Raises:
            `GroupsManagerGetError`: When the requested group could not be retrieved

        Returns:
            `CmdbUserGroup`: The requested CmdbUserGroup
        """
        try:
            requested_group = self.get_one(public_id)

            return CmdbUserGroup.from_data(requested_group, self.rights)
        #TODO: ERROR-FIX (catch init errors)
        except Exception as err:
            raise GroupsManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbUserGroup]:
        """
        Retrieve multiple CmdbUserGroups

        Args:
            `builder_params` (BuilderParameters): Filter for which CmdbUserGroups should be retrieved

        Raises:
            `GroupsManagerIterationError`: When the iteration failed

        Returns:
            `IterationResult[CmdbUserGroup]`: All CmdbUserGroups matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            iteration_result: IterationResult[CmdbUserGroup] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbUserGroup)

            return iteration_result
        #TODO: ERROR-FIX (catch init errors)
        except Exception as err:
            raise GroupsManagerIterationError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_group(self, public_id: int, group: Union[CmdbUserGroup, dict]) -> None:
        """
        Update an existing CmdbUserGroup in the database

        Args:
            `public_id` (int): public_id of the CmdbUserGroup which should be updated
            `group` (CmdbUserGroup / dict): New data for the CmdbUserGroup

        Raises:
            `GroupsManagerUpdateError`: When no CmdbUserGroup matches the input
            `GroupsManagerUpdateError`: When multiple CmdbUserGroups matched the input
            `GroupsManagerUpdateError`: When the update operation failed
        """
        try:
            update_result = self.update(criteria={'public_id': public_id}, data=group)

            if update_result.matched_count == 0:
                raise GroupsManagerUpdateError('No CmdbUserGroup matches the input!')
            if update_result.matched_count > 1:
                raise GroupsManagerUpdateError('More than one CmdbUserGroup matched the input!')
        except ManagerUpdateError as err:
            raise GroupsManagerUpdateError(err) from err
        #TODO: ERROR-FIX (catch init errors, handle multiple or no matches)
        except Exception as err:
            raise GroupsManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_group(self, public_id: int) -> CmdbUserGroup:
        """
        Delete an existing CmdbUserGroup by its public_id

        Args:
            `public_id` (int): public_id of the CmdbUserGroup which should be deleted

        Raises:
            `ManagerDeleteError`: If you try to delete the Admin or User CmdbUserGroup
            `ManagerDeleteError`: Could not retrieve the CmdbUserGroup which should be deleted
            `ManagerDeleteError`: When the delete operation failed

        Returns:
            `bool`: True if the deletion succeded
        """
        try:
            if public_id in [1, 2]:
                raise GroupsManagerDeleteError(f'Deletion Group with ID: {public_id} is not allowed!')

            group = self.get_group(public_id)

            self.delete({'public_id': public_id})

            return group
        except GroupsManagerGetError as err:
            raise GroupsManagerDeleteError(err) from err
        except ManagerDeleteError as err:
            raise GroupsManagerDeleteError(err) from err
        except Exception as err:
            raise GroupsManagerDeleteError(err) from err

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
This module contains the implementation of the ObjectGroupsManager
"""
import logging
from typing import Optional, Union

from cmdb.database import MongoDatabaseManager

from cmdb.manager.base_manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.object_group_model import CmdbObjectGroup

from cmdb.framework.results import IterationResult

from cmdb.errors.models.cmdb_object_group import (
    CmdbObjectGroupToJsonError,
)
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
    BaseManagerIterationError,
)
from cmdb.errors.manager.object_groups_manager import (
    ObjectGroupsManagerInitError,
    ObjectGroupsManagerInsertError,
    ObjectGroupsManagerGetError,
    ObjectGroupsManagerUpdateError,
    ObjectGroupsManagerDeleteError,
    ObjectGroupsManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              ObjectGroupsManager - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectGroupsManager(BaseManager):
    """
    The ObjectGroupsManager manages the interaction between CmdbObjectGroups and the database

    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the ObjectGroupsManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            ObjectGroupsManagerInitError: If the ObjectGroupsManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(CmdbObjectGroup.COLLECTION, dbm)
        except Exception as err:
            raise ObjectGroupsManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_object_group(self, object_group: dict) -> int:
        """
        Insert an CmdbObjectGroup into the database

        Args:
            object_group (dict): Raw data of the CmdbObjectGroup

        Raises:
            ObjectGroupsManagerInsertError: When an CmdbObjectGroup could not be inserted into the database

        Returns:
            int: The public_id of the created CmdbObjectGroup
        """
        try:
            if isinstance(object_group, CmdbObjectGroup):
                object_group = CmdbObjectGroup.to_json(object_group)

            return self.insert(object_group)
        except (BaseManagerInsertError, CmdbObjectGroupToJsonError) as err:
            raise ObjectGroupsManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_object_group] Exception: %s. Type: %s", err, type(err))
            raise ObjectGroupsManagerInsertError(err) from err


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_object_group(self, public_id: int) -> Optional[dict]:
        """
        Retrieves an CmdbObjectGroup from the database

        Args:
            public_id (int): public_id of the CmdbObjectGroup

        Raises:
            ObjectGroupsManagerGetError: When an CmdbObjectGroup could not be retrieved

        Returns:
            Optional[dict]: A dictionary representation of the CmdbObjectGroup if successful, otherwise None
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise ObjectGroupsManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbObjectGroup]:
        """
        Retrieves multiple CmdbObjectGroups

        Args:
            builder_params (BuilderParameters): Filter for which CmdbObjectGroups should be retrieved

        Raises:
            ObjectGroupsManagerIterationError: When the iteration failed

        Returns:
            IterationResult[CmdbObjectGroup]: All CmdbObjectGroups matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            result: IterationResult[CmdbObjectGroup] = IterationResult(aggregation_result,
                                                                          total,
                                                                          CmdbObjectGroup)

            return result
        except BaseManagerIterationError as err:
            raise ObjectGroupsManagerIterationError(err) from err
        except Exception as err:
            LOGGER.error("[iterate] Exception: %s. Type: %s", err, type(err))
            raise ObjectGroupsManagerIterationError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_object_group(self, public_id:int, data: Union[CmdbObjectGroup, dict]) -> None:
        """
        Updates an CmdbObjectGroup in the database

        Args:
            public_id (int): public_id of the CmdbObjectGroup which should be updated
            data: Union[CmdbObjectGroup, dict]: The new data for the CmdbObjectGroup

        Raises:
            ObjectGroupsManagerUpdateError: When the update operation fails
        """
        try:
            if isinstance(data, CmdbObjectGroup):
                data = CmdbObjectGroup.to_json(data)

            self.update({'public_id':public_id}, data)
        except (BaseManagerUpdateError, CmdbObjectGroupToJsonError) as err:
            raise ObjectGroupsManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_object_group] Exception: %s. Type: %s", err, type(err))
            raise ObjectGroupsManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_object_group(self, public_id: int) -> bool:
        """
        Deletes an CmdbObjectGroup from the database

        Args:
            public_id (int): public_id of the CmdbObjectGroup which should be deleted

        Raises:
            ObjectGroupsManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise ObjectGroupsManagerDeleteError(err) from err

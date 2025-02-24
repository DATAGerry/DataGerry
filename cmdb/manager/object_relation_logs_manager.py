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
This module contains the implementation of the ObjectRelationLogsManager
"""
import logging
from typing import Optional

from cmdb.database import MongoDatabaseManager

from cmdb.manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.log_model import CmdbObjectRelationLog
from cmdb.models.user_model import CmdbUser

from cmdb.framework.results import IterationResult
from cmdb.security.acl.permission import AccessControlPermission

from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerIterationError,
    BaseManagerDeleteError,
)
from cmdb.errors.manager.object_relation_logs_manager import (
    ObjectRelationLogsManagerInitError,
    ObjectRelationLogsManagerInsertError,
    ObjectRelationLogsManagerGetError,
    ObjectRelationLogsManagerIterationError,
    ObjectRelationLogsManagerDeleteError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                           ObjectRelationLogsManager - CLASS                                          #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectRelationLogsManager(BaseManager):
    """
    The ObjectRelationLogsManager handles the interaction between the CmdbObjectRelationLogs-API and the database

    Extends: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database:str = None):
        """
        Set the database connection for the ObjectRelationLogsManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            ObjectRelationLogsManagerInitError: If the ObjectRelationLogsManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(CmdbObjectRelationLog.COLLECTION, dbm)
        except Exception as err:
            raise ObjectRelationLogsManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_object_relation_log(self, object_relation_log: dict) -> int:
        """
        Insert a CmdbObjectRelationLog into the database

        Args:
            object_relation_log (dict): Raw data of the CmdbObjectRelationLog

        Raises:
            ObjectRelationLogsManagerInsertError: When a CmdbObjectRelationLog could not be inserted into database

        Returns:
            int: The public_id of the created CmdbObjectRelationLog
        """
        try:
            return self.insert(object_relation_log)
        except BaseManagerInsertError as err:
            raise ObjectRelationLogsManagerInsertError(err) from err


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_object_relation_log(self, public_id: int) -> Optional[dict]:
        """
        Retrieves a CmdbObjectRelationLog from the database

        Args:
            public_id (int): public_id of the CmdbObjectRelationLog

        Raises:
            ObjectRelationLogsManagerGetError: When a CmdbObjectRelationLog could not be retrieved

        Returns:
            Optional[dict]: Raw data of the CmdbObjectRelationLog if it exists
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise ObjectRelationLogsManagerGetError(err) from err


    def iterate(self,
                builder_params: BuilderParameters,
                user: CmdbUser = None,
                permission: AccessControlPermission = None) -> IterationResult[CmdbObjectRelationLog]:
        """
        Retrieves multiple CmdbObjectRelationLogs

        Args:
            builder_params (BuilderParameters): Filter for which CmdbObjectRelationLogs should be retrieved
            user (CmdbUser, optional): CmdbUser requestion this operation. Defaults to None
            permission (AccessControlPermission, optional): Required permission for the operation. Defaults to None

        Raises:
            ObjectRelationLogsManagerIterationError: When the iteration or creating the IterationResult failed

        Returns:
            IterationResult[CmdbObjectRelationLog]: All CmdbObjectRelationLogs matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params, user, permission)

            iteration_result: IterationResult[CmdbObjectRelationLog] = IterationResult(aggregation_result,
                                                                                       total,
                                                                                       CmdbObjectRelationLog)

            return iteration_result
        except (BaseManagerIterationError, Exception) as err:
            raise ObjectRelationLogsManagerIterationError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_object_relation_log(self, public_id: int) -> bool:
        """
        Deletes a CmdbObjectRelationLog from the database

        Args:
            public_id (int): public_id of the CmdbObjectRelationLog which should be deleted

        Raises:
            ObjectRelationLogsManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise ObjectRelationLogsManagerDeleteError(err) from err

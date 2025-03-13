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
This module contains the implementation of the ProtectionGoalManager
"""
import logging
from typing import Optional, Union

from cmdb.database import MongoDatabaseManager

from cmdb.manager.base_manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.isms_model import IsmsProtectionGoal

from cmdb.framework.results import IterationResult

from cmdb.errors.models.isms_protection_goal import (
    IsmsProtectionGoalToJsonError,
)
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
    BaseManagerIterationError,
)
from cmdb.errors.manager.protection_goal_manager import (
    ProtectionGoalManagerInitError,
    ProtectionGoalManagerInsertError,
    ProtectionGoalManagerGetError,
    ProtectionGoalManagerUpdateError,
    ProtectionGoalManagerDeleteError,
    ProtectionGoalManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                             ProtectionGoalManager - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class ProtectionGoalManager(BaseManager):
    """
    The ProtectionGoalManager manages the interaction between IsmsProtectionGoals and the database

    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the ProtectionGoalManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            ProtectionGoalManagerInitError: If the ProtectionGoalManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(IsmsProtectionGoal.COLLECTION, dbm)
        except Exception as err:
            raise ProtectionGoalManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_protection_goal(self, protection_goal: dict) -> int:
        """
        Insert an IsmsProtectionGoal into the database

        Args:
            protection_goal (dict): Raw data of the IsmsProtectionGoal

        Raises:
            ProtectionGoalManagerInsertError: When an IsmsProtectionGoal could not be inserted into the database

        Returns:
            int: The public_id of the created IsmsProtectionGoal
        """
        try:
            if isinstance(protection_goal, IsmsProtectionGoal):
                protection_goal = IsmsProtectionGoal.to_json(protection_goal)

            return self.insert(protection_goal)
        except (BaseManagerInsertError, IsmsProtectionGoalToJsonError) as err:
            raise ProtectionGoalManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_protection_goal] Exception: %s. Type: %s", err, type(err))
            raise ProtectionGoalManagerInsertError(err) from err


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_protection_goal(self, public_id: int) -> Optional[dict]:
        """
        Retrieves an IsmsProtectionGoal from the database

        Args:
            public_id (int): public_id of the IsmsProtectionGoal

        Raises:
            ProtectionGoalManagerGetError: When an IsmsProtectionGoal could not be retrieved

        Returns:
            Optional[dict]: A dictionary representation of the IsmsProtectionGoal if successful, otherwise None
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise ProtectionGoalManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[IsmsProtectionGoal]:
        """
        Retrieves multiple IsmsProtectionGoals

        Args:
            builder_params (BuilderParameters): Filter for which IsmsProtectionGoals should be retrieved

        Raises:
            ProtectionGoalManagerIterationError: When the iteration failed

        Returns:
            IterationResult[IsmsProtectionGoal]: All IsmsProtectionGoals matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            result: IterationResult[IsmsProtectionGoal] = IterationResult(aggregation_result,
                                                                          total,
                                                                          IsmsProtectionGoal)

            return result
        except BaseManagerIterationError as err:
            raise ProtectionGoalManagerIterationError(err) from err
        except Exception as err:
            LOGGER.error("[iterate] Exception: %s. Type: %s", err, type(err))
            raise ProtectionGoalManagerIterationError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_protection_goal(self, public_id:int, data: Union[IsmsProtectionGoal, dict]) -> None:
        """
        Updates an IsmsProtectionGoal in the database

        Args:
            public_id (int): public_id of the IsmsProtectionGoal which should be updated
            data: Union[IsmsProtectionGoal, dict]: The new data for the IsmsProtectionGoal

        Raises:
            ProtectionGoalManagerUpdateError: When the update operation fails
        """
        try:
            if isinstance(data, IsmsProtectionGoal):
                data = IsmsProtectionGoal.to_json(data)

            self.update({'public_id':public_id}, data)
        except (BaseManagerUpdateError, IsmsProtectionGoalToJsonError) as err:
            raise ProtectionGoalManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_protection_goal] Exception: %s. Type: %s", err, type(err))
            raise ProtectionGoalManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_prtection_goal(self, public_id: int) -> bool:
        """
        Deletes an IsmsProtectionGoal from the database

        Args:
            public_id (int): public_id of the IsmsProtectionGoal which should be deleted

        Raises:
            ProtectionGoalManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise ProtectionGoalManagerDeleteError(err) from err

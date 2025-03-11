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
This module contains the implementation of the RiskClassManager
"""
import logging
from typing import Optional, Union

from cmdb.database import MongoDatabaseManager

from cmdb.manager.base_manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.isms_model.isms_risk_class import IsmsRiskClass

from cmdb.framework.results import IterationResult

from cmdb.errors.models.isms_risk_class import (
    IsmsRiskClassToJsonError,
)
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
    BaseManagerIterationError,
)
from cmdb.errors.manager.risk_class_manager import (
    RiskClassManagerInitError,
    RiskClassManagerInsertError,
    RiskClassManagerGetError,
    RiskClassManagerUpdateError,
    RiskClassManagerDeleteError,
    RiskClassManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               RelationsManager - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class RiskClassManager(BaseManager):
    """
    The RiskClassManager manages the interaction between IsmsRiskClasses and the database

    Extends: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the RiskClassManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            RiskClassManagerInitError: If the RiskClassManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(IsmsRiskClass.COLLECTION, dbm)
        except Exception as err:
            raise RiskClassManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_risk_class(self, risk_class: dict) -> int:
        """
        Insert a IsmsRiskClass into the database

        Args:
            risk_class (dict): Raw data of the IsmsRiskClass

        Raises:
            RelationsManagerInsertError: When a IsmsRiskClass could not be inserted into the database

        Returns:
            int: The public_id of the created IsmsRiskClass
        """
        try:
            if isinstance(risk_class, IsmsRiskClass):
                risk_class = IsmsRiskClass.to_json(risk_class)

            return self.insert(risk_class)
        except (BaseManagerInsertError, IsmsRiskClassToJsonError) as err:
            raise RiskClassManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_risk_class] Exception: %s. Type: %s", err, type(err))
            raise RiskClassManagerInsertError(err) from err


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_risk_class(self, public_id: int) -> Optional[dict]:
        """
        Retrieves an IsmsRiskClass from the database

        Args:
            public_id (int): public_id of the IsmsRiskClass

        Raises:
            RiskClassManagerGetError: When an IsmsRiskClass could not be retrieved

        Returns:
            Optional[dict]: A dictionary representation of the IsmsRiskClass if successful, otherwise None
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise RiskClassManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[IsmsRiskClass]:
        """
        Retrieves multiple IsmsRiskClasses

        Args:
            builder_params (BuilderParameters): Filter for which IsmsRiskClasses should be retrieved

        Raises:
            RiskClassManagerIterationError: When the iteration failed

        Returns:
            IterationResult[IsmsRiskClass]: All IsmsRiskClasses matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            result: IterationResult[IsmsRiskClass] = IterationResult(aggregation_result, total, IsmsRiskClass)

            return result
        except BaseManagerIterationError as err:
            raise RiskClassManagerIterationError(err) from err
        except Exception as err:
            LOGGER.error("[iterate] Exception: %s. Type: %s", err, type(err))
            raise RiskClassManagerIterationError(err) from err


    def count_risk_classes(self) -> int:
        """
        Counts the total number of IsmsRiskClasses in the collection

        Raises:
            RiskClassManagerGetError: If counting IsmsRiskClasses failed

        Returns:
            int: The number of IsmsRiskClasses
        """
        try:
            return self.count_documents(self.collection)
        except BaseManagerGetError as err:
            raise RiskClassManagerGetError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_risk_class(self, public_id:int, data: Union[IsmsRiskClass, dict]) -> None:
        """
        Updates a IsmsRiskClass in the database

        Args:
            public_id (int): public_id of the IsmsRiskClass which should be updated
            data: Union[IsmsRiskClass, dict]: The new data for the IsmsRiskClass

        Raises:
            RiskClassManagerUpdateError: When the update operation fails
        """
        try:
            if isinstance(data, IsmsRiskClass):
                data = IsmsRiskClass.to_json(data)

            self.update({'public_id':public_id}, data)
        except (BaseManagerUpdateError, IsmsRiskClassToJsonError) as err:
            raise RiskClassManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_risk_class] Exception: %s. Type: %s", err, type(err))
            raise RiskClassManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_risk_class(self, public_id: int) -> bool:
        """
        Deletes a IsmsRiskClass from the database

        Args:
            public_id (int): public_id of the IsmsRiskClass which should be deleted

        Raises:
            RiskClassManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise RiskClassManagerDeleteError(err) from err

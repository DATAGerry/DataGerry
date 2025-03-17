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
This module contains the implementation of the RiskMatrixManager
"""
import logging
from typing import Optional, Union

from cmdb.database import MongoDatabaseManager

from cmdb.manager.base_manager import BaseManager

from cmdb.models.isms_model import IsmsRiskMatrix

from cmdb.errors.models.isms_risk_matrix import (
    IsmsRiskMatrixToJsonError,
)
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerUpdateError,
)
from cmdb.errors.manager.risk_matrix_manager import (
    RiskMatrixManagerInitError,
    RiskMatrixManagerInsertError,
    RiskMatrixManagerGetError,
    RiskMatrixManagerUpdateError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                             RiskMatrixManager - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class RiskMatrixManager(BaseManager):
    """
    The RiskMatrixManager manages the interaction between IsmsRiskMatrix and the database

    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the RiskMatrixManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            RiskMatrixManagerInitError: If the RiskMatrixManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(IsmsRiskMatrix.COLLECTION, dbm)
        except Exception as err:
            raise RiskMatrixManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_risk_matrix(self, risk_matrix: dict) -> int:
        """
        Insert an IsmsRiskMatrix into the database

        Args:
            risk_matrix (dict): Raw data of the IsmsRiskMatrix

        Raises:
            RiskMatrixManagerInsertError: When an IsmsRiskMatrix could not be inserted into the database

        Returns:
            int: The public_id of the created IsmsRiskMatrix
        """
        try:
            if isinstance(risk_matrix, IsmsRiskMatrix):
                risk_matrix = IsmsRiskMatrix.to_json(risk_matrix)

            return self.insert(risk_matrix)
        except (BaseManagerInsertError, IsmsRiskMatrixToJsonError) as err:
            raise RiskMatrixManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_risk_matrix] Exception: %s. Type: %s", err, type(err))
            raise RiskMatrixManagerInsertError(err) from err


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_risk_matrix(self, public_id: int) -> Optional[dict]:
        """
        Retrieves an IsmsRiskMatrix from the database

        Args:
            public_id (int): public_id of the IsmsRiskMatrix

        Raises:
            RiskMatrixManagerGetError: When an IsmsRiskMatrix could not be retrieved

        Returns:
            Optional[dict]: A dictionary representation of the IsmsRiskMatrix if successful, otherwise None
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise RiskMatrixManagerGetError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_risk_matrix(self, public_id:int, data: Union[IsmsRiskMatrix, dict]) -> None:
        """
        Updates an IsmsRiskMatrix in the database

        Args:
            public_id (int): public_id of the IsmsRiskMatrix which should be updated
            data: Union[IsmsRiskMatrix, dict]: The new data for the IsmsRiskMatrix

        Raises:
            RiskMatrixManagerUpdateError: When the update operation fails
        """
        try:
            if isinstance(data, IsmsRiskMatrix):
                data = IsmsRiskMatrix.to_json(data)

            self.update({'public_id':public_id}, data)
        except (BaseManagerUpdateError, IsmsRiskMatrixToJsonError) as err:
            raise RiskMatrixManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_risk_matrix] Exception: %s. Type: %s", err, type(err))
            raise RiskMatrixManagerUpdateError(err) from err

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
This module contains the implementation of the ImpactManager
"""
import logging
from typing import Optional, Union

from cmdb.database import MongoDatabaseManager

from cmdb.manager.base_manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.isms_model import IsmsImpact

from cmdb.framework.results import IterationResult

from cmdb.errors.models.isms_impact import (
    IsmsImpactToJsonError,
)
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
    BaseManagerIterationError,
)
from cmdb.errors.manager.impact_manager import (
    ImpactManagerInitError,
    ImpactManagerInsertError,
    ImpactManagerGetError,
    ImpactManagerUpdateError,
    ImpactManagerDeleteError,
    ImpactManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 ImpactManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class ImpactManager(BaseManager):
    """
    The ImpactManager manages the interaction between IsmsImpacts and the database

    Extends: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the ImpactManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            ImpactManagerInitError: If the ImpactManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(IsmsImpact.COLLECTION, dbm)
        except Exception as err:
            raise ImpactManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_impact(self, impact: dict) -> int:
        """
        Insert an IsmsImpact into the database

        Args:
            impact (dict): Raw data of the IsmsImpact

        Raises:
            ImpactManagerInsertError: When an IsmsImpact could not be inserted into the database

        Returns:
            int: The public_id of the created IsmsImpact
        """
        try:
            if isinstance(impact, IsmsImpact):
                impact = IsmsImpact.to_json(impact)

            return self.insert(impact)
        except (BaseManagerInsertError, IsmsImpactToJsonError) as err:
            raise ImpactManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_impact] Exception: %s. Type: %s", err, type(err))
            raise ImpactManagerInsertError(err) from err


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_impact(self, public_id: int) -> Optional[dict]:
        """
        Retrieves an IsmsImpact from the database

        Args:
            public_id (int): public_id of the IsmsImpact

        Raises:
            ImpactManagerGetError: When an IsmsImpact could not be retrieved

        Returns:
            Optional[dict]: A dictionary representation of the IsmsImpact if successful, otherwise None
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise ImpactManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[IsmsImpact]:
        """
        Retrieves multiple IsmsLikelihoods

        Args:
            builder_params (BuilderParameters): Filter for which IsmsLikelihoods should be retrieved

        Raises:
            ImpactManagerIterationError: When the iteration failed

        Returns:
            IterationResult[IsmsImpact]: All IsmsLikelihoods matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            result: IterationResult[IsmsImpact] = IterationResult(aggregation_result, total, IsmsImpact)

            return result
        except BaseManagerIterationError as err:
            raise ImpactManagerIterationError(err) from err
        except Exception as err:
            LOGGER.error("[iterate] Exception: %s. Type: %s", err, type(err))
            raise ImpactManagerIterationError(err) from err


    def count_impacts(self) -> int:
        """
        Counts the total number of IsmsImpacts in the collection

        Raises:
            ImpactManagerGetError: If counting IsmsImpacts failed

        Returns:
            int: The number of IsmsImpacts
        """
        try:
            return self.count_documents(self.collection)
        except BaseManagerGetError as err:
            raise ImpactManagerGetError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_impact(self, public_id:int, data: Union[IsmsImpact, dict]) -> None:
        """
        Updates an IsmsImpact in the database

        Args:
            public_id (int): public_id of the IsmsImpact which should be updated
            data: Union[IsmsImpact, dict]: The new data for the IsmsImpact

        Raises:
            ImpactManagerUpdateError: When the update operation fails
        """
        try:
            if isinstance(data, IsmsImpact):
                data = IsmsImpact.to_json(data)

            self.update({'public_id':public_id}, data)
        except (BaseManagerUpdateError, IsmsImpactToJsonError) as err:
            raise ImpactManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_impact] Exception: %s. Type: %s", err, type(err))
            raise ImpactManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_impact(self, public_id: int) -> bool:
        """
        Deletes an IsmsImpact from the database

        Args:
            public_id (int): public_id of the IsmsImpact which should be deleted

        Raises:
            ImpactManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise ImpactManagerDeleteError(err) from err

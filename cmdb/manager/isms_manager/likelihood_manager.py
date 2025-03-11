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
This module contains the implementation of the LikelihoodManager
"""
import logging
from typing import Optional, Union

from cmdb.database import MongoDatabaseManager

from cmdb.manager.base_manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.isms_model import IsmsLikelihood

from cmdb.framework.results import IterationResult

from cmdb.errors.models.isms_likelihood import (
    IsmsLikelihoodToJsonError,
)
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
    BaseManagerIterationError,
)
from cmdb.errors.manager.likelihood_manager import (
    LikelihoodManagerInitError,
    LikelihoodManagerInsertError,
    LikelihoodManagerGetError,
    LikelihoodManagerUpdateError,
    LikelihoodManagerDeleteError,
    LikelihoodManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               LikelihoodManager - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class LikelihoodManager(BaseManager):
    """
    The LikelihoodManager manages the interaction between IsmsLikelihoods and the database

    Extends: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the LikelihoodManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            LikelihoodManagerInitError: If the LikelihoodManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(IsmsLikelihood.COLLECTION, dbm)
        except Exception as err:
            raise LikelihoodManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_likelihood(self, likelihood: dict) -> int:
        """
        Insert an IsmsLikelihood into the database

        Args:
            likelihood (dict): Raw data of the IsmsLikelihood

        Raises:
            LikelihoodManagerInsertError: When an IsmsLikelihood could not be inserted into the database

        Returns:
            int: The public_id of the created IsmsLikelihood
        """
        try:
            if isinstance(likelihood, IsmsLikelihood):
                likelihood = IsmsLikelihood.to_json(likelihood)

            return self.insert(likelihood)
        except (BaseManagerInsertError, IsmsLikelihoodToJsonError) as err:
            raise LikelihoodManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_likelihood] Exception: %s. Type: %s", err, type(err))
            raise LikelihoodManagerInsertError(err) from err


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_likelihood(self, public_id: int) -> Optional[dict]:
        """
        Retrieves an IsmsLikelihood from the database

        Args:
            public_id (int): public_id of the IsmsLikelihood

        Raises:
            LikelihoodManagerGetError: When an IsmsLikelihood could not be retrieved

        Returns:
            Optional[dict]: A dictionary representation of the IsmsLikelihood if successful, otherwise None
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise LikelihoodManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[IsmsLikelihood]:
        """
        Retrieves multiple IsmsLikelihoods

        Args:
            builder_params (BuilderParameters): Filter for which IsmsLikelihoods should be retrieved

        Raises:
            LikelihoodManagerIterationError: When the iteration failed

        Returns:
            IterationResult[IsmsLikelihood]: All IsmsLikelihoods matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            result: IterationResult[IsmsLikelihood] = IterationResult(aggregation_result, total, IsmsLikelihood)

            return result
        except BaseManagerIterationError as err:
            raise LikelihoodManagerIterationError(err) from err
        except Exception as err:
            LOGGER.error("[iterate] Exception: %s. Type: %s", err, type(err))
            raise LikelihoodManagerIterationError(err) from err


    def count_likelihoods(self) -> int:
        """
        Counts the total number of IsmsLikelihoods in the collection

        Raises:
            LikelihoodManagerGetError: If counting IsmsLikelihoods failed

        Returns:
            int: The number of IsmsLikelihoods
        """
        try:
            return self.count_documents(self.collection)
        except BaseManagerGetError as err:
            raise LikelihoodManagerGetError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_likelihood(self, public_id:int, data: Union[IsmsLikelihood, dict]) -> None:
        """
        Updates an IsmsLikelihood in the database

        Args:
            public_id (int): public_id of the IsmsLikelihood which should be updated
            data: Union[IsmsLikelihood, dict]: The new data for the IsmsLikelihood

        Raises:
            LikelihoodManagerUpdateError: When the update operation fails
        """
        try:
            if isinstance(data, IsmsLikelihood):
                data = IsmsLikelihood.to_json(data)

            self.update({'public_id':public_id}, data)
        except (BaseManagerUpdateError, IsmsLikelihoodToJsonError) as err:
            raise LikelihoodManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_likelihood] Exception: %s. Type: %s", err, type(err))
            raise LikelihoodManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_likelihood(self, public_id: int) -> bool:
        """
        Deletes an IsmsLikelihood from the database

        Args:
            public_id (int): public_id of the IsmsLikelihood which should be deleted

        Raises:
            LikelihoodManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise LikelihoodManagerDeleteError(err) from err

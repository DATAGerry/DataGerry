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
This module contains the implementation of the ExtendableOptionsManager
"""
import logging
from typing import Optional, Union

from cmdb.database import MongoDatabaseManager

from cmdb.manager.base_manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.extendable_option_model import CmdbExtendableOption

from cmdb.framework.results import IterationResult

from cmdb.errors.models.cmdb_extendable_option import (
    CmdbExtendableOptionToJsonError,
)
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
    BaseManagerIterationError,
)
from cmdb.errors.manager.extendable_options_manager import (
    ExtendableOptionsManagerInitError,
    ExtendableOptionsManagerInsertError,
    ExtendableOptionsManagerGetError,
    ExtendableOptionsManagerUpdateError,
    ExtendableOptionsManagerDeleteError,
    ExtendableOptionsManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                           ExtendableOptionsManager - CLASS                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class ExtendableOptionsManager(BaseManager):
    """
    The ExtendableOptionsManager manages the interaction between CmdbExtendableOptions and the database

    Extends: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the ExtendableOptionsManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            ExtendableOptionsManagerInitError: If the ExtendableOptionsManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(CmdbExtendableOption.COLLECTION, dbm)
        except Exception as err:
            raise ExtendableOptionsManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_extendable_option(self, extendable_option: dict) -> int:
        """
        Insert an CmdbExtendableOption into the database

        Args:
            extendable_option (dict): Raw data of the CmdbExtendableOption

        Raises:
            ExtendableOptionsManagerInsertError: When an CmdbExtendableOption could not be inserted into the database

        Returns:
            int: The public_id of the created CmdbExtendableOption
        """
        try:
            if isinstance(extendable_option, CmdbExtendableOption):
                extendable_option = CmdbExtendableOption.to_json(extendable_option)

            return self.insert(extendable_option)
        except (BaseManagerInsertError, CmdbExtendableOptionToJsonError) as err:
            raise ExtendableOptionsManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_extendable_option] Exception: %s. Type: %s", err, type(err))
            raise ExtendableOptionsManagerInsertError(err) from err


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_extendable_option(self, public_id: int) -> Optional[dict]:
        """
        Retrieves an CmdbExtendableOption from the database

        Args:
            public_id (int): public_id of the CmdbExtendableOption

        Raises:
            ExtendableOptionsManagerGetError: When an CmdbExtendableOption could not be retrieved

        Returns:
            Optional[dict]: A dictionary representation of the CmdbExtendableOption if successful, otherwise None
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise ExtendableOptionsManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbExtendableOption]:
        """
        Retrieves multiple CmdbExtendableOptions

        Args:
            builder_params (BuilderParameters): Filter for which CmdbExtendableOptions should be retrieved

        Raises:
            ExtendableOptionsManagerIterationError: When the iteration failed

        Returns:
            IterationResult[CmdbExtendableOption]: All CmdbExtendableOptions matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            result: IterationResult[CmdbExtendableOption] = IterationResult(aggregation_result,
                                                                            total,
                                                                            CmdbExtendableOption)

            return result
        except BaseManagerIterationError as err:
            raise ExtendableOptionsManagerIterationError(err) from err
        except Exception as err:
            LOGGER.error("[iterate] Exception: %s. Type: %s", err, type(err))
            raise ExtendableOptionsManagerIterationError(err) from err


    def count_extendable_options(self) -> int:
        """
        Counts the total number of CmdbExtendableOptions in the collection

        Raises:
            ExtendableOptionsManagerGetError: If counting CmdbExtendableOptions failed

        Returns:
            int: The number of CmdbExtendableOptions
        """
        try:
            return self.count_documents(self.collection)
        except BaseManagerGetError as err:
            raise ExtendableOptionsManagerGetError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_extendable_option(self, public_id:int, data: Union[CmdbExtendableOption, dict]) -> None:
        """
        Updates an CmdbExtendableOption in the database

        Args:
            public_id (int): public_id of the CmdbExtendableOption which should be updated
            data: Union[CmdbExtendableOption, dict]: The new data for the CmdbExtendableOption

        Raises:
            ExtendableOptionsManagerUpdateError: When the update operation fails
        """
        try:
            if isinstance(data, CmdbExtendableOption):
                data = CmdbExtendableOption.to_json(data)

            self.update({'public_id':public_id}, data)
        except (BaseManagerUpdateError, CmdbExtendableOptionToJsonError) as err:
            raise ExtendableOptionsManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_extendable_option] Exception: %s. Type: %s", err, type(err))
            raise ExtendableOptionsManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_extendable_option(self, public_id: int) -> bool:
        """
        Deletes an CmdbExtendableOption from the database

        Args:
            public_id (int): public_id of the CmdbExtendableOption which should be deleted

        Raises:
            ExtendableOptionsManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise ExtendableOptionsManagerDeleteError(err) from err

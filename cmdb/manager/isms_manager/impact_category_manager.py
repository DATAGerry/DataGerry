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
This module contains the implementation of the ImpactCategoryManager
"""
import logging
from typing import Optional, Union

from cmdb.database import MongoDatabaseManager

from cmdb.manager.base_manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.isms_model import IsmsImpactCategory

from cmdb.framework.results import IterationResult

from cmdb.errors.models.isms_impact_category import (
    IsmsImpactCategoryToJsonError,
)
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
    BaseManagerIterationError,
)
from cmdb.errors.manager.impact_category_manager import (
    ImpactCategoryManagerInitError,
    ImpactCategoryManagerInsertError,
    ImpactCategoryManagerGetError,
    ImpactCategoryManagerUpdateError,
    ImpactCategoryManagerDeleteError,
    ImpactCategoryManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                             ImpactCategoryManager - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class ImpactCategoryManager(BaseManager):
    """
    The ImpactCategoryManager manages the interaction between IsmsImpactCategories and the database

    Extends: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the ImpactCategoryManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            ImpactCategoryManagerInitError: If the ImpactCategoryManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(IsmsImpactCategory.COLLECTION, dbm)
        except Exception as err:
            raise ImpactCategoryManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_impact_category(self, impact: dict) -> int:
        """
        Insert an IsmsImpactCategory into the database

        Args:
            impact (dict): Raw data of the IsmsImpactCategory

        Raises:
            ImpactCategoryManagerInsertError: When an IsmsImpactCategory could not be inserted into the database

        Returns:
            int: The public_id of the created IsmsImpactCategory
        """
        try:
            if isinstance(impact, IsmsImpactCategory):
                impact = IsmsImpactCategory.to_json(impact)

            return self.insert(impact)
        except (BaseManagerInsertError, IsmsImpactCategoryToJsonError) as err:
            raise ImpactCategoryManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_impact_category] Exception: %s. Type: %s", err, type(err))
            raise ImpactCategoryManagerInsertError(err) from err


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_impact_category(self, public_id: int) -> Optional[dict]:
        """
        Retrieves an IsmsImpactCategory from the database

        Args:
            public_id (int): public_id of the IsmsImpactCategory

        Raises:
            ImpactCategoryManagerGetError: When an IsmsImpactCategory could not be retrieved

        Returns:
            Optional[dict]: A dictionary representation of the IsmsImpactCategory if successful, otherwise None
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise ImpactCategoryManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[IsmsImpactCategory]:
        """
        Retrieves multiple IsmsImpactCategories

        Args:
            builder_params (BuilderParameters): Filter for which IsmsImpactCategories should be retrieved

        Raises:
            ImpactCategoryManagerIterationError: When the iteration failed

        Returns:
            IterationResult[IsmsImpactCategory]: All IsmsImpactCategories matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            result: IterationResult[IsmsImpactCategory] = IterationResult(aggregation_result,
                                                                          total,
                                                                          IsmsImpactCategory)

            return result
        except BaseManagerIterationError as err:
            raise ImpactCategoryManagerIterationError(err) from err
        except Exception as err:
            LOGGER.error("[iterate] Exception: %s. Type: %s", err, type(err))
            raise ImpactCategoryManagerIterationError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_impact_category(self, public_id:int, data: Union[IsmsImpactCategory, dict]) -> None:
        """
        Updates an IsmsImpactCategory in the database

        Args:
            public_id (int): public_id of the IsmsImpactCategory which should be updated
            data: Union[IsmsImpactCategory, dict]: The new data for the IsmsImpactCategory

        Raises:
            ImpactCategoryManagerUpdateError: When the update operation fails
        """
        try:
            if isinstance(data, IsmsImpactCategory):
                data = IsmsImpactCategory.to_json(data)

            self.update({'public_id':public_id}, data)
        except (BaseManagerUpdateError, IsmsImpactCategoryToJsonError) as err:
            raise ImpactCategoryManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_impact_category] Exception: %s. Type: %s", err, type(err))
            raise ImpactCategoryManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_impact_category(self, public_id: int) -> bool:
        """
        Deletes an IsmsImpactCategory from the database

        Args:
            public_id (int): public_id of the IsmsImpactCategory which should be deleted

        Raises:
            ImpactCategoryManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise ImpactCategoryManagerDeleteError(err) from err

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

    def add_new_impact_to_categories(self, new_impact_id: int) -> None:
        """
        Adds the new IsmsImpact entry to all IsmsImpactCategories

        Args:
            new_impact_id (int): public_id of the newly created IsmsImpact
        """
        update = {
            "impact_descriptions": {
                "impact_id": new_impact_id,
                "value": ""
            }
        }

        self.update_many({}, update, add_to_set=True)


    def remove_deleted_impact_from_categories(self, deleted_impact_id: int) -> None:
        """
        Removes the IsmsImpact entry from all IsmsImpactCategories

        Args:
            new_impact_id (int): public_id of the deleted IsmsImpact
        """
        update = {
            "impact_descriptions": {
                "impact_id": {"$eq": deleted_impact_id}
            }
        }

        # Call update_many_pull to remove the references in all ImpactCategory documents
        self.update_many_pull({}, update)

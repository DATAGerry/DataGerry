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
This module contains the implementation of the ReportCategoriesManager
"""
import logging
from typing import Optional, Union

from cmdb.database import MongoDatabaseManager
from cmdb.manager.base_manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.reports_model.cmdb_report_category import CmdbReportCategory
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import (
    BaseManagerGetError,
    BaseManagerIterationError,
    BaseManagerInsertError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
)
from cmdb.errors.models.cmdb_report_category import (
    CmdbReportCategoryInitFromDataError,
    CmdbReportCategoryToJsonError,
)
from cmdb.errors.manager.report_categories_manager import (
    ReportCategoriesManagerInitError,
    ReportCategoriesManagerInsertError,
    ReportCategoriesManagerGetError,
    ReportCategoriesManagerIterationError,
    ReportCategoriesManagerDeleteError,
    ReportCategoriesManagerUpdateError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            ReportCategoriesManager - CLASS                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class ReportCategoriesManager(BaseManager):
    """
    The ReportCategoriesManager handles the interaction between ReportCategories and the database

    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, database:str = None):
        """
        Set the database connection for the ReportCategoriesManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            ReportCategoriesManagerInitError: If the ReportCategoriesManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(CmdbReportCategory.COLLECTION, dbm)
        except Exception as err:
            raise ReportCategoriesManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_report_category(self, report_category: dict) -> int:
        """
        Insert a CmdbReportCategory into the database

        Args:
            report_category (dict): Raw data of the CmdbReportCategory

        Raises:
            ReportCategoriesManagerInsertError: When a CmdbReportCategory could not be inserted into the database

        Returns:
            int: The public_id of the created CmdbReportCategory
        """
        try:
            return self.insert(report_category)
        except BaseManagerInsertError as err:
            raise ReportCategoriesManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_report_category] Exception: %s. Type: %s", err, type(err))
            raise ReportCategoriesManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_report_category(self, public_id: int) -> Optional[CmdbReportCategory]:
        """
        Retrives a CmdbReportCategory from the database with the given public_id

        Args:
            public_id (int): public_id of the CmdbReportCategory which should be retrieved

        Raises:
            ReportCategoriesManagerGetError: Raised if the CmdbReportCategory could not ne retrieved

        Returns:
            Optional[CmdbReportCategory]: The requested CmdbReportCategory if it exists, else None
        """
        try:
            requested_report_category = self.get_one(public_id)

            if requested_report_category:
                return CmdbReportCategory.from_data(requested_report_category)

            return None
        except (BaseManagerGetError, CmdbReportCategoryInitFromDataError) as err:
            raise ReportCategoriesManagerGetError(err) from err
        except Exception as err:
            LOGGER.error("[get_report_category] Exception: %s. Type: %s", err, type(err))
            raise ReportCategoriesManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbReportCategory]:
        """
        Retrieves multiple CmdbReportCategories

        Args:
            builder_params (BuilderParameters): Filter for which CmdbReportCategories should be retrieved

        Raises:
            ReportCategoriesManagerIterationError: When the iteration failed

        Returns:
            IterationResult[CmdbRelation]: All CmdbRelations matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            iteration_result: IterationResult[CmdbReportCategory] = IterationResult(aggregation_result,
                                                                                    total,
                                                                                    CmdbReportCategory)

            return iteration_result
        except BaseManagerIterationError as err:
            raise ReportCategoriesManagerIterationError(err) from err
        except Exception as err:
            LOGGER.error("[iterate] Exception: %s. Type: %s", err, type(err))
            raise ReportCategoriesManagerIterationError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_report_category(self, public_id:int, data: Union[CmdbReportCategory, dict]) -> None:
        """
        Updates a CmdbRelation in the database

        Args:
            public_id (int): public_id of the CmdbRelation which should be updated
            data: Union[CmdbRelation, dict]: The new data for the CmdbRelation

        Raises:
            RelationsManagerUpdateError: When the update operation fails
        """
        try:
            if isinstance(data, CmdbReportCategory):
                data = CmdbReportCategory.to_json(data)

            self.update({'public_id':public_id}, data)
        except (BaseManagerUpdateError, CmdbReportCategoryToJsonError) as err:
            raise ReportCategoriesManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_report_category] Exception: %s. Type: %s", err, type(err))
            raise ReportCategoriesManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_report_category(self, public_id: int) -> bool:
        """
        Deletes a CmdbRelation from the database

        Args:
            public_id (int): public_id of the CmdbRelation which should be deleted

        Raises:
            RelationsManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise ReportCategoriesManagerDeleteError(err) from err

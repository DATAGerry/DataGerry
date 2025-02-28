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

from cmdb.database import MongoDatabaseManager
from cmdb.manager.base_manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.reports_model.cmdb_report_category import CmdbReportCategory
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import BaseManagerGetError, BaseManagerIterationError, BaseManagerInsertError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            ReportCategoriesManager - CLASS                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class ReportCategoriesManager(BaseManager):
    """
    The ReportCategoriesManager handles the interaction between the ReportCategories-API and the database
    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, database:str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            dbm (MongoDatabaseManager): Database connection
        """
        if database:
            dbm.connector.set_database(database)

        super().__init__(CmdbReportCategory.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_report_category(self, data: dict) -> int:
        """
        Inserts a single CmdbReportCategory in the database

        Args:
            data (dict): Data of the new CmdbReportCategory

        Returns:
            int: public_id of the newly created CmdbReportCategory
        """
        try:
            new_report_category = CmdbReportCategory(**data)

            ack = self.insert(new_report_category.__dict__)

            return ack
            #TODO: ERROR-FIX
        except Exception as err:
            raise BaseManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_report_category(self, public_id: int) -> CmdbReportCategory:
        """
        Retrives a CmdbReportCategory from the database with the given public_id

        Args:
            public_id (int): public_id of the CmdbReportCategory which should be retrieved
        Raises:
            BaseManagerGetError: Raised if the CmdbReportCategory could not ne retrieved
        Returns:
            CmdbReportCategory: The requested CmdbReportCategory if it exists, else None
        """
        try:
            requested_report_category = self.get_one(public_id)
        except Exception as err:
            #TODO: ERROR-FIX
            raise BaseManagerGetError(f"Report Category with ID: {public_id}! 'GET' Error: {err}") from err

        if requested_report_category:
            requested_report_category = CmdbReportCategory.from_data(requested_report_category)

            return requested_report_category

        #TODO: ERROR-FIX
        raise BaseManagerGetError(f'Report Category with ID: {public_id} not found!')


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbReportCategory]:
        """
        Performs an aggregation on the database

        Args:
            builder_params (BuilderParameters): Contains input to identify the target of action

        Raises:
            BaseManagerIterationError: Raised when something goes wrong during the aggregate part
            BaseManagerIterationError: Raised when something goes wrong during the building of the IterationResult
        Returns:
            IterationResult[CmdbReportCategory]: Result which matches the Builderparameters
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            iteration_result: IterationResult[CmdbReportCategory] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbReportCategory)

            return iteration_result
        except Exception as err:
            #TODO: ERROR-FIX
            raise BaseManagerIterationError(err) from err


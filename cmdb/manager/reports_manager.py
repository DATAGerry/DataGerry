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
This module contains the implementation of the ReportsManager
"""
import logging

from cmdb.database import MongoDatabaseManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.base_manager import BaseManager

from cmdb.models.reports_model.cmdb_report import CmdbReport
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import BaseManagerInsertError, BaseManagerGetError, BaseManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                ReportsManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class ReportsManager(BaseManager):
    """
    The ReportsManager handles the interaction between the Reports-API and the database
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

        super().__init__(CmdbReport.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_report(self, data: dict) -> int:
        """
        Inserts a single CmdbReport in the database

        Args:
            data (dict): Data of the new CmdbReport

        Returns:
            int: public_id of the newly created CmdbReport
        """
        try:
            new_report_category = CmdbReport(**data)

            ack = self.insert(new_report_category.__dict__)
            #TODO: ERROR-FIX
            return ack
        except Exception as err:
            raise BaseManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_report(self, public_id: int) -> CmdbReport:
        """
        Retrives a CmdbReport from the database with the given public_id

        Args:
            public_id (int): public_id of the CmdbReport which should be retrieved
        Raises:
            BaseManagerGetError: Raised if the CmdbReport could not be retrieved
        Returns:
            CmdbReport: The requested CmdbReport if it exists, else None
        """
        try:
            requested_report_category = self.get_one(public_id)
        except Exception as err:
            #TODO: ERROR-FIX
            raise BaseManagerGetError(f"Report with ID: {public_id}! 'GET' Error: {err}") from err

        if requested_report_category:
            requested_report_category = CmdbReport.from_data(requested_report_category)

            return requested_report_category

        #TODO: ERROR-FIX
        raise BaseManagerGetError(f'Report with ID: {public_id} not found!')


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbReport]:
        """
        Performs an aggregation on the database

        Args:
            builder_params (BuilderParameters): Contains input to identify the target of action

        Raises:
            BaseManagerIterationError: Raised when something goes wrong during the aggregate part
            BaseManagerIterationError: Raised when something goes wrong during the building of the IterationResult
        Returns:
            IterationResult[CmdbReport]: Result which matches the Builderparameters
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            iteration_result: IterationResult[CmdbReport] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbReport)

            return iteration_result
        except Exception as err:
            #TODO: ERROR-FIX
            raise BaseManagerIterationError(err) from err


    def count_reports(self, criteria: dict = None) -> int:
        """
        Counts the number of reports in the collection based on the given criteria

        Args:
            criteria (dict, optional): A dictionary specifying filter conditions for counting reports
                                    If not provided, counts all reports in the collection

        Raises:
            BaseManagerGetError: If an error occurs while counting documents in the collection

        Returns:
            int: The number of reports matching the given criteria
        """
        try:
            if criteria:
                report_count = self.count_documents(self.collection, criteria=criteria)
            else:
                report_count = self.count_documents(self.collection)

            return report_count
        except BaseManagerGetError as err:
            # TODO: ERROR-FIX (Report Specific Error)
            raise BaseManagerGetError(err) from err

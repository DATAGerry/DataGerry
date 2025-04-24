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
This module contains the implementation of the RiskManager
"""
import logging

from cmdb.database import MongoDatabaseManager

from cmdb.manager.generic_manager import GenericManager

from cmdb.models.isms_model import IsmsRisk, IsmsRiskAssessment

from cmdb.errors.manager.risk_manager import RISK_MANAGER_ERRORS
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  RiskManager - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class RiskManager(GenericManager):
    """
    The RiskManager manages the interaction between IsmsRisks and the database

    Extends: GenericManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        super().__init__(dbm, IsmsRisk, RISK_MANAGER_ERRORS, database)

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_with_follow_up(self, public_id: int) -> bool:
        """
        Deletes the Risk with the given public_id and all associated RiskAssessments
        that reference it via the 'risk_id' field.

        Args:
            public_id (int): The public_id of the Risk to delete

        Returns:
            bool: True if the Risk was successfully deleted, False otherwise
        """
        # Delete all RiskAssessments referencing this Risk
        self.dbm.get_collection(IsmsRiskAssessment.COLLECTION).delete_many({'risk_id': public_id})

        # Delete the Risk itself
        return self.delete_item(public_id)

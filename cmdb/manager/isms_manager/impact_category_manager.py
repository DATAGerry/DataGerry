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

from cmdb.database import MongoDatabaseManager

from cmdb.manager.generic_manager import GenericManager

from cmdb.models.isms_model import IsmsImpactCategory

from cmdb.errors.manager.impact_category_manager import IMPACT_CATEGORY_MANAGER_ERRORS
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                             ImpactCategoryManager - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class ImpactCategoryManager(GenericManager):
    """
    The ImpactCategoryManager manages the interaction between IsmsImpactCategories and the database

    Extends: GenericManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        super().__init__(dbm, IsmsImpactCategory, IMPACT_CATEGORY_MANAGER_ERRORS, database)

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
                "value": "-"
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

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

from cmdb.database import MongoDatabaseManager

from cmdb.manager.generic_manager import GenericManager

from cmdb.models.isms_model import IsmsLikelihood

from cmdb.errors.manager.likelihood_manager import LIKELIHOOD_MANAGER_ERRORS, LikelihoodManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               LikelihoodManager - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class LikelihoodManager(GenericManager):
    """
    The LikelihoodManager manages the interaction between IsmsLikelihood and the database

    Extends: GenericManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        super().__init__(dbm, IsmsLikelihood, LIKELIHOOD_MANAGER_ERRORS, database)

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

    def likelihood_calculation_basis_exists(self, calculation_basis: float) -> bool:
        """
        Checks if a calculation_basis already exists for an IsmsLikelihood

        Args:
            calculation_basis (float): The calculation_basis which should be checked

        Raises:
            LikelihoodManagerGetError: If checking calculation_basis failed

        Returns:
            bool: True if calculation_basis exists, else false
        """
        try:
            result = self.get_one_by({'calculation_basis': calculation_basis})

            return bool(result)
        except Exception as err:
            LOGGER.error("[likelihood_calculation_basis_exists] Exception: %s. Type: %s", err, type(err))
            raise LikelihoodManagerGetError(err) from err

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


from cmdb.database import MongoDatabaseManager

from cmdb.manager.generic_manager import GenericManager

from cmdb.models.extendable_option_model import CmdbExtendableOption

from cmdb.errors.manager.extendable_options_manager import EXTENDABLE_OPTIONS_MANAGER_ERRORS
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                           ExtendableOptionsManager - CLASS                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class ExtendableOptionsManager(GenericManager):
    """
    The ThreatManager manages the interaction between CmdbExtendableOptions and the database

    Extends: GenericManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        super().__init__(dbm, CmdbExtendableOption, EXTENDABLE_OPTIONS_MANAGER_ERRORS, database)

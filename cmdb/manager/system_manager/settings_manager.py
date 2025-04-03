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
Implementation of SettingsManager
"""
import logging
from typing import Union
from pymongo.results import UpdateResult

from cmdb.database import MongoDatabaseManager

from cmdb.manager.system_manager.system_reader import SystemReader

from cmdb.errors.system_config import SectionError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                SettingsManager - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class SettingsManager(SystemReader):
    """
    Settings reader loads settings from database
    """
    COLLECTION = 'settings.conf'

    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        init system settings reader
        Args:
            database_manager: database managers
        """
        if database:
            dbm.connector.set_database(database)

        self.dbm = dbm

        super().__init__()


    def get_value(self, name, section) -> Union[dict, list]:
        """
        Retrieve a value from a given section
        Args:
            name: key of value
            section: section of the value

        Returns:
            value
        """
        return self.dbm.find_one_by(collection=SettingsManager.COLLECTION, filter={'_id': section})[name]


    def get_section(self, section_name: str) -> dict:
        """document"""
        #TODO: DOCUMENT-FIX
        query_filter = {'_id': section_name}
        return self.dbm.find_one_by(collection=SettingsManager.COLLECTION, filter=query_filter)


    def get_sections(self):
        """
        get all sections from config
        Returns:
            list of sections inside a config
        """
        return self.dbm.find_all(collection=SettingsManager.COLLECTION, projection={'_id': 1})


    def get_all_values_from_section(self, section, default=None) -> dict:
        """
        get all values from a section
        Args:
            section: section name
            default: if no document was found

        Returns:
            key value dict of all elements inside section
        """

        section_values = self.dbm.find_one_by(collection=SettingsManager.COLLECTION, filter={'_id': section})

        if not section_values:
            if default:
                return default

            raise SectionError(f"The section '{section}' does not exist!")

        return section_values


    def write(self, _id: str, data: dict) -> UpdateResult:
        """
        Writes a new setting value in the database

        Args:
            _id (str): Identifier of the setting
            data (dict): The new data of the setting

        Returns:
            UpdateResult: The result of the update operation
        """
        return self.dbm.update(collection=self.COLLECTION, criteria={'_id': _id}, data=data, upsert=True)

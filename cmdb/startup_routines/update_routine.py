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
This module contains the implementation of the Update routine for DataGerry
"""
import logging
from pymongo.errors import CollectionInvalid

from cmdb.database import MongoDatabaseManager

from cmdb.startup_routines.update_status_enum import UpdateStatus
from cmdb.updater.updater_module import UpdaterModule
from cmdb.updater.updater_settings import UpdateSettings
from cmdb.manager import (
    SettingsReaderManager,
    SettingsWriterManager,
)

from cmdb.utils.system_config_reader import SystemConfigReader
from cmdb.framework.constants import __COLLECTIONS__ as FRAMEWORK_CLASSES
from cmdb.models.user_management_constants import __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION

from cmdb.errors.database import ServerTimeoutError
from cmdb.errors.setup import CollectionInitError
from cmdb.errors.system_config import SectionError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 UpdateRoutine - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class UpdateRoutine:
    """
    This class manages the updates of DataGerry
    """
    def __init__(self, dbm: MongoDatabaseManager):
        self.status = UpdateStatus.NOT
        # check if settings are loaded
        self.setup_system_config_reader = SystemConfigReader()
        system_config_reader_status = self.setup_system_config_reader.status()
        self.dbm = dbm

        if system_config_reader_status is not True:
            self.status = UpdateStatus.ERROR
            raise RuntimeError(
                f'The system configuration files were loaded incorrectly or nothing has been loaded at all. - \
                    system config reader status: {system_config_reader_status}')


    def get_updater_status(self) -> UpdateStatus:
        """
        Retrieve the current status of the UpdateRoutine

        Returns:
            `UpdateStatus`: The current UpdateStatus of the UpdateRoutine
        """
        return self.status


    def __check_database(self) -> bool:
        """
        Checks the connection status of the database

        Returns:
            bool: True if connected, False if disconnected
        """
        LOGGER.info('[UPDATE ROUTINE] Checking database connection')
        try:
            return self.dbm.connector.is_connected()
        except ServerTimeoutError:
            LOGGER.info("[UPDATE ROUTINE] Database connection check failed due to timeout")
            return False


    def __is_database_empty(self) -> bool:
        """
        Checks if the database is empty of collections

        Returns:
            bool: True if database is empty, else False
        """
        return not self.dbm.connector.database.list_collection_names()


    def start_update(self) -> UpdateStatus:
        """
        Updates the database collections

        Raises:
            RuntimeError: When the databse can not be reached

        Returns:
            UpdateStatus: The status of the update routine
        """
        LOGGER.info('[UPDATE ROUTINE] Update database collection')
        self.status = UpdateStatus.RUNNING

        # check database
        if not self.__check_database():
            self.status = UpdateStatus.ERROR
            raise RuntimeError("Update failed because the database can not be reached")

        if not self.__is_database_empty():
            try:
                self.update_database_collection()
            except CollectionInitError as err:
                LOGGER.error("[start_update] Error: %s", err)

            self.update_db_version()
        else:
            LOGGER.info("[UPDATE ROUTINE] The update is faulty because no collection was detected.")

        LOGGER.info('[UPDATE ROUTINE] Update database collection finished.')
        self.status = UpdateStatus.FINISHED
        LOGGER.info('[UPDATE ROUTINE] FINISHED!')

        return self.status


    def update_database_collection(self) -> None:
        """
        Creates the database collection for DataGerry

        Raises:
            CollectionInitError: When a collection could not be initialised
        """
        try:
            detected_database = self.dbm.connector.database

            # update framework collections
            for collection in FRAMEWORK_CLASSES:
                try:
                    detected_database.validate_collection(collection.COLLECTION)['valid']
                except CollectionInvalid:
                    self.dbm.create_collection(collection.COLLECTION)
                    # set unique indexes
                    self.dbm.create_indexes(collection.COLLECTION, collection.get_index_keys())
                    LOGGER.info('[UPDATE ROUTINE] Database collection %s was created.', collection.COLLECTION)

            # update user management collections
            for collection in USER_MANAGEMENT_COLLECTION:
                try:
                    detected_database.validate_collection(collection.COLLECTION)['valid']
                except CollectionInvalid:
                    self.dbm.create_collection(collection.COLLECTION)
                    # set unique indexes
                    self.dbm.create_indexes(collection.COLLECTION, collection.get_index_keys())
                    LOGGER.info('[UPDATE ROUTINE] Database collection %s was created.', collection.COLLECTION)
        except Exception as err:
            LOGGER.error("[UPDATE ROUTINE] Database collection validation failed: %s, %s", err, type(err))
            raise CollectionInitError(str(err)) from err


    def update_db_version(self) -> None:
        """
        Checks for exisiting updates and installs them, then updates the value
        for the lastest updater version

        Raises:
            RuntimeError: When the updates could not be applied
        """
        try:
            updater_settings_values = UpdaterModule.__DEFAULT_SETTINGS__
            settings_reader = SettingsReaderManager(self.dbm)

            try:
                updater_settings_values = settings_reader.get_all_values_from_section('updater')
                updater_setting_instance = UpdateSettings(**updater_settings_values)
            except SectionError: #ERROR-FIX (UpdateSettings initialisation is not covered)
                # create updater section if not exist
                settings_writer = SettingsWriterManager(self.dbm)
                updater_setting_instance = UpdateSettings(updater_settings_values['version'])
                settings_writer.write(_id='updater', data=updater_setting_instance.__dict__)

            # start running update files
            updater_setting_instance.run_updates(updater_settings_values.get('version'), settings_reader)

        except Exception as err:
            self.status = UpdateStatus.ERROR
            raise RuntimeError(
                f'Something went wrong during the generation of the updater module. \n Error: {err}'
            ) from err

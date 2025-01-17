# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
"""This class provides the different managers for the API routes"""
import logging
from flask import current_app

from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager import (
    CategoriesManager,
    ObjectsManager,
    LogsManager,
    DocapiTemplatesManager,
    UsersManager,
    UsersSettingsManager,
    GroupsManager,
    MediaFilesManager,
    TypesManager,
    LocationsManager,
    SectionTemplatesManager,
    ObjectLinksManager,
    SecurityManager,
    SettingsReaderManager,
    SettingsWriterManager,
    ReportCategoriesManager,
    ReportsManager,
    WebhooksManager,
    WebhooksEventManager,
)

from cmdb.models.user_model.user import UserModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                ManagerProvider - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class ManagerProvider:
    """
    Provides Managers for stateless API route requests
    """

    @classmethod
    def get_manager(cls, manager_type: ManagerType, request_user: UserModel):
        """Retrieves a manager based on the provided ManagerType and 'cloud_mode' app flag

        Args:
            manager_type (ManagerType): Enum of possible Managers
            request_user (UserModel): The user which is making the API call

        Returns:
            Manager: Returns the manager of the provided ManagerType
        """
        manager_class = cls.__get_manager_class(manager_type)

        if not manager_class:
            LOGGER.error("No manager found for type: %s", manager_type)
            return None

        manager_args = cls.__get_manager_args(request_user)

        return manager_class(*manager_args)


    @staticmethod
    def __get_manager_class(manager_type: ManagerType):
        """
        Returns the appropriate manager class based on the provided ManagerType

        Args:
            manager_type (ManagerType): Enum of possible Managers

        Returns:
            type: The manager class corresponding to the given ManagerType
        """
        manager_classes = {
            ManagerType.CATEGORIES_MANAGER: CategoriesManager,
            ManagerType.OBJECTS_MANAGER: ObjectsManager,
            ManagerType.LOGS_MANAGER: LogsManager,
            ManagerType.DOCAPI_TEMPLATES_MANAGER: DocapiTemplatesManager,
            ManagerType.USERS_MANAGER: UsersManager,
            ManagerType.USERS_SETTINGS_MANAGER: UsersSettingsManager,
            ManagerType.GROUPS_MANAGER: GroupsManager,
            ManagerType.MEDIA_FILES_MANAGER: MediaFilesManager,
            ManagerType.TYPES_MANAGER: TypesManager,
            ManagerType.LOCATIONS_MANAGER: LocationsManager,
            ManagerType.SECTION_TEMPLATES_MANAGER: SectionTemplatesManager,
            ManagerType.OBJECT_LINKS_MANAGER: ObjectLinksManager,
            ManagerType.SETTINGS_READER_MANAGER: SettingsReaderManager,
            ManagerType.SETTINGS_WRITER_MANAGER: SettingsWriterManager,
            ManagerType.SECURITY_MANAGER: SecurityManager,
            ManagerType.REPORT_CATEGORIES_MANAGER: ReportCategoriesManager,
            ManagerType.REPORTS_MANAGER: ReportsManager,
            ManagerType.WEBHOOKS_MANAGER: WebhooksManager,
            ManagerType.WEBHOOKS_EVENT_MANAGER: WebhooksEventManager,
        }

        return manager_classes.get(manager_type)


    @staticmethod
    def __get_manager_args(request_user: UserModel):
        """
        Returns the appropriate arguments for the manager class based on the provided
        ManagerType and 'cloud_mode' flag.

        Args:
            manager_type (ManagerType): Enum of possible Managers
            request_user (UserModel): The user which is making the API call
        Returns:
            tuple: Arguments for the manager class initialization
        """
        common_args = (current_app.database_manager,)

        if current_app.cloud_mode:
            return common_args + (request_user.database,)

        return common_args

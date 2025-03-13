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
This class provides the different managers for the API routes
"""
import logging
from flask import current_app

from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager import (
    CategoriesManager,
    DocapiTemplatesManager,
    LogsManager,
    UsersManager,
    UsersSettingsManager,
    GroupsManager,
    MediaFilesManager,
    TypesManager,
    LocationsManager,
    SectionTemplatesManager,
    ObjectsManager,
    ObjectLinksManager,
    ObjectRelationsManager,
    ObjectRelationLogsManager,
    RelationsManager,
    SecurityManager,
    SettingsReaderManager,
    SettingsWriterManager,
    ReportCategoriesManager,
    ReportsManager,
    WebhooksManager,
    WebhooksEventManager,
    RiskClassManager,
    LikelihoodManager,
    ImpactManager,
    ImpactCategoryManager,
    ProtectionGoalManager,
)

from cmdb.models.user_model import CmdbUser
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
    def get_manager(cls, manager_type: ManagerType, request_user: CmdbUser):
        """Retrieves a manager based on the provided ManagerType and 'cloud_mode' app flag

        Args:
            manager_type (ManagerType): Enum of possible Managers
            request_user (CmdbUser): The user which is making the API call

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
            ManagerType.CATEGORIES: CategoriesManager,
            ManagerType.OBJECTS: ObjectsManager,
            ManagerType.LOGS: LogsManager,
            ManagerType.DOCAPI_TEMPLATES: DocapiTemplatesManager,
            ManagerType.USERS: UsersManager,
            ManagerType.USERS_SETTINGS: UsersSettingsManager,
            ManagerType.GROUPS: GroupsManager,
            ManagerType.MEDIA_FILES: MediaFilesManager,
            ManagerType.TYPES: TypesManager,
            ManagerType.LOCATIONS: LocationsManager,
            ManagerType.SECTION_TEMPLATES: SectionTemplatesManager,
            ManagerType.OBJECT_LINKS: ObjectLinksManager,
            ManagerType.SETTINGS_READER: SettingsReaderManager,
            ManagerType.SETTINGS_WRITER: SettingsWriterManager,
            ManagerType.SECURITY: SecurityManager,
            ManagerType.REPORT_CATEGORIES: ReportCategoriesManager,
            ManagerType.REPORTS: ReportsManager,
            ManagerType.WEBHOOKS: WebhooksManager,
            ManagerType.WEBHOOKS_EVENT: WebhooksEventManager,
            ManagerType.RELATIONS: RelationsManager,
            ManagerType.OBJECT_RELATIONS: ObjectRelationsManager,
            ManagerType.OBJECT_RELATION_LOGS: ObjectRelationLogsManager,
            ManagerType.RISK_CLASS: RiskClassManager,
            ManagerType.LIKELIHOOD: LikelihoodManager,
            ManagerType.IMPACT: ImpactManager,
            ManagerType.IMPACT_CATEGORY: ImpactCategoryManager,
            ManagerType.PROTECTION_GOAL: ProtectionGoalManager,
        }

        return manager_classes.get(manager_type)


    @staticmethod
    def __get_manager_args(request_user: CmdbUser):
        """
        Returns the appropriate arguments for the manager class based on the provided
        ManagerType and 'cloud_mode' flag.

        Args:
            request_user (CmdbUser): The user which is making the API call

        Returns:
            tuple: Arguments for the manager class initialization
        """
        common_args = (current_app.database_manager,)

        if current_app.cloud_mode:
            return common_args + (request_user.database,)

        return common_args

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
"""document"""
#TODO: DOCUMENT-FIX
from cmdb.manager.base_manager import BaseManager
from cmdb.manager.categories_manager import CategoriesManager
from cmdb.manager.docapi_templates_manager import DocapiTemplatesManager
from cmdb.manager.groups_manager import GroupsManager
from cmdb.manager.locations_manager import LocationsManager
from cmdb.manager.logs_manager import LogsManager
from cmdb.manager.media_files_manager import MediaFilesManager
from cmdb.manager.object_links_manager import ObjectLinksManager
from cmdb.manager.objects_manager import ObjectsManager
from cmdb.manager.relations_manager import RelationsManager
from cmdb.manager.report_categories_manager import ReportCategoriesManager
from cmdb.manager.reports_manager import ReportsManager
from cmdb.manager.rights_manager import RightsManager
from cmdb.manager.section_templates_manager import SectionTemplatesManager
from cmdb.manager.security_manager import SecurityManager
from cmdb.manager.settings_reader_manager import SettingsReaderManager
from cmdb.manager.settings_writer_manager import SettingsWriterManager
from cmdb.manager.types_manager import TypesManager
from cmdb.manager.users_manager import UsersManager
from cmdb.manager.users_settings_manager import UsersSettingsManager
from cmdb.manager.webhooks_event_manager import WebhooksEventManager
from cmdb.manager.webhooks_manager import WebhooksManager
# -------------------------------------------------------------------------------------------------------------------- #

__all__ = [
    'BaseManager',
    'CategoriesManager',
    'DocapiTemplatesManager',
    'GroupsManager',
    'LocationsManager',
    'LogsManager',
    'MediaFilesManager',
    'ObjectLinksManager',
    'ObjectsManager',
    'RelationsManager',
    'ReportCategoriesManager',
    'ReportsManager',
    'RightsManager',
    'SectionTemplatesManager',
    'SecurityManager',
    'SettingsReaderManager',
    'SettingsWriterManager',
    'TypesManager',
    'UsersManager',
    'UsersSettingsManager',
    'WebhooksEventManager',
    'WebhooksManager',
]

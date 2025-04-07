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
This module provides all refactored Managers of DataGerry (refactoring still in process)
"""
from cmdb.manager.categories_manager import CategoriesManager
from cmdb.manager.docapi_templates_manager import DocapiTemplatesManager
from cmdb.manager.groups_manager import GroupsManager
from cmdb.manager.locations_manager import LocationsManager
from cmdb.manager.logs_manager import LogsManager
from cmdb.manager.media_files_manager import MediaFilesManager
from cmdb.manager.object_links_manager import ObjectLinksManager
from cmdb.manager.objects_manager import ObjectsManager
from cmdb.manager.object_relations_manager import ObjectRelationsManager
from cmdb.manager.object_relation_logs_manager import ObjectRelationLogsManager
from cmdb.manager.relations_manager import RelationsManager
from cmdb.manager.report_categories_manager import ReportCategoriesManager
from cmdb.manager.reports_manager import ReportsManager
from cmdb.manager.rights_manager import RightsManager
from cmdb.manager.section_templates_manager import SectionTemplatesManager
from cmdb.manager.security_manager import SecurityManager
from cmdb.manager.types_manager import TypesManager
from cmdb.manager.users_manager import UsersManager
from cmdb.manager.webhooks_event_manager import WebhooksEventManager
from cmdb.manager.webhooks_manager import WebhooksManager
from cmdb.manager.extendable_options_manager import ExtendableOptionsManager
from cmdb.manager.object_groups_manager import ObjectGroupsManager
from cmdb.manager.user_settings_manager import UserSettingsManager
from cmdb.manager.persons_manager import PersonsManager
from cmdb.manager.person_groups_manager import PersonGroupsManager

# System Managers
from cmdb.manager.system_manager.settings_manager import SettingsManager

# ISMS Managers
from cmdb.manager.isms_manager.risk_class_manager import RiskClassManager
from cmdb.manager.isms_manager.likelihood_manager import LikelihoodManager
from cmdb.manager.isms_manager.impact_manager import ImpactManager
from cmdb.manager.isms_manager.impact_category_manager import ImpactCategoryManager
from cmdb.manager.isms_manager.protection_goal_manager import ProtectionGoalManager
from cmdb.manager.isms_manager.risk_matrix_manager import RiskMatrixManager
from cmdb.manager.isms_manager.threat_manager import ThreatManager
from cmdb.manager.isms_manager.vulnerability_manager import VulnerabilityManager
from cmdb.manager.isms_manager.risk_manager import RiskManager
from cmdb.manager.isms_manager.control_meassure_manager import ControlMeassureManager
# -------------------------------------------------------------------------------------------------------------------- #

__all__ = [
    'CategoriesManager',
    'DocapiTemplatesManager',
    'GroupsManager',
    'LocationsManager',
    'LogsManager',
    'MediaFilesManager',
    'ObjectLinksManager',
    'ObjectsManager',
    'ObjectRelationsManager',
    'ObjectRelationLogsManager',
    'RelationsManager',
    'ReportCategoriesManager',
    'ReportsManager',
    'RightsManager',
    'SectionTemplatesManager',
    'SecurityManager',
    'SettingsManager',
    'TypesManager',
    'UsersManager',
    'WebhooksEventManager',
    'WebhooksManager',
    'RiskClassManager',
    'LikelihoodManager',
    'ImpactManager',
    'ImpactCategoryManager',
    'ProtectionGoalManager',
    'RiskMatrixManager',
    'ExtendableOptionsManager',
    'ObjectGroupsManager',
    'ThreatManager',
    'VulnerabilityManager',
    'UserSettingsManager',
    'RiskManager',
    'ControlMeassureManager',
    'PersonsManager',
    'PersonGroupsManager',
]

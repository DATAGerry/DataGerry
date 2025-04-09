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
Implementation of DataGerry general system information API routes
"""
import sys
import time
import logging

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager import SettingsManager
from cmdb.manager.system_manager.system_config_reader import SystemConfigReader

from cmdb import __title__, __version__, __runtime__
from cmdb.interface.rest_api.routes.framework_routes.setting_routes import settings_blueprint
from cmdb.interface.route_utils import right_required, insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.blueprints import NestedBlueprint
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.models.user_model import CmdbUser
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

system_blueprint = NestedBlueprint(settings_blueprint, url_prefix='/system')

# -------------------------------------------------------------------------------------------------------------------- #

@system_blueprint.route('/', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_datagerry_information(request_user: CmdbUser):
    """document"""
    #TODO: DOCUMENT-FIX
    settings_manager: SettingsManager = ManagerProvider.get_manager(ManagerType.SETTINGS, request_user)

    try:
        db_version = settings_manager.get_all_values_from_section('updater').get('version')
    except Exception as err:
        LOGGER.warning(err)
        db_version = 0

    datagerry_infos = {
        'title': __title__,
        'version': __version__,
        'db_version': db_version,
        'runtime': (time.time() - __runtime__),
        'starting_parameters': sys.argv
    }

    return DefaultResponse(datagerry_infos).make_response()


@system_blueprint.route('/config/', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@right_required('base.system.view')
def get_config_information(request_user: CmdbUser):
    """document"""
    #TODO: DOCUMENT-FIX
    ssc = SystemConfigReader()

    config_dict = {
        'path': ssc.config_file,
        'properties': []
    }

    for section in ssc.get_sections():
        section_values = []

        for key, value in ssc.get_all_values_from_section(section).items():
            section_values.append([key, value])

        config_dict['properties'].append([section, section_values])

    api_response = DefaultResponse(config_dict)

    if len(config_dict) < 1:
        return api_response.make_response(204)

    return api_response.make_response()


#TODO: ROUTE-FIX (Remove one route)
@system_blueprint.route('/information/', methods=['GET'])
@system_blueprint.route('/information', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@right_required('base.system.view')
def get_system_information():
    """document"""
    #TODO: DOCUMENT-FIX
    system_infos = {
        'platform': sys.platform,
        'python_interpreter': {
            'version': sys.version,
            'path': sys.path
        }
    }

    api_response = DefaultResponse(system_infos)

    return api_response.make_response()

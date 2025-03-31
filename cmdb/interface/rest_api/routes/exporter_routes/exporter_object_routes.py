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
Implementation of all API routes for CmdbObject exports
"""
import logging
from flask import abort, current_app

from cmdb.models.user_model import CmdbUser
from cmdb.framework.exporter.config.exporter_config import ExporterConfig
from cmdb.framework.exporter.writer.base_export_writer import BaseExportWriter
from cmdb.framework.exporter.writer.supported_exporter_extension import SupportedExporterExtension
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.interface.rest_api.responses.response_parameters import CollectionParameters
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.blueprints import APIBlueprint
from cmdb.utils.helpers import load_class
from cmdb.security.acl.permission import AccessControlPermission
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

exporter_blueprint = APIBlueprint('exporter', __name__)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@exporter_blueprint.route('/extensions', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_export_file_types():
    """document"""
    #TODO: DOCUMENT-FIX
    #TODO: ERROR-FIX (try-catch block)
    return DefaultResponse(SupportedExporterExtension().convert_to()).make_response()


@exporter_blueprint.route('/', methods=['GET'])
@exporter_blueprint.parse_collection_parameters(view='native')
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@exporter_blueprint.protect(auth=True, right='base.framework.object.view')
def export_objects(params: CollectionParameters, request_user: CmdbUser):
    """document"""
    #TODO: DOCUMENT-FIX
    try:
        _config = ExporterConfig(parameters=params, options=params.optional)
        _class = 'ZipExportFormat' if params.optional.get('zip', False) in ['true'] \
            else params.optional.get('classname', 'JsonExportFormat')
        exporter_class = load_class('cmdb.framework.exporter.format.' + _class)()

        if current_app.cloud_mode:
            current_app.database_manager.connector.set_database(request_user.database)

        exporter = BaseExportWriter(exporter_class, _config)

        exporter.from_database(current_app.database_manager, request_user, AccessControlPermission.READ)

        return exporter.export()
    except ModuleNotFoundError as err:
        LOGGER.debug("[export_objects] ModuleNotFoundError: %s", err)
        #TODO: ERROR-FIX
        abort(400, "Module not found for export!")
    except Exception as err:
        LOGGER.debug("[export_objects] Exception: %s, Type: %s", err, type(err))
        abort(500, "Internal server error!")

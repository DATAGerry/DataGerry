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
Implementation of all API routes for Object Imports
"""
import json
import logging
from flask import request, abort
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from cmdb.database.database_utils import default
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager import (
    ObjectsManager,
    TypesManager,
    LogsManager,
)

from cmdb.models.object_model import CmdbObject
from cmdb.models.type_model.cmdb_type import CmdbType
from cmdb.models.user_model import CmdbUser
from cmdb.models.log_model.log_action_enum import LogAction
from cmdb.models.log_model.cmdb_object_log import CmdbObjectLog
from cmdb.framework.rendering.cmdb_render import CmdbRender
from cmdb.framework.importer.configs.object_importer_config import ObjectImporterConfig
from cmdb.framework.importer.parser.base_object_parser import BaseObjectParser
from cmdb.framework.importer.responses.importer_object_response import ImporterObjectResponse
from cmdb.framework.importer.helper.importer_helper import (
    load_parser_class,
    load_importer_class,
    load_importer_config_class,
    __OBJECT_IMPORTER__,
    __OBJECT_PARSER__,
    __OBJECT_IMPORTER_CONFIG__,
)
from cmdb.interface.rest_api.routes.importer_routes.import_routes import importer_blueprint
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.interface.route_utils import (
    insert_request_user,
    right_required,
    verify_api_access,
)
from cmdb.interface.blueprints import NestedBlueprint
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.routes.importer_routes.importer_route_utils import (
    get_file_in_request,
    get_element_from_data_request,
    generate_parsed_output,
    verify_import_access,
)

from cmdb.errors.manager import BaseManagerInsertError
from cmdb.errors.security import AccessDeniedError
from cmdb.errors.manager.objects_manager import ObjectsManagerGetError
from cmdb.errors.render import InstanceRenderError
from cmdb.errors.importer import ImportRuntimeError, ParserRuntimeError, ImporterLoadError, ParserLoadError
from cmdb.errors.manager.types_manager import (
    TypesManagerGetError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

importer_object_blueprint = NestedBlueprint(importer_blueprint, url_prefix='/object')

# -------------------------------------------------------------------------------------------------------------------- #
#TODO: ROUTE-FIX (Remove one route)
@importer_object_blueprint.route('/importer/', methods=['GET'])
@importer_object_blueprint.route('/importer', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_importer():
    """document"""
    #TODO: DOCUMENT-FIX
    importer_response = []

    for importer in __OBJECT_IMPORTER__:
        importer_response.append({
            'name': __OBJECT_IMPORTER__.get(importer).FILE_TYPE,
            'content_type': __OBJECT_IMPORTER__.get(importer).CONTENT_TYPE,
            'icon': __OBJECT_IMPORTER__.get(importer).ICON
        })

    api_response = DefaultResponse(importer_response)

    return api_response.make_response()


#TODO: ROUTE-FIX (Remove one route)
@importer_object_blueprint.route('/importer/config/<string:importer_type>/', methods=['GET'])
@importer_object_blueprint.route('/importer/config<string:importer_type>', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_default_importer_config(importer_type):
    """document"""
    #TODO: DOCUMENT-FIX
    try:
        importer: ObjectImporterConfig = __OBJECT_IMPORTER_CONFIG__[importer_type]
    except IndexError:
        abort(404)

    api_response = DefaultResponse({'manually_mapping': importer.MANUALLY_MAPPING})

    return api_response.make_response()


#TODO: ROUTE-FIX (Remove one route)
@importer_object_blueprint.route('/parser/', methods=['GET'])
@importer_object_blueprint.route('/parser', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_parser():
    """document"""
    #TODO: DOCUMENT-FIX
    parser = list(__OBJECT_PARSER__)

    api_response = DefaultResponse(parser)

    return api_response.make_response()


#TODO: ROUTE-FIX (Remove one route)
@importer_object_blueprint.route('/parser/default/<string:parser_type>', methods=['GET'])
@importer_object_blueprint.route('/parser/default/<string:parser_type>/', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_default_parser_config(parser_type: str):
    """document"""
    #TODO: DOCUMENT-FIX
    try:
        parser: BaseObjectParser = __OBJECT_PARSER__[parser_type]
    except IndexError:
        abort(404)

    api_response = DefaultResponse(parser.DEFAULT_CONFIG)

    return api_response.make_response()


#TODO: ROUTE-FIX (Remove one route)
@importer_object_blueprint.route('/parse/', methods=['POST'])
@importer_object_blueprint.route('/parse', methods=['POST'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def parse_objects():
    """document"""
    #TODO: DOCUMENT-FIX
    # TODO: check if request user has the permission 'base.import.object.*'
    # Check if file exists
    try:
        #TODO: REFACTOR-FIX (get_file_in_request-function)
        request_file: FileStorage = get_file_in_request('file', request.files)
    except Exception as err:
        LOGGER.debug("[parse_objects] Exception: %s, Type: %s", err, type(err))
        abort(500, "No file in request!")

    # Load parser config
    try:
        parser_config: dict = get_element_from_data_request('parser_config', request) or {}
    except Exception as err:
        LOGGER.debug("[parse_objects] Exception: %s, Type: %s", err, type(err))
        abort(500, "No parser config!")
    # Load file format
    file_format = request.form.get('file_format', None)

    if not file_format:
        abort(500, "No file format!")

    try:
        parsed_output = generate_parsed_output(request_file, file_format, parser_config).output()
    except (ParserRuntimeError, Exception) as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[parse_objects] Error: %s, Type: %s", err, type(err))
        abort(500, "Could not generate parsed output!")

    api_response = DefaultResponse(parsed_output)

    return api_response.make_response()


@importer_object_blueprint.route('/', methods=['POST'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@insert_request_user
@right_required('base.import.object.*')
def import_objects(request_user: CmdbUser):
    """document"""
    #TODO: DOCUMENT-FIX
    try:
        # Check if file exists
        if not request.files:
            LOGGER.error("[import_objects] No import file!")
            abort(400, 'No import file was provided')

        request_file: FileStorage = get_file_in_request('file', request.files)

        filename = secure_filename(request_file.filename)
        working_file = f'/tmp/{filename}'
        request_file.save(working_file)

        # Load file format
        file_format = request.form.get('file_format', None)

        # Load parser config
        parser_config: dict = get_element_from_data_request('parser_config', request) or {}
        if parser_config == {}:
            LOGGER.info('No parser config was provided - using default parser config')

        # Check for importer config
        importer_config_request: dict = get_element_from_data_request('importer_config', request) or None
        if not importer_config_request:
            LOGGER.error("[import_objects] No import config was provided!")
            abort(400, 'No import config was provided')

        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)
        logs_manager: LogsManager = ManagerProvider.get_manager(ManagerType.LOGS, request_user)

        # Check if type exists
        try:
            type_ = types_manager.get_type(importer_config_request.get('type_id'))

            if type_:
                type_ = CmdbType.from_data(type_)

                if not type_.active:
                    raise AccessDeniedError(f'Objects cannot be created because type `{type_.name}` is deactivated.')
                verify_import_access(request_user, type_, types_manager)
        except AccessDeniedError:
            LOGGER.error("[import_objects] No import config was provided!")
            abort(403, "Access denied for importing objects !")
        except (TypesManagerGetError, Exception) as error:
            #TODO: ERROR-FIX
            LOGGER.error("[import_objects] Exception: %s. Type: %s", error, type(error), exc_info=True)
            abort(400, "Could not import objects !")

        # Load parser
        try:
            parser_class = load_parser_class('object', file_format)
        except ParserLoadError as err:
            #TODO: ERROR-FIX
            LOGGER.error("[import_objects] ParserLoadError: %s", err, exc_info=True)
            abort(406)

        parser = parser_class(parser_config)

        # Load importer config
        try:
            importer_config_class = load_importer_config_class('object', file_format)
        except ImporterLoadError as err:
            #TODO: ERROR-FIX
            LOGGER.error("[import_objects] ImporterLoadError: %s", err, exc_info=True)
            abort(406)
        importer_config = importer_config_class(**importer_config_request)

        # Load importer
        try:
            importer_class = load_importer_class('object', file_format)
        except ImporterLoadError as err:
            #TODO: ERROR-FIX
            LOGGER.error("[import_objects] ImporterLoadError: %s", err, exc_info=True)
            abort(406)
        importer = importer_class(working_file, importer_config, parser, objects_manager, request_user)

        try:
            import_response: ImporterObjectResponse = importer.start_import()
        except ImportRuntimeError as err:
            LOGGER.error("[import_objects] ImportRuntimeError: %s", err, exc_info=True)
            abort(500)
        except AccessDeniedError as err:
            LOGGER.error("[import_objects] AccessDeniedError: %s", err)
            abort(403)
        except Exception as err:
            LOGGER.error("[import_objects-import_response] Exception: %s. Type: %s", err, type(err), exc_info=True)
            abort(500, "Internal server error!")

        # close request file
        request_file.close()

        # log all successful imports
        for message in import_response.success_imports:
            try:
                # get object state of every imported object
                current_type_instance = objects_manager.get_object_type(importer_config_request.get('type_id'))
                current_object = objects_manager.get_object(message.public_id)
                current_object = CmdbObject.from_data(current_object)

                current_object_render_result = CmdbRender(current_object,
                                                        current_type_instance,
                                                        request_user,
                                                        False,
                                                        objects_manager.dbm).result()

                # insert object create log
                log_params = {
                    'object_id': message.public_id,
                    'user_id': request_user.get_public_id(),
                    'user_name': request_user.get_display_name(),
                    'comment': 'Object was imported',
                    'render_state': json.dumps(
                                        current_object_render_result,
                                        default=default).encode('UTF-8'),
                    'version': current_object.version
                }

                logs_manager.insert_log(action=LogAction.CREATE, log_type=CmdbObjectLog.__name__, **log_params)
            except ObjectsManagerGetError as err:
                LOGGER.debug("[import_objects] %s", err)
                abort(404)
            except InstanceRenderError as err:
                #TODO: ERROR-FIX
                LOGGER.error("[import_objects] InstanceRenderError: %s. Type: %s", err, type(err), exc_info=True)
                abort(500)
            except BaseManagerInsertError as err:
                #TODO: ERROR-FIX
                LOGGER.debug("[import_objects] %s", err)

        return DefaultResponse(import_response).make_response()
    except Exception as err:
        LOGGER.error("[import_objects] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Internal server error!")

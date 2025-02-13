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
import logging
import json
from bson import json_util
from flask import abort, request, Response

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager import (
    DocapiTemplatesManager,
    ObjectsManager,
)

from cmdb.framework.docapi.docapi_renderer import DocApiRenderer
from cmdb.framework.docapi.docapi_template.docapi_template import DocapiTemplate
from cmdb.framework.results import IterationResult
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import GetMultiResponse, DefaultResponse
from cmdb.interface.route_utils import insert_request_user, right_required, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.blueprints import APIBlueprint, RootBlueprint
from cmdb.models.user_model import CmdbUser

from cmdb.errors.manager.docapi_templates_manager import (
    DocapiTemplatesManagerInsertError,
    DocapiTemplatesManagerGetError,
    DocapiTemplatesManagerDeleteError,
    DocapiTemplatesManagerUpdateError,
    DocapiTemplatesManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

docapi_blueprint = RootBlueprint('docapi', __name__, url_prefix='/docapi')
docs_blueprint = APIBlueprint('docs', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

#TODO: ROUTE-FIX(remove one route)
@docapi_blueprint.route('/template', methods=['POST'])
@docapi_blueprint.route('/template/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@right_required('base.docapi.template.add')
def create_template(request_user: CmdbUser):
    """
    HTTP `POST` route to insert a DocapiTemplate into the database

    Args:
        `request_user` (CmdbUser): `request_user` (CmdbUser): User requesting this data

    Returns:
        `DefaultResponse`: True if insertion was succesful
    """
    try:
        docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                             request_user)

        add_data_dump = json.dumps(request.json)

        new_tpl_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        new_tpl_data['public_id'] = docapi_manager.get_new_docapi_public_id()
        new_tpl_data['author_id'] = request_user.get_public_id()

        template_instance = DocapiTemplate(**new_tpl_data)

        ack = docapi_manager.insert_template(template_instance)

        api_response = DefaultResponse(ack)

        return api_response.make_response()
    #TODO: ERROR-FIX (Catch proper exceptions)
    except DocapiTemplatesManagerInsertError as err:
        LOGGER.error("[create_template] %s", err, exc_info=True)
        return abort(400, "Could not insert the new template in the database!")
    except Exception as err:
        LOGGER.error("[create_template] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "An error occured when trying to insert the template!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@docs_blueprint.route('/template', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@docs_blueprint.protect(auth=True, right='base.docapi.template.view')
@docs_blueprint.parse_collection_parameters()
def get_templates(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple DocapiTemplates

    Args:
        `params` (CollectionParameters): Filter for requested DocapiTemplates
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `GetMultiResponse`: All the DocapiTemplates matching the CollectionParameters
    """
    try:
        docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                             request_user)

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[DocapiTemplate] = docapi_manager.get_templates(builder_params)

        types = [DocapiTemplate.to_json(type) for type in iteration_result.results]

        api_response = GetMultiResponse(types,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        body=request.method == 'HEAD')

        return api_response.make_response()
    except DocapiTemplatesManagerIterationError as err:
        LOGGER.error("[get_templates] %s", err, exc_info=True)
        return abort(400, "Could not retrieve templates from database!")
    except Exception as err:
        LOGGER.error("[get_templates] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "An error occured when trying to retrieve the templates!")


#TODO: ROUTE-FIX (Remove one route)
@docapi_blueprint.route('/template/by/<string:searchfilter>/', methods=['GET'])
@docapi_blueprint.route('/template/by/<string:searchfilter>', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@right_required('base.docapi.template.view')
def get_template_list_filtered(searchfilter: str, request_user: CmdbUser):
    """
    HTTP `GET` route for getting multiple DocapiTemplates filtered by the searchfilter

    Args:
        `searchfilter` (str): Filter for the DocapiTemplates
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `DefaultResponse`: All DocapiTemplates matching the searchfilter
    """
    try:
        docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                             request_user)
        filterdict = json.loads(searchfilter)

        tpl = docapi_manager.get_templates_by(**filterdict)

        api_response = DefaultResponse(tpl)

        return api_response.make_response()
    except DocapiTemplatesManagerGetError as err:
        LOGGER.error("[get_template_list_filtered] %s", err, exc_info=True)
        return abort(404, f"Could not retrieve template list for filter: {searchfilter}")
    except Exception as err:
        LOGGER.error("[get_template_list_filtered] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "An error occured when trying to retrieve the templates!")


#TODO: ROUTE-FIX (Remove one route)
@docapi_blueprint.route('/template/<int:public_id>/', methods=['GET'])
@docapi_blueprint.route('/template/<int:public_id>', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@right_required('base.docapi.template.view')
def get_template(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET` route for retrieving a single DocapiTemplate with the given public_id

    Args:
        `public_id` (int): public_id of the DocapiTemplate which should be retrieved
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `DefaultResponse`: The requested DocapiTemplate
    """
    try:
        docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                             request_user)

        tpl = docapi_manager.get_template(public_id)

        api_response = DefaultResponse(tpl)

        return api_response.make_response()
    except DocapiTemplatesManagerGetError as err:
        LOGGER.error("[get_template] %s", err, exc_info=True)
        return abort(404, "Could not retrieve the  requested template!")
    except Exception as err:
        LOGGER.error("[get_template] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "An error occured when trying to retrieve the template!")


#TODO: ROUTE-FIX (Remove one route)
@docapi_blueprint.route('/template/name/<string:name>/', methods=['GET'])
@docapi_blueprint.route('/template/name/<string:name>', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@right_required('base.docapi.template.view')
def get_template_by_name(name: str, request_user: CmdbUser):
    """
    HTTP `GET` route for retrieving a single DocapiTemplate with the given name

    Args:
        `name` (str): name of the DocapiTemplate
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `DefaultResponse`: The requested DocapiTemplate
    """
    try:
        docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                                request_user)

        tpl = docapi_manager.get_template_by_name(name=name)

        api_response = DefaultResponse(tpl)

        return api_response.make_response()
    except DocapiTemplatesManagerGetError as err:
        LOGGER.error("[get_template_by_name] %s", err, exc_info=True)
        return abort(404, f"Could not retrieve the template with name:{name}!")
    except Exception as err:
        LOGGER.error("[get_template_by_name] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, f"An error occured when trying to retrieve the template with name:{name}!")


#TODO: ROUTE-FIX (Remove one route)
@docapi_blueprint.route('/template/<int:public_id>/render/<int:object_id>/', methods=['GET'])
@docapi_blueprint.route('/template/<int:public_id>/render/<int:object_id>', methods=['GET'])
@insert_request_user
@right_required('base.framework.object.view')
def render_object_template(public_id: int, object_id: int, request_user: CmdbUser):
    """
    HTTP `GET` route for retrieving a single rendered DocapiTemplate

    Args:
        `public_id (int)`: public_id of DocapiTemplate which should be used
        `object_id (int)`: public_id of CmdbObject should be rendered
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `Response`: The rendered DocapiTemplate with the CmdbObject as a PDF-file
    """
    try:
        docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                                request_user)

        #TODO: DEPENDENCY-FIX (Remove dependency on ObjectsManager)
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

        docapi_renderer = DocApiRenderer(objects_manager, docapi_manager)
        output = docapi_renderer.render_object_template(public_id, object_id)

        return Response(
            output,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=output.pdf"
            }
        )
    except Exception as err:
        LOGGER.error("[render_object_template] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "An error occured when trying to render the template!")

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

#TODO: ROUTE-FIX (Remove one route)
@docapi_blueprint.route('/template', methods=['PUT'])
@docapi_blueprint.route('/template/', methods=['PUT'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@right_required('base.docapi.template.edit')
def update_template(request_user: CmdbUser):
    """
    HTTP `PUT` route for updating a single DocapiTemplate

    Args:
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `DefaultResponse`: The updated DocapiTemplate
    """
    try:
        docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                             request_user)

        new_tpl_data = None
        add_data_dump = json.dumps(request.json)
        new_tpl_data = json.loads(add_data_dump, object_hook=json_util.object_hook)

        update_tpl_instance = DocapiTemplate(**new_tpl_data)

        docapi_manager.update_template(update_tpl_instance)

        api_response = DefaultResponse(update_tpl_instance)

        return api_response.make_response()
    except DocapiTemplatesManagerUpdateError as err:
        LOGGER.error("[update_template] %s", err, exc_info=True)
        return abort(400, "Could not update the template!")
    except Exception as err:
        LOGGER.error("[update_template] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "An error occured when trying to update the template!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

#TODO: ROUTE-FIX (Remove one route)
@docapi_blueprint.route('/template/<int:public_id>/', methods=['DELETE'])
@docapi_blueprint.route('/template/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@right_required('base.docapi.template.delete')
def delete_template(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single DocapiTemplate

    Args:
        `public_id` (int): public_id of the DocapiTemplate which should be deleted
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `DefaultResponse`: True if deletion was successful
    """
    try:
        docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                             request_user)

        ack = docapi_manager.delete_template(public_id)

        api_response = DefaultResponse(ack)

        return api_response.make_response()
    except DocapiTemplatesManagerDeleteError as err:
        LOGGER.error("[delete_template] %s", err, exc_info=True)
        return abort(400, "Could not delete the template!")
    except Exception as err:
        LOGGER.error("[delete_template] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "An error occured when trying to delete the template!")

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
Definition of all routes for CmdbSectionTemplates
"""
import json
import logging
from flask import request, abort
from werkzeug.exceptions import HTTPException

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager import SectionTemplatesManager

from cmdb.models.user_model import CmdbUser
from cmdb.models.section_template_model.cmdb_section_template import CmdbSectionTemplate
from cmdb.framework.results import IterationResult
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.responses.response_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import UpdateSingleResponse, GetMultiResponse, DefaultResponse

from cmdb.errors.database import NoDocumentFoundError
from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerIterationError,
    BaseManagerGetError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

section_template_blueprint = APIBlueprint('section_templates', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@section_template_blueprint.route('/', methods=['POST'])
@section_template_blueprint.parse_request_parameters()
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.add')
def create_section_template(params: dict, request_user: CmdbUser):
    """
    Creates a CmdbSectionTemplate in the database

    Args:
        params (dict): CmdbSectionTemplate parameters
    Returns:
        int: public_id of the created CmdbSectionTemplate
    """
    template_manager: SectionTemplatesManager = ManagerProvider.get_manager(ManagerType.SECTION_TEMPLATES,
                                                                            request_user)

    try:
        params['public_id'] = template_manager.get_next_public_id()
        params['is_global'] = params['is_global'] in ['true', 'True', True]
        params['predefined'] = params['predefined'] in ['true', 'True', True]
        params['fields'] = json.loads(params['fields'])
        params['type'] = 'section'

        created_section_template_id = template_manager.insert_section_template(params)
    except BaseManagerInsertError as err:
        # TODO: ERROR-FIX
        LOGGER.debug("[create_section_template] %s", err)
        abort(400, "Could not create the section template!")
        # TODO: ERROR-FIX
    except Exception as err:
        LOGGER.error("[create_section_template] Exception: %s. Type: %s", err, type(err))
        abort(500, "Internal server error!")

    api_response = DefaultResponse(created_section_template_id)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@section_template_blueprint.route('/', methods=['GET', 'HEAD'])
@section_template_blueprint.parse_collection_parameters(view='native')
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.view')
def get_all_section_templates(params: CollectionParameters, request_user: CmdbUser):
    """Returns all CmdbSectionTemplates based on the params

    Args:
        params (CollectionParameters): Parameters to identify documents in database
    Returns:
        (GetMultiResponse): All CmdbSectionTemplates considering the params
    """
    template_manager: SectionTemplatesManager = ManagerProvider.get_manager(ManagerType.SECTION_TEMPLATES,
                                                                            request_user)

    try:
        builder_params: BuilderParameters = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbSectionTemplate] = template_manager.iterate(builder_params)
        template_list: list[dict] = [template_.__dict__ for template_ in iteration_result.results]

        api_response = GetMultiResponse(template_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')
    except BaseManagerIterationError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_all_section_templates] %s", err)
        abort(400, "Could not retrieve SectionTemplates!")
    except Exception as err:
        LOGGER.error("[get_all_section_templates] Exception: %s. Type: %s", err, type(err))
        abort(500, "Internal Server Error!")

    return api_response.make_response()


@section_template_blueprint.route('/<int:public_id>', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.view')
def get_section_template(public_id: int, request_user: CmdbUser):
    """
    Retrieves the CmdbSectionTemplate with the given public_id
    
    Args:
        public_id (int): public_id of CmdbSectionTemplate which should be retrieved
        request_user (CmdbUser): User which is requesting the CmdbSectionTemplate
    """
    template_manager: SectionTemplatesManager = ManagerProvider.get_manager(ManagerType.SECTION_TEMPLATES,
                                                                            request_user)

    try:
        section_template_instance = template_manager.get_section_template(public_id)
    except BaseManagerGetError as err:
        LOGGER.debug("[get_section_template] %s", err)
        abort(400, f"Could not retrieve SectionTemplate with public_id: {public_id}!")

    if not section_template_instance:
        section_template_instance = []

    api_response = DefaultResponse(section_template_instance)

    return api_response.make_response()


@section_template_blueprint.route('/<int:public_id>/count', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.view')
def get_global_section_template_count(public_id: int, request_user: CmdbUser):
    """
    Retrives the count of types and objects using this global CmdbSectionTemplate

    Args:
        public_id (int): public_id of CmdbSectionTemplate which should be checked
    Returns:
        dict: Dict with counts of types and objects using this global CmdbSectionTemplate
    """
    template_manager: SectionTemplatesManager = ManagerProvider.get_manager(ManagerType.SECTION_TEMPLATES,
                                                                            request_user)

    try:
        instance: CmdbSectionTemplate = template_manager.get_section_template(public_id)
        counts: dict = template_manager.get_global_template_usage_count(instance.name, instance.is_global)

    except BaseManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_section_template] %s", err)
        abort(400, f"Could not retrieve SectionTemplate with public_id: {public_id}!")
    except Exception as err:
        LOGGER.debug("[get_section_template] Exception: %s", err)
        abort(400, "Could not retrive SectionTemplate!")

    api_response = DefaultResponse(counts)

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@section_template_blueprint.route('/', methods=['PUT', 'PATCH'])
@section_template_blueprint.parse_request_parameters()
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.edit')
def update_section_template(params: dict, request_user: CmdbUser):
    """
    Updates a CmdbSectionTemplate

    Args:
        params (dict): updated CmdbSectionTemplate parameters
    Returns:
        _type_: _description_
    """
    template_manager: SectionTemplatesManager = ManagerProvider.get_manager(ManagerType.SECTION_TEMPLATES,
                                                                            request_user)

    try:
        params['is_global'] = params['is_global'] in ('true', 'True')
        params['predefined'] = params['predefined'] in ('true', 'True')
        params['fields'] = json.loads(params['fields'])
        params['public_id'] = int(params['public_id'])
        params['type'] = 'section'

        current_template: CmdbSectionTemplate = template_manager.get_section_template(params['public_id'])

        if current_template:
            result = template_manager.update({'public_id':params['public_id']}, params)

            # Apply changes to all types and objects using the template
            template_manager.handle_section_template_changes(params, current_template)
        else:
            raise NoDocumentFoundError(template_manager.collection)

    except BaseManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_section_template] %s", err)
        abort(404, f"Could not retrieve SectionTemplate with ID: {params['public_id']}!")
    except BaseManagerUpdateError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[update_section_template] %s", err)
        abort(400, f"Could not update SectionTemplate with ID: {params['public_id']}!")
    except NoDocumentFoundError:
        abort(404, "Section template not found!")
    except Exception as err:
        LOGGER.error("[update_section_template] Exception: %s, Type: %s", err, type(err))
        abort(500, "Internal server error!")

    api_response = UpdateSingleResponse(result.acknowledged)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@section_template_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@section_template_blueprint.protect(auth=True, right='base.framework.sectionTemplate.delete')
def delete_section_template(public_id: int, request_user: CmdbUser):
    """
    Delete a CmdbSectionTemplate by its public ID, with appropriate checks and permission handling.

    This function attempts to delete a CmdbSectionTemplate based on the provided public ID. Before deleting, 
    it checks whether the template is predefined (in which case it cannot be deleted) and whether it is 
    a global template that requires additional cleanup.

    Args:
        public_id (int): The public ID of the CmdbSectionTemplate to be deleted.
        request_user (CmdbUser): The user making the request, used for permission validation.

    Returns:
        DefaultResponse: A response indicating whether the deletion was successful
    """
    try:
        template_manager: SectionTemplatesManager = ManagerProvider.get_manager(ManagerType.SECTION_TEMPLATES,
                                                                                request_user)

        template_instance: CmdbSectionTemplate = template_manager.get_section_template(public_id)

        if template_instance.predefined:
            abort(400, "A predefined SectionTemplate is not deletable!")

        if template_instance.is_global:
            template_manager.cleanup_global_section_templates(template_instance.name)

        #TODO: REFACTOR-FIX
        ack: bool = template_manager.delete({'public_id':public_id})

        return DefaultResponse(ack).make_response()
    except HTTPException as http_err:
        raise http_err
    except BaseManagerGetError as err:
        LOGGER.debug("[delete_section_template] %s", err)
        abort(400, f"Could not retrieve SectionTemplate with public_id: {public_id}!")
    except BaseManagerDeleteError as err:
        LOGGER.debug("[delete_section_template] %s", err)
        abort(400, f"Could not delete SectionTemplate with public_id: {public_id}!")
    except Exception as err:
        LOGGER.error("[delete_section_template] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while deleting the SectionTemplate!")

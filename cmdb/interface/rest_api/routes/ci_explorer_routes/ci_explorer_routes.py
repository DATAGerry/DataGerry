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
Implementation of all API routes for CI Explorer
"""
import logging
from flask import abort
from werkzeug.exceptions import HTTPException

from cmdb.manager import ObjectsManager, TypesManager, RelationsManager, ObjectRelationsManager
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsImpact

from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import (
    DefaultResponse,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

ci_explorer_blueprint = APIBlueprint('ci_explorer', __name__)
# -------------------------------------------------------------------------------------------------------------------- #

@ci_explorer_blueprint.route('/tooltip/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def update_tooltip(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update the ci_explorer_tooltip of an CmdbObject from the CI Explorer

    Args:
        public_id (int): public_id of the CmdbObject which should be updated
        data (dict): New tooltip data ({'ci_explorer_tooltip': <string>})
        request_user (CmdbUser): User requesting this data

    Returns:
        DefaultResponse: The Tooltip which was set for the CmdbObject
    """
    try:
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)

        to_update_object: IsmsImpact = objects_manager.get_object(public_id)

        if not to_update_object:
            abort(404, f"The Object with ID:{public_id} was not found!")

        to_update_object['ci_explorer_tooltip'] = data.get('ci_explorer_tooltip')

        objects_manager.update_object(public_id, to_update_object)

        return DefaultResponse(data).make_response()
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        LOGGER.error("[update_tooltip] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, f"An internal server error occured while updating the Tooltip for Object-ID: {public_id}!")


@ci_explorer_blueprint.route('/type_label/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def update_type_label(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update the ci_explorer_label for a CmdbType

    Args:
        public_id (int): public_id of the CmdbType which should be updated
        data (dict): New label data ({'ci_explorer_label': <string>})
        request_user (CmdbUser): User requesting this data

    Returns:
        DefaultResponse: The Label which was set for the CmdbType
    """
    try:
        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)

        to_update_type: IsmsImpact = types_manager.get_type(public_id)

        if not to_update_type:
            abort(404, f"The Type with ID:{public_id} was not found!")

        to_update_type['ci_explorer_label'] = data.get('ci_explorer_label')

        types_manager.update_type(public_id, to_update_type)

        return DefaultResponse(data).make_response()
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        LOGGER.error("[update_type_label] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, f"An internal server error occured while updating the Label for Type-ID: {public_id}!")


@ci_explorer_blueprint.route('/items', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_ci_explorer_nodes_edges(data: dict, request_user: CmdbUser):
    """
    HTTP `GET` route to retrieve Nodes and Edges for the CI Explorer

    Args:
        data (dict): Nodes and edges parameters
        request_user (CmdbUser): User requesting this data

    Returns:
        DefaultResponse: The requested nodes and edges
    """
    try:
        requested_data = {}

        # TODO: add required

        return DefaultResponse(requested_data).make_response()
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        LOGGER.error("[get_ci_explorer_nodes_edges] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving CI Explorer nodes and edges!")

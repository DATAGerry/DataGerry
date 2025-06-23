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
from flask import abort, request
from werkzeug.exceptions import HTTPException

from cmdb.manager import ObjectsManager, TypesManager, RelationsManager, ObjectRelationsManager
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsImpact
from cmdb.models.ci_explorer_model import NodeType

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
def get_ci_explorer_nodes_edges(request_user: CmdbUser):
    """
    HTTP `GET` route to retrieve Nodes and Edges for the CI Explorer

    Expects the following data via request args:
            "target_id" (int): # public_id of target CmdbObject
            "target_type" (str): # Enum with PARENT, CHILD or BOTH
            "with_root" (bool): True # If True then the target Object will be part of the Response

    Args:
        request_user (CmdbUser): User requesting this data

    Returns:
        DefaultResponse: The requested nodes and edges
    """
    try:
        target_id = request.args.get("target_id", type=int)
        target_type = request.args.get("target_type", default="BOTH").upper()
        with_root = request.args.get("with_root", default="false").lower() == "true"

        if target_id is None:
            abort(400, "Missing ID of target Object!")

        if not NodeType.is_valid(target_type):
            abort(
                400, f"Invalid target_type '{target_type}'. Must be one of: {', '.join(NodeType.__members__.keys())}"
            )

        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)
        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)
        relations_manager: RelationsManager = ManagerProvider.get_manager(ManagerType.RELATIONS, request_user)
        object_relations_manager: ObjectRelationsManager = ManagerProvider.get_manager(ManagerType.OBJECT_RELATIONS,
                                                                                       request_user)

        # Retrieve target object & type info for root if needed
        root_object = objects_manager.get_object(target_id) if with_root else None
        root_type_info = types_manager.get_type(root_object['type_id']) if root_object else None

        # Retrieve all object relations where this object is involved (either as parent or child)
        # We want all relations with either parent_id == target_id or child_id == target_id
        object_relations = list(object_relations_manager.find(
            criteria={
                "$or": [
                    {"relation_parent_id": target_id},
                    {"relation_child_id": target_id}
                ]
            }
        ))

        # Load all relations (relation metadata) used by these object_relations
        relation_ids = set(rel['relation_id'] for rel in object_relations)
        relations_list = relations_manager.find(criteria={"public_id": {"$in": list(relation_ids)}})
        relations_by_id = {rel['public_id']: rel for rel in relations_list}

        # Helper: map public_id to object and type
        # We'll need the linked CmdbObjects and their CmdbTypes for nodes
        # Collect all object ids referenced by relations except the root object (we already have it if with_root)
        linked_object_ids = set()
        for orr in object_relations:
            if orr['relation_parent_id'] != target_id:
                linked_object_ids.add(orr['relation_parent_id'])
            if orr['relation_child_id'] != target_id:
                linked_object_ids.add(orr['relation_child_id'])

        # Get all linked objects
        linked_objects_cursor = objects_manager.find(criteria={"public_id": {"$in": list(linked_object_ids)}})
        linked_objects = {obj['public_id']: obj for obj in linked_objects_cursor}

        # Get all linked types for those objects + root type if needed
        type_ids = {obj['type_id'] for obj in linked_objects.values()}
        if root_type_info:
            type_ids.add(root_type_info['public_id'])
        types_list = types_manager.find(criteria={"public_id": {"$in": list(type_ids)}})
        types_by_id = {t['public_id']: t for t in types_list}

        # Helper function to get title based on type ci_explorer_label
        def get_title(obj: dict, obj_type: dict):
            label_field_name = obj_type.get('ci_explorer_label')
            if not label_field_name:
                return None
            # Find the value of the field in obj['fields'] by field name
            f: dict
            for f in obj.get('fields', []):
                if f.get('name') == label_field_name:
                    return f.get('value')
            return None

        # Prepare response containers
        response = {}
        if with_root and root_object and root_type_info:
            root_title = get_title(root_object, root_type_info)
            response['root_node'] = {
                "linked_object": root_object,
                "title": root_title,
                "type_info": {
                    "type_id": root_type_info['public_id'],
                    "label": root_type_info['label'],
                    "icon": root_type_info.get('icon'),
                    "fields": root_type_info.get('fields', {}),
                },
                "relation_color": None,  # Root has no relation_color since no relation in this context
            }

        # Initialize children/parents lists
        response['children_nodes'] = []
        response['child_edges'] = []
        response['parent_nodes'] = []
        response['parent_edges'] = []

        # Iterate over object relations and create nodes and edges
        for obj_rel in object_relations:
            relation = relations_by_id.get(obj_rel['relation_id'])
            if not relation:
                # Skip if relation info missing
                continue

            # Determine if target is parent or child in this relation
            is_parent = obj_rel['relation_parent_id'] == target_id
            is_child = obj_rel['relation_child_id'] == target_id

            # Determine linked object id and type for the opposite end of the relation
            if is_parent:
                linked_id = obj_rel['relation_child_id']
                linked_type_id = obj_rel['relation_child_type_id']
                relation_color = relation.get('relation_color_parent')
                edge_from = target_id
                edge_to = linked_id
                edge_relation_name = relation.get('relation_name_parent')
                edge_relation_icon = relation.get('relation_icon_parent')
            elif is_child:
                linked_id = obj_rel['relation_parent_id']
                linked_type_id = obj_rel['relation_parent_type_id']
                relation_color = relation.get('relation_color_child')
                edge_from = linked_id
                edge_to = target_id
                edge_relation_name = relation.get('relation_name_child')
                edge_relation_icon = relation.get('relation_icon_child')
            else:
                # Should not happen since we filtered relations involving target_id
                continue

            linked_object = linked_objects.get(linked_id)
            linked_type: dict = types_by_id.get(linked_type_id)

            if not linked_object or not linked_type:
                # Missing data, skip this relation
                continue

            # Build node title
            node_title = get_title(linked_object, linked_type)

            node_dict = {
                "linked_object": linked_object,
                "title": node_title,
                "type_info": {
                    "type_id": linked_type['public_id'],
                    "label": linked_type['label'],
                    "icon": linked_type.get('icon'),
                    "fields": linked_type.get('fields', {}),
                },
                "relation_color": relation_color
            }

            # Build edge metadata
            edge_dict = {
                "from": edge_from,
                "to": edge_to,
                "metadata": {
                    "relation_id": relation['public_id'],
                    "relation_name": relation['relation_name'],
                    "relation_label": edge_relation_name,
                    "relation_icon": edge_relation_icon,
                    "relation_color": relation_color,
                }
            }

            # Append node & edge to children or parents depending on relation direction
            if is_parent:
                # The linked object is child
                response['children_nodes'].append(node_dict)
                response['child_edges'].append(edge_dict)
            elif is_child:
                # The linked object is parent
                response['parent_nodes'].append(node_dict)
                response['parent_edges'].append(edge_dict)

        # Ensure keys exist even if empty (except root_node when with_root is False)
        if 'root_node' not in response and with_root:
            response['root_node'] = None
        for key in ['children_nodes', 'child_edges', 'parent_nodes', 'parent_edges']:
            if key not in response:
                response[key] = []

        return DefaultResponse(response).make_response()
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        LOGGER.error("[get_ci_explorer_nodes_edges] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving CI Explorer nodes and edges!")

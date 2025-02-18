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
Implementation of all API routes for CmdbRelations
"""
import logging
from flask import request, abort

from cmdb.manager import RelationsManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.relation_model import CmdbRelation
from cmdb.framework.results import IterationResult
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import (
    InsertSingleResponse,
    GetMultiResponse,
    GetSingleResponse,
    UpdateSingleResponse,
    DeleteSingleResponse,
)

from cmdb.errors.manager.relations_manager import (
    RelationsManagerInsertError,
    RelationsManagerGetError,
    RelationsManagerIterationError,
    RelationsManagerUpdateError,
    RelationsManagerDeleteError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

relations_blueprint = APIBlueprint('relations', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@relations_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@relations_blueprint.protect(auth=True, right='base.framework.relation.add')
@relations_blueprint.validate(CmdbRelation.SCHEMA)
def insert_relation(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert a CmdbRelation into the database

    Args:
        `data` (CmdbRelation.SCHEMA): Data of the CmdbRelation which should be inserted
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `InsertSingleResponse`: The new CmdbRelation and its public_id
    """
    try:
        relations_manager: RelationsManager = ManagerProvider.get_manager(ManagerType.RELATIONS_MANAGER,
                                                                           request_user)

        result_id: int = relations_manager.insert_relation(data)

        created_relation = relations_manager.get_relation(result_id)

        api_response = InsertSingleResponse(created_relation, result_id)

        return api_response.make_response()
    except RelationsManagerInsertError as err:
        LOGGER.error("[insert_relation] %s", err, exc_info=True)
        return abort(400, "Could not insert the new relation in the database!")
    except RelationsManagerGetError as err:
        LOGGER.error("[insert_relation] %s", err, exc_info=True)
        return abort(404, "Could not retrieve the created relation from the database!")
    except Exception as err:
        LOGGER.error("[insert_relation] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@relations_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@relations_blueprint.protect(auth=True, right='base.framework.relation.view')
@relations_blueprint.parse_collection_parameters()
def get_relations(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple CmdbRelations

    Args:
        `params` (CollectionParameters): Filter for requested CmdbRelations
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `GetMultiResponse`: All the CmdbRelations matching the CollectionParameters
    """
    try:
        body = request.method == 'HEAD'

        relations_manager: RelationsManager = ManagerProvider.get_manager(ManagerType.RELATIONS_MANAGER,
                                                                          request_user)

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbRelation] = relations_manager.iterate(builder_params)

        relation_list = [CmdbRelation.to_json(relation) for relation in iteration_result.results]

        api_response = GetMultiResponse(relation_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)

        return api_response.make_response()
    except RelationsManagerIterationError as err:
        LOGGER.error("[get_relations] %s", err, exc_info=True)
        return abort(400, "Could not retrieve relations from database!")
    except Exception as err:
        LOGGER.error("[get_relations] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


@relations_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@relations_blueprint.protect(auth=True, right='base.framework.relation.view')
def get_relation(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single CmdbRelation

    Args:
        `public_id` (int): public_id of the CmdbRelation
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `GetSingleResponse`: The requested CmdbRelation
    """
    try:
        relations_manager: RelationsManager = ManagerProvider.get_manager(ManagerType.RELATIONS_MANAGER,
                                                                          request_user)

        requested_relation = relations_manager.get_relation(public_id)

        api_response = GetSingleResponse(requested_relation, body = request.method == 'HEAD')

        return api_response.make_response()
    except RelationsManagerGetError as err:
        LOGGER.error("[get_relation] %s", err, exc_info=True)
        return abort(404, "Could not retrieve the requested relation from the database!")
    except Exception as err:
        LOGGER.error("[get_relation] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@relations_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@relations_blueprint.protect(auth=True, right='base.framework.relation.edit')
@relations_blueprint.validate(CmdbRelation.SCHEMA)
def update_relation(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single CmdbRelation

    Args:
        `public_id` (int): public_id of the CmdbRelation which should be updated
        `data` (CmdbRelation.SCHEMA): New CmdbRelation data
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `UpdateSingleResponse`: The new data of the CmdbRelation
    """
    try:
        relations_manager: RelationsManager = ManagerProvider.get_manager(ManagerType.RELATIONS_MANAGER,
                                                                          request_user)

        relation = CmdbRelation.from_data(data)

        relations_manager.update_relation(public_id, relation)

        api_response = UpdateSingleResponse(result=data)

        return api_response.make_response()
    except RelationsManagerUpdateError as err:
        LOGGER.error("[update_relation] %s", err, exc_info=True)
        return abort(400, "Could not update the relation!")
    except Exception as err:
        LOGGER.error("[update_relation] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@relations_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@relations_blueprint.protect(auth=True, right='base.framework.relation.delete')
def delete_relation(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single CmdbRelation

    Args:
        `public_id` (int): public_id of the CmdbRelation which should be deleted
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `DeleteSingleResponse`: The deleted CmdbRelation data
    """
    try:
        relations_manager: RelationsManager = ManagerProvider.get_manager(ManagerType.RELATIONS_MANAGER,
                                                                           request_user)

        relation_instance = relations_manager.get_relation(public_id)
        relations_manager.delete_relation(public_id)

        api_response = DeleteSingleResponse(raw=relation_instance)

        return api_response.make_response()
    except RelationsManagerDeleteError as err:
        LOGGER.error("[delete_relation] %s", err, exc_info=True)
        return abort(400, f"Could not delete the relation with the ID:{public_id}")
    except RelationsManagerGetError as err:
        LOGGER.error("[delete_relation] %s", err, exc_info=True)
        return abort(404, "Could not retrieve the relation from the database!")
    except Exception as err:
        LOGGER.error("[delete_relation] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

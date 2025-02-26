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
Implementation of all API routes for CmdbObjectRelationLogs
"""
import logging
from flask import request, abort
from werkzeug.exceptions import HTTPException

from cmdb.manager import ObjectRelationLogsManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.log_model import CmdbObjectRelationLog
from cmdb.framework.results import IterationResult
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import (
    GetMultiResponse,
    GetSingleResponse,
    DeleteSingleResponse,
)

from cmdb.errors.manager.object_relation_logs_manager import (
    ObjectRelationLogsManagerIterationError,
    ObjectRelationLogsManagerGetError,
    ObjectRelationLogsManagerDeleteError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

object_relation_logs_blueprint = APIBlueprint('object_relation_logs', __name__)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@object_relation_logs_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@object_relation_logs_blueprint.protect(auth=True, right='base.framework.objectRelationLog.view')
@object_relation_logs_blueprint.parse_collection_parameters()
def get_cmdb_object_relation_logs(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple CmdbObjectRelationLogs

    Args:
        params (CollectionParameters): Filter for requested CmdbObjectRelationLogs
        request_user (CmdbUser): CmdbUser requesting this data

    Returns:
        GetMultiResponse: All the CmdbObjectRelationLogs matching the CollectionParameters
    """
    try:
        body = request.method == 'HEAD'

        object_relation_logs_manager: ObjectRelationLogsManager = ManagerProvider.get_manager(
                                                            ManagerType.OBJECT_RELATION_LOGS_MANAGER,
                                                            request_user)

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbObjectRelationLog] = object_relation_logs_manager.iterate(builder_params)

        object_relation_logs_list = [CmdbObjectRelationLog.to_json(object_relation_log) for
                                      object_relation_log in iteration_result.results]

        api_response = GetMultiResponse(object_relation_logs_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)

        return api_response.make_response()
    except ObjectRelationLogsManagerIterationError as err:
        LOGGER.error("[get_cmdb_object_relation_logs] %s", err, exc_info=True)
        return abort(400, "Failed to retrieve ObjectRelationLogs from database!")
    except Exception as err:
        LOGGER.error("[get_cmdb_object_relation_logs] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


@object_relation_logs_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@object_relation_logs_blueprint.protect(auth=True, right='base.framework.objectRelationLog.view')
def get_cmdb_object_relation_log(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single CmdbObjectRelationLog

    Args:
        public_id (int): public_id of the CmdbObjectRelationLog
        request_user (CmdbUser): User requesting this data

    Returns:
        GetSingleResponse: The requested CmdbObjectRelationLog
    """
    try:
        object_relation_logs_manager: ObjectRelationLogsManager = ManagerProvider.get_manager(
                                                            ManagerType.OBJECT_RELATION_LOGS_MANAGER,
                                                            request_user)

        requested_object_relation_log = object_relation_logs_manager.get_object_relation_log(public_id)

        if requested_object_relation_log:
            api_response = GetSingleResponse(requested_object_relation_log, body = request.method == 'HEAD')

            return api_response.make_response()

        return abort(404, f"The ObjectRelationLog with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except ObjectRelationLogsManagerGetError as err:
        LOGGER.error("[get_cmdb_object_relation_log] %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the ObjectRelationLog with ID: {public_id} from the database!")
    except Exception as err:
        LOGGER.error("[get_cmdb_object_relation_log] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@object_relation_logs_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@object_relation_logs_blueprint.protect(auth=True, right='base.framework.objectRelationLog.delete')
def delete_object_relation_log(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single CmdbObjectRelationLog

    Args:
        public_id (int): public_id of the CmdbObjectRelationLog which should be deleted
        request_user (CmdbUser): CmdbUser requesting this data

    Returns:
        DeleteSingleResponse: The deleted CmdbObjectRelationLog data
    """
    try:
        object_relation_logs_manager: ObjectRelationLogsManager = ManagerProvider.get_manager(
                                                            ManagerType.OBJECT_RELATION_LOGS_MANAGER,
                                                            request_user)

        to_delete_object_relation_log = object_relation_logs_manager.get_object_relation_log(public_id)

        if to_delete_object_relation_log:
            object_relation_logs_manager.delete_object_relation_log(public_id)

            api_response = DeleteSingleResponse(raw=to_delete_object_relation_log)

            return api_response.make_response()

        return abort(404, f"The ObjectRelationLog with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except ObjectRelationLogsManagerDeleteError as err:
        LOGGER.error("[delete_object_relation_log] %s", err, exc_info=True)
        return abort(400, f"Failed to delete the ObjectRelationLog with ID:{public_id}!")
    except ObjectRelationLogsManagerGetError as err:
        LOGGER.error("[delete_object_relation_log] %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the ObjectRelationLog ID:{public_id} from the database!")
    except Exception as err:
        LOGGER.error("[delete_object_relation_log] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

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
Definition of all routes for Logs
"""
import logging
from flask import request, abort

from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager import LogsManager

from cmdb.models.user_model import CmdbUser
from cmdb.models.log_model.log_action_enum import  LogAction
from cmdb.models.log_model.cmdb_object_log import CmdbObjectLog
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import GetMultiResponse, DefaultResponse
from cmdb.interface.rest_api.responses.response_parameters import CollectionParameters
from cmdb.interface.blueprints import APIBlueprint

from cmdb.errors.manager import BaseManagerIterationError, BaseManagerGetError, BaseManagerDeleteError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

logs_blueprint = APIBlueprint('logs', __name__)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@logs_blueprint.route('/<int:public_id>', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
def get_log(public_id: int, request_user: CmdbUser):
    """
    Retrives a single log from the database

    Args:
        public_id (int): public_id of the requested log
    Returns:
        CmdbObjectLog: The log with the given public_id
    """
    logs_manager: LogsManager = ManagerProvider.get_manager(ManagerType.LOGS, request_user)

    try:
        requested_log: CmdbObjectLog = logs_manager.get_one(public_id)
    except BaseManagerGetError:
        abort(404, "Could not retrieve the requested log from database!")

    return DefaultResponse(requested_log).make_response()


@logs_blueprint.route('/object/exists', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
@logs_blueprint.parse_collection_parameters()
def get_logs_with_existing_objects(params: CollectionParameters, request_user: CmdbUser):
    """
    Retrieves all logs of objects which still exist

    Args:
        params (CollectionParameters): parameters for query
    Returns:
        GetMultiResponse: with all logs of exisiting objects
    """
    logs_manager = ManagerProvider.get_manager(ManagerType.LOGS, request_user)

    try:
        query = logs_manager.query_builder.prepare_log_query()
        builder_params = BuilderParameters(query, params.limit, params.skip, params.sort, params.order)

        object_logs = logs_manager.iterate(builder_params)
        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]

        api_response = GetMultiResponse(logs,
                                        object_logs.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')
    except BaseManagerIterationError as err:
        LOGGER.debug("[get_logs_with_existing_objects] %s", err)
        abort(400, "Could not retrieve existing object logs from database!")

    return api_response.make_response()


@logs_blueprint.route('/object/notexists', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
@logs_blueprint.parse_collection_parameters()
def get_logs_with_deleted_objects(params: CollectionParameters, request_user: CmdbUser):
    """
    Retrieves all logs of objects which are deleted

    Args:
        params (CollectionParameters): parameters for query
    Returns:
        GetMultiResponse: with all logs of deleted objects
    """
    logs_manager = ManagerProvider.get_manager(ManagerType.LOGS, request_user)

    try:
        query = logs_manager.query_builder.prepare_log_query(False)
        builder_params = BuilderParameters(query, params.limit, params.skip, params.sort, params.order)

        object_logs = logs_manager.iterate(builder_params)
        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]

        api_response = GetMultiResponse(logs,
                                        object_logs.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')
    except BaseManagerIterationError as err:
        LOGGER.debug("[get_logs_with_deleted_objects] %s", err)
        abort(400, "Could not retrieve deleted objects logs from database!")

    return api_response.make_response()


@logs_blueprint.route('/object/deleted', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
@logs_blueprint.parse_collection_parameters()
def get_object_delete_logs(params: CollectionParameters, request_user: CmdbUser):
    """
    Retrives all logs of objects being deleted

    Args:
        params (CollectionParameters): filter for documents
    Returns:
        GetMultiResponse: with all object deleted logs
    """
    logs_manager = ManagerProvider.get_manager(ManagerType.LOGS, request_user)

    try:
        query = {
            'log_type': CmdbObjectLog.__name__,
            'action': LogAction.DELETE.value
        }

        builder_params = BuilderParameters(query, params.limit, params.skip, params.sort, params.order)
        object_logs = logs_manager.iterate(builder_params)
        logs = [CmdbObjectLog.to_json(_) for _ in object_logs.results]

        api_response = GetMultiResponse(logs,
                                        object_logs.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')
    except BaseManagerIterationError as err:
        LOGGER.debug("[get_object_delete_logs] %s", err)
        abort(400, "Could not retrieve the deleted object logs from database!")

    return api_response.make_response()


@logs_blueprint.route('/object/<int:object_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
@logs_blueprint.parse_collection_parameters()
def get_logs_by_object(object_id: int, params: CollectionParameters, request_user: CmdbUser):
    """
    Retrieves logs for an object with the given public_id

    Args:
        object_id (int): public_id of the object
        params (CollectionParameters): Filter for documents
    Returns:
        GetMultiResponse: with all logs of the object
    """
    logs_manager = ManagerProvider.get_manager(ManagerType.LOGS, request_user)

    try:
        builder_params = BuilderParameters({'object_id':object_id},
                                           params.limit,
                                           params.skip,
                                           params.sort,
                                           params.order)

        iteration_result = logs_manager.iterate(builder_params)

        logs = [CmdbObjectLog.to_json(_) for _ in iteration_result.results]

        api_response = GetMultiResponse(logs,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')
    except BaseManagerIterationError as err:
        LOGGER.debug("[get_logs_by_object] %s", err)
        abort(400, f"Could not retrieve logs for object with ID:{object_id}!")

    return api_response.make_response()


@logs_blueprint.route('/<int:public_id>/corresponding', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@logs_blueprint.protect(auth=True, right='base.framework.log.view')
def get_corresponding_object_logs(public_id: int, request_user: CmdbUser):
    """
    Get the corresponding log

    Args:
        public_id (int): public_id of log
    Returns:
        dict: object log
    """
    logs_manager: LogsManager = ManagerProvider.get_manager(ManagerType.LOGS, request_user)

    try:
        selected_log: CmdbObjectLog = logs_manager.get_one(public_id)
        query = {
            'log_type': CmdbObjectLog.__name__,
            'object_id': selected_log['object_id'],
            'action': LogAction.EDIT.value,
            '$nor': [{
                'public_id': public_id
            }]
        }

        builder_params = BuilderParameters(query)

        logs = logs_manager.iterate(builder_params)
        corresponding_logs = [CmdbObjectLog.to_json(log) for log in logs.results]
    except BaseManagerIterationError as err:
        LOGGER.debug("[get_corresponding_object_logs] %s", err)
        abort(400, f"Could not retrieve corresponding logs for ID:{public_id}!")

    api_response = DefaultResponse(corresponding_logs)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@logs_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@logs_blueprint.protect(auth=True, right='base.framework.log.delete')
def delete_log(public_id: int, request_user: CmdbUser):
    """
    Deletes a single log with the given public_id

    Args:
        public_id (int): public_id of the log which need to be deleted
    Returns:
        bool: deletion success
    """
    logs_manager: LogsManager = ManagerProvider.get_manager(ManagerType.LOGS, request_user)

    try:
        deleted = logs_manager.delete({'public_id':public_id})

        api_response = DefaultResponse(deleted)

        return api_response.make_response()
    except BaseManagerDeleteError as err:
        LOGGER.error("[delete_log] %s", err)
        abort(400, f"Could not delete the log with the ID:{public_id}!")
    except Exception as err:
        LOGGER.debug("[delete_log] Exception: %s. Type: %s", err, type(err))
        abort(500, f"Could not delete the log with the ID:{public_id}!")

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
Implementation of all API routes for CmdbWebhooks
"""
import logging
from ast import literal_eval
from flask import abort, request

from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager import WebhooksManager

from cmdb.models.user_model import CmdbUser
from cmdb.models.webhook_model.cmdb_webhook_model import CmdbWebhook
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import DefaultResponse, GetMultiResponse, UpdateSingleResponse
from cmdb.interface.rest_api.responses.response_parameters import CollectionParameters
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerIterationError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
)
from cmdb.errors.database import NoDocumentFoundError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

webhook_blueprint = APIBlueprint('webhooks', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@webhook_blueprint.route('/', methods=['POST'])
@webhook_blueprint.parse_request_parameters()
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def create_webhook(params: dict, request_user: CmdbUser):
    """
    Creates a CmdbWebhook in the database

    Args:
        params (dict): CmdbWebhook parameters
    Returns:
        int: public_id of the created CmdbWebhook
    """
    webhooks_manager: WebhooksManager = ManagerProvider.get_manager(ManagerType.WEBHOOKS, request_user)

    try:
        params['public_id'] = webhooks_manager.get_next_public_id()
        params['event_types'] = literal_eval(params['event_types'])
        params['active'] = params['active'] in ["True", "true"]

        new_webhook_id = webhooks_manager.insert_webhook(params)
    except BaseManagerInsertError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[create_webhook] %s", err)
        abort(400, "Could not create the Webhook!")
    except Exception as err:
        LOGGER.debug("[create_webhook] Exception: %s, Type: %s", err, type(err))

    api_response = DefaultResponse(new_webhook_id)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@webhook_blueprint.route('/<int:public_id>', methods=['GET'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_webhook(public_id: int, request_user: CmdbUser):
    """
    Retrieves the CmdbWebhook with the given public_id
    
    Args:
        public_id (int): public_id of CmdbWebhook which should be retrieved
        request_user (CmdbUser): User which is requesting the CmdbWebhook
    """
    webhooks_manager: WebhooksManager = ManagerProvider.get_manager(ManagerType.WEBHOOKS, request_user)

    try:
        requested_webhook = webhooks_manager.get_webhook(public_id)
    except BaseManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_webhook] %s", err)
        abort(400, f"Could not retrieve Webhook with ID: {public_id}!")

    api_response = DefaultResponse(requested_webhook)

    return api_response.make_response()


@webhook_blueprint.route('/', methods=['GET', 'HEAD'])
@webhook_blueprint.parse_collection_parameters()
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def get_webhooks(params: CollectionParameters, request_user: CmdbUser):
    """
    Returns all CmdbWebhooks based on the params

    Args:
        params (CollectionParameters): Parameters to identify documents in database
    Returns:
        (GetMultiResponse): All CmdbWebhooks considering the params
    """
    webhooks_manager: WebhooksManager = ManagerProvider.get_manager(ManagerType.WEBHOOKS, request_user)

    try:
        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbWebhook] = webhooks_manager.iterate(builder_params)
        webhook_list: list[dict] = [webhook_.__dict__ for webhook_ in iteration_result.results]

        api_response = GetMultiResponse(webhook_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        request.method == 'HEAD')
    except BaseManagerIterationError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[get_webhooks] %s", err)
        abort(400, "Could not retrieve CmdbWebhooks!")

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@webhook_blueprint.route('/<int:public_id>', methods=['PUT','PATCH'])
@webhook_blueprint.parse_request_parameters()
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def update_webhook(params: dict, request_user: CmdbUser):
    """
    Updates a CmdbWebhook

    Args:
        params (dict): updated CmdbWebhook parameters
    Returns:
        UpdateSingleResponse: Response with UpdateResult
    """
    webhooks_manager: WebhooksManager = ManagerProvider.get_manager(ManagerType.WEBHOOKS, request_user)

    try:
        params['public_id'] = int(params['public_id'])
        params['event_types'] = literal_eval(params['event_types'])
        params['active'] = params['active'] in ["True", "true"]

        current_webhook = webhooks_manager.get_webhook(params['public_id'])

        if current_webhook:
            #TODO: REFACTOR-FIX
            webhooks_manager.update({'public_id': params['public_id']}, params)
            current_webhook = webhooks_manager.get_webhook(params['public_id'])
        else:
            raise NoDocumentFoundError(webhooks_manager.collection)

    except BaseManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[update_webhook] %s", err)
        abort(400, f"Could not retrieve CmdbWebhook with ID: {params['public_id']}!")
    except BaseManagerUpdateError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[update_webhook] %s", err)
        abort(400, f"Could not update CmdbWebhook with ID: {params['public_id']}!")
    except NoDocumentFoundError:
        abort(404, "Webhook not found!")
    except Exception as err:
        LOGGER.debug("[update_webhook] Exception: %s, Type: %s", err, type(err))
        abort(400, "Something went wrong during updating the Webhook!")

    api_response = UpdateSingleResponse(current_webhook.__dict__)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@webhook_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def delete_webhook(public_id: int, request_user: CmdbUser):
    """
    Deletes the CmdbWebhook with the given public_id
    
    Args:
        public_id (int): public_id of CmdbWebhook which should be retrieved
        request_user (CmdbUser): User which is requesting the CmdbWebhook
    """
    webhooks_manager: WebhooksManager = ManagerProvider.get_manager(ManagerType.WEBHOOKS, request_user)

    try:
        webhook_instance: CmdbWebhook = webhooks_manager.get_webhook(public_id)

        if not webhook_instance:
            abort(400, f"Could not retrieve Webhook with ID: {public_id}!")

        #TODO: REFACTOR-FIX
        ack: bool = webhooks_manager.delete({'public_id':public_id})
    except BaseManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_webhook] %s", err)
        abort(400, f"Could not retrieve Webhook with ID: {public_id}!")
    except BaseManagerDeleteError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[delete_webhook] %s", err)
        abort(400, f"Could not delete Webhook with ID: {public_id}!")

    api_response = DefaultResponse(ack)

    return api_response.make_response()

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
This module contains the implementation of the WebhooksManager
"""
import logging
import json
from datetime import datetime, timezone
import requests

from cmdb.database import MongoDatabaseManager
from cmdb.database.database_utils import default
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.base_manager import BaseManager
from cmdb.manager import WebhooksEventManager

from cmdb.models.webhook_model.cmdb_webhook_model import CmdbWebhook
from cmdb.models.webhook_model.webhook_event_type_enum import WebhookEventType
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import BaseManagerInsertError, BaseManagerGetError, BaseManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                WebhooksManager - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class WebhooksManager(BaseManager):
    """
    The WebhooksManager handles the interaction between the Webhooks-API and the database
    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, database:str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            dbm (MongoDatabaseManager): Database connection
        """
        if database:
            dbm.connector.set_database(database)

        self.webhooks_event_manager = WebhooksEventManager(dbm)

        super().__init__(CmdbWebhook.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_webhook(self, data: dict) -> int:
        """
        Inserts a single CmdbWebhook in the database

        Args:
            data (dict): Data of the new CmdbWebhook

        Returns:
            int: public_id of the newly created CmdbWebhook
        """
        try:
            new_webhook = CmdbWebhook(**data)

            ack = self.insert(new_webhook.__dict__)

            return ack
            #TODO: ERROR-FIX
        except Exception as err:
            raise BaseManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_webhook(self, public_id: int) -> CmdbWebhook:
        """
        Retrives a CmdbWebhook from the database with the given public_id

        Args:
            public_id (int): public_id of the CmdbWebhook which should be retrieved
        Raises:
            BaseManagerGetError: Raised if the CmdbWebhook could not be retrieved
        Returns:
            CmdbWebhook: The requested CmdbWebhook if it exists, else None
        """
        try:
            requested_webhook = self.get_one(public_id)
        except Exception as err:
            #TODO: ERROR-FIX
            raise BaseManagerGetError(f"Webhook with ID: {public_id}! 'GET' Error: {err}") from err

        if requested_webhook:
            requested_webhook = CmdbWebhook.from_data(requested_webhook)

            return requested_webhook

        #TODO: ERROR-FIX
        raise BaseManagerGetError(f'Webhook with ID: {public_id} not found!')


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbWebhook]:
        """
        Performs an aggregation on the database

        Args:
            builder_params (BuilderParameters): Contains input to identify the target of action

        Raises:
            BaseManagerIterationError: Raised when something goes wrong during the aggregate part
            BaseManagerIterationError: Raised when something goes wrong during the building of the IterationResult
        Returns:
            IterationResult[CmdbWebhook]: Result which matches the Builderparameters
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            iteration_result: IterationResult[CmdbWebhook] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbWebhook)

            return iteration_result
        except Exception as err:
            #TODO: ERROR-FIX
            raise BaseManagerIterationError(err) from err

# ------------------------------------------------------ HELPERS ----------------------------------------------------- #

    def send_webhook_event(self,
                           operation: WebhookEventType = None,
                           object_before: dict = None,
                           object_after: dict = None,
                           changes: dict = None):
        """document"""
        #TODO: DOCUMENT-FIX
        builder_params = BuilderParameters({})
        webhooks: IterationResult[CmdbWebhook] = self.iterate(builder_params).results

        try:
            if len(webhooks) > 0:
                # Check all webhooks
                webhook: CmdbWebhook
                for webhook in webhooks:
                    # Check if operation is registered in the webhook
                    if operation in webhook.event_types:
                        webhook_url = webhook.url

                        payload = self.build_payload(operation, object_before, object_after, changes)

                        response: requests.Response = requests.post(
                            webhook_url,
                            data=json.dumps(payload, default=default, ensure_ascii=False, indent=2),
                            headers={'Content-Type': 'application/json'},
                            timeout=3,
                        )

                        payload['public_id'] = self.webhooks_event_manager.get_next_public_id()
                        payload['webhook_id'] = webhook.public_id
                        payload['response_code'] = response.status_code
                        payload['status'] = response.status_code == 200

                        self.webhooks_event_manager.insert_webhook_event(payload)
        except Exception as err:
            LOGGER.debug("[send_webhook_event] Exception: %s, Type: %s", err, type(err))


    def build_payload(self,
                      operation: WebhookEventType,
                      object_before: dict,
                      object_after:dict,
                      changes: dict = None) -> dict:
        """document"""
        #TODO: DOCUMENT-FIX
        payload = {}

        payload['event_time'] = datetime.now(timezone.utc)
        payload['operation'] = operation
        payload['object_before'] = object_before
        payload['object_after'] = object_after
        payload['changes'] = changes

        return payload

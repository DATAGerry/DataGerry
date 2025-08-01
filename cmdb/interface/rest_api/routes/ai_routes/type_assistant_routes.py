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
Definition of all routes for the Type Assistant
"""
import logging
from flask import abort, request

from werkzeug.exceptions import HTTPException

from cmdb.models.user_model import CmdbUser

from cmdb.interface.rest_api.ai_models.gemini_model import gemini_model
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.responses import DefaultResponse
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

type_assistant_blueprint = APIBlueprint('type_assistant', __name__)
# -------------------------------------------------------------------------------------------------------------------- #

@type_assistant_blueprint.route('/message', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
def send_message_ai(request_user: CmdbUser):
    """
    HTTP `POST` route to interact with Gemini AI

    Args:
        data (dict): User message to AI ({'message': <string>})
        request_user (CmdbUser): User requesting this data

    Returns:
        DefaultResponse: The response from the AI
    """
    try:
        user_message: dict = request.get_json()
        user_message = user_message.get('message')

        # LOGGER.debug(f"user_message: {user_message}")

        if not user_message:
            abort(400, "No message provided!")

        response = gemini_model.generate_content(user_message)

        # LOGGER.debug(f"response text: {response.text}")
        return DefaultResponse(response.text).make_response()
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        LOGGER.error("[send_message_ai] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while interacting with the AI!")

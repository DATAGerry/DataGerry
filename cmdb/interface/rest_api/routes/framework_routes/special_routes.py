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
Implementation of all API routes for DataGerry Assistant
"""
import logging
from flask import abort
from werkzeug.exceptions import HTTPException

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager import (
    ObjectsManager,
    TypesManager,
    CategoriesManager,
)

from cmdb.models.user_model import CmdbUser
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.blueprints import RootBlueprint
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.framework.datagerry_assistant.profile_assistant import ProfileAssistant

from cmdb.errors.manager.categories_manager import CategoriesManagerGetError
from cmdb.errors.manager.types_manager import TypesManagerGetError
from cmdb.errors.manager.objects_manager import ObjectsManagerGetError
from cmdb.errors.dg_assistant.dg_assistant_errors import ProfileCreationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

special_blueprint = RootBlueprint('special_rest', __name__, url_prefix='/special')

# -------------------------------------------------------------------------------------------------------------------- #

@special_blueprint.route('/intro', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@insert_request_user
def show_datagerry_assistant(request_user: CmdbUser):
    """
    Checks if the DataGerry assistant should be displayed when starting DataGerry

    Returns:
        DefaultResponse: True if there are no types, categories and objects in the database else False
    """
    try:
        categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES,
                                                                            request_user)
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)
        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)

        categories_total = categories_manager.count_categories()
        types_total = types_manager.count_types()
        objects_total = objects_manager.count_objects()

        show_assistant = types_total == 0 and categories_total == 0 and objects_total == 0

        return DefaultResponse(show_assistant).make_response()
    except (CategoriesManagerGetError, TypesManagerGetError, ObjectsManagerGetError) as err:
        LOGGER.error("[show_datagerry_assistant] Error: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Failed to check prerequisites to display DataGerry Assistant!")
    except Exception as err:
        LOGGER.error("[show_datagerry_assistant] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Internal server error!")


@special_blueprint.route('/profiles', methods=['POST'])
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@special_blueprint.parse_assistant_parameters()
@insert_request_user
def create_initial_profiles(data: str, request_user: CmdbUser):
    """
    Creates all profiles selected in the assistant

    Args:
        data (str): profile string seperated by '#'

    Returns:
        _type_: list of created public_ids of types
    """
    try:
        categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES,
                                                                            request_user)
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)
        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)

        profiles = data['data'].split('#')

        categories_total = categories_manager.count_categories()
        types_total = types_manager.count_types()
        objects_total = objects_manager.count_objects()

        # Only execute if there are no categories, types and objects in the database
        if categories_total > 0 or types_total > 0 or objects_total > 0:
            abort(400, "There are objects, types, or categories in the database which prevents this action!")

        profile_assistant = ProfileAssistant(categories_manager)
        created_ids = profile_assistant.create_profiles(profiles)

        return DefaultResponse(created_ids).make_response()
    except HTTPException as http_err:
        raise http_err
    except ProfileCreationError as err:
        LOGGER.error("[create_initial_profiles] Error: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Failed to create initial profiles!")
    except (CategoriesManagerGetError, TypesManagerGetError, ObjectsManagerGetError) as err:
        LOGGER.error("[create_initial_profiles] Error: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Failed to check prerequisites if the DataGerry Assistant can be executed!")
    except Exception as err:
        LOGGER.error("[create_initial_profiles] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Internal server error!")

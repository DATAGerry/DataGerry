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
Implementation of all API routes for CmdbExtendableOptions
"""
import logging
from flask import request, abort
from werkzeug.exceptions import HTTPException

from cmdb.manager import (
    ExtendableOptionsManager,
    ThreatManager,
    VulnerabilityManager,
    ObjectGroupsManager,
)

from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.extendable_option_model import CmdbExtendableOption, OptionType

from cmdb.framework.results import IterationResult
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses.response_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import (
    InsertSingleResponse,
    GetMultiResponse,
    GetSingleResponse,
    UpdateSingleResponse,
    DeleteSingleResponse,
)

from cmdb.errors.manager.extendable_options_manager import (
    ExtendableOptionsManagerInsertError,
    ExtendableOptionsManagerGetError,
    ExtendableOptionsManagerUpdateError,
    ExtendableOptionsManagerDeleteError,
    ExtendableOptionsManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

extendable_option_blueprint = APIBlueprint('extendable_options', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@extendable_option_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@extendable_option_blueprint.protect(auth=True, right='base.framework.extendableOption.add')
@extendable_option_blueprint.validate(CmdbExtendableOption.SCHEMA)
def insert_cmdb_extendable_option(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert an CmdbExtendableOption into the database

    Args:
        data (CmdbExtendableOption.SCHEMA): Data of the CmdbExtendableOption which should be inserted
        request_user (CmdbUser): User requesting this data

    Returns:
        InsertSingleResponse: The new CmdbExtendableOption and its public_id
    """
    try:
        extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(
                                                                    ManagerType.EXTENDABLE_OPTIONS,
                                                                    request_user
                                                                )
        if data.get('predefined'):
            abort(400, "Predefined ExtendableOptions cannot be created via API!")


        # Validate the OptionType
        if not OptionType.is_valid(data.get('option_type')):
            abort(400, f"Invalid OptionType provided: {data.get('option_type')}")

        # Validate that the ExtendableOption does not exist
        existing_extendable_option = extendable_options_manager.get_one_by(data)

        if existing_extendable_option:
            abort(400, f"An Option with the value already exists: {data.get('value')}")

        result_id: int = extendable_options_manager.insert_extendable_option(data)

        created_extendable_option: dict = extendable_options_manager.get_extendable_option(result_id)

        if not created_extendable_option:
            abort(404, "Could not retrieve the created ExtendableOption from the database!")

        return InsertSingleResponse(created_extendable_option, result_id).make_response()
    except HTTPException as http_err:
        raise http_err
    except ExtendableOptionsManagerInsertError as err:
        LOGGER.error("[insert_cmdb_extendable_option] ExtendableOptionsManagerInsertError: %s", err, exc_info=True)
        abort(400, "Could not insert the new ExtendableOption in the database!")
    except ExtendableOptionsManagerGetError as err:
        LOGGER.error("[insert_cmdb_extendable_option] ExtendableOptionsManagerGetError: %s", err, exc_info=True)
        abort(400, "Failed to retrieve the created ExtendableOption from the database!")
    except Exception as err:
        LOGGER.error("[insert_cmdb_extendable_option] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Internal server error!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@extendable_option_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@extendable_option_blueprint.protect(auth=True, right='base.framework.extendableOption.view')
@extendable_option_blueprint.parse_collection_parameters()
def get_cmdb_extendable_options(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple CmdbExtendableOptions

    Args:
        params (CollectionParameters): Filter for requested CmdbExtendableOptions
        request_user (CmdbUser): User requesting this data

    Returns:
        GetMultiResponse: All the CmdbExtendableOptions matching the CollectionParameters
    """
    try:
        body = request.method == 'HEAD'

        extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(
                                                                    ManagerType.EXTENDABLE_OPTIONS,
                                                                    request_user
                                                                )

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbExtendableOption] = extendable_options_manager.iterate(builder_params)
        extendable_option_list = [CmdbExtendableOption.to_json(extendable_option) for extendable_option
                                  in iteration_result.results]

        api_response = GetMultiResponse(extendable_option_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)

        return api_response.make_response()
    except ExtendableOptionsManagerIterationError as err:
        LOGGER.error("[get_cmdb_extendable_options] ExtendableOptionsManagerIterationError: %s", err, exc_info=True)
        abort(400, "Failed to retrieve ExtendableOptions from the database!")
    except Exception as err:
        LOGGER.error("[get_cmdb_extendable_options] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Internal server error!")


@extendable_option_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@extendable_option_blueprint.protect(auth=True, right='base.framework.extendableOption.view')
def get_cmdb_extendable_option(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single CmdbExtendableOption

    Args:
        public_id (int): public_id of the CmdbExtendableOption
        request_user (CmdbUser): User requesting this data

    Returns:
        GetSingleResponse: The requested CmdbExtendableOption
    """
    try:
        extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(
                                                                    ManagerType.EXTENDABLE_OPTIONS,
                                                                    request_user
                                                                )

        extendable_option = extendable_options_manager.get_extendable_option(public_id)

        if extendable_option:
            return GetSingleResponse(extendable_option, body = request.method == 'HEAD').make_response()

        abort(404, f"The ExtendableOption with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except ExtendableOptionsManagerGetError as err:
        LOGGER.error("[get_cmdb_extendable_option] ExtendableOptionsManagerGetError: %s", err, exc_info=True)
        abort(400, f"Failed to retrieve the ExtendableOption with ID: {public_id} from the database!")
    except Exception as err:
        LOGGER.error("[get_cmdb_extendable_option] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@extendable_option_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@extendable_option_blueprint.protect(auth=True, right='base.framework.extendableOption.edit')
@extendable_option_blueprint.validate(CmdbExtendableOption.SCHEMA)
def update_cmdb_extendable_option(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single CmdbExtendableOption

    Args:
        public_id (int): public_id of the CmdbExtendableOption which should be updated
        data (CmdbExtendableOption.SCHEMA): New CmdbExtendableOption data
        request_user (CmdbUser): User requesting this data

    Returns:
        UpdateSingleResponse: The new data of the CmdbExtendableOption
    """
    try:
        extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(
                                                                    ManagerType.EXTENDABLE_OPTIONS,
                                                                    request_user
                                                                )
        # Validate the OptionType
        if not OptionType.is_valid(data.get('option_type')):
            abort(400, f"Invalid OptionType provided: {data.get('option_type')}")

        to_update_extendable_option = extendable_options_manager.get_extendable_option(public_id)

        if not to_update_extendable_option:
            abort(404, f"The ExtendableOption with ID:{public_id} was not found!")

        # Predefined cannot be changed
        if data.get('predefined') != to_update_extendable_option['predefined']:
            abort(404, "The 'predefined' property of an ExtendableOption cannot be changed!")

        # Validate that the OptionType is not changed
        if data['option_type'] != to_update_extendable_option['option_type']:
            abort(400, "The OptionType of an ExtendableOption can not be changed!")

        # Validate that the ExtendableOption with the updated values does not exist
        existing_extendable_option = extendable_options_manager.get_one_by({
                                                            'value': data.get('value'),
                                                            'option_type': data.get('option_type')
                                                        })

        if existing_extendable_option:
            abort(400, f"An Option with the value already exists: {data.get('value')}")

        extendable_option = CmdbExtendableOption.from_data(data)

        extendable_options_manager.update_extendable_option(public_id, extendable_option)

        return UpdateSingleResponse(data).make_response()
    except HTTPException as http_err:
        raise http_err
    except ExtendableOptionsManagerGetError as err:
        LOGGER.error("[update_cmdb_extendable_option] ExtendableOptionsManagerGetError: %s", err, exc_info=True)
        abort(400, f"Failed to retrieve the ExtendableOption with ID: {public_id} from the database!")
    except ExtendableOptionsManagerUpdateError as err:
        LOGGER.error("[update_cmdb_extendable_option] ExtendableOptionsManagerUpdateError: %s", err, exc_info=True)
        abort(400, f"Failed to update the ExtendableOption with ID: {public_id}!")
    except Exception as err:
        LOGGER.error("[update_cmdb_extendable_option] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@extendable_option_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@extendable_option_blueprint.protect(auth=True, right='base.framework.extendableOption.delete')
def delete_cmdb_extendable_option(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single CmdbExtendableOption

    Args:
        public_id (int): public_id of the CmdbExtendableOption which should be deleted
        request_user (CmdbUser): User requesting this data

    Returns:
        DeleteSingleResponse: The deleted CmdbExtendableOption data
    """
    try:
        extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(
                                                                    ManagerType.EXTENDABLE_OPTIONS,
                                                                    request_user
                                                                )

        to_delete_extendable_option = extendable_options_manager.get_extendable_option(public_id)

        if not to_delete_extendable_option:
            abort(404, f"The ExtendableOption with ID:{public_id} was not found!")

        # Predefined is undeletable
        if to_delete_extendable_option['predefined']:
            abort(404, "A predefined ExtendableOption cannot be deleted !")

        if is_extendable_option_used(to_delete_extendable_option, request_user):
            abort(400, f"Cannot delete the ExtendableOption with ID: {public_id} as it is in use by other resources!")

        extendable_options_manager.delete_extendable_option(public_id)

        return DeleteSingleResponse(to_delete_extendable_option).make_response()
    except HTTPException as http_err:
        raise http_err
    except ExtendableOptionsManagerDeleteError as err:
        LOGGER.error("[delete_cmdb_extendable_option] ExtendableOptionsManagerDeleteError: %s", err, exc_info=True)
        abort(400, f"Failed to delete the ExtendableOption with ID:{public_id}!")
    except ExtendableOptionsManagerGetError as err:
        LOGGER.error("[delete_cmdb_extendable_option] ExtendableOptionsManagerGetError: %s", err, exc_info=True)
        abort(400, f"Failed to retrieve the ExtendableOption with ID:{public_id} from the database!")
    except Exception as err:
        LOGGER.error("[delete_cmdb_extendable_option] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "Internal server error!")

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

def is_extendable_option_used(extendable_option: dict, request_user: CmdbUser) -> bool:
    """
    Checks if a CmdbExtendableOption is used in other collections before deletion

    Args:
        extendable_option (dict): The public_id of the CmdbExtendableOption to check.
        request_user (str): User requesting the check

    Returns:
        bool: True if the option is used, False otherwise.
    """
    threat_manager: ThreatManager = ManagerProvider.get_manager(ManagerType.THREAT, request_user)
    vulnerability_manager: VulnerabilityManager = ManagerProvider.get_manager(ManagerType.VULNERABILITY, request_user)
    object_groups_manager: ObjectGroupsManager = ManagerProvider.get_manager(ManagerType.OBJECT_GROUP, request_user)

    if extendable_option.get('option_type') == OptionType.THREAT:
        return threat_manager.count_items({"source": extendable_option.get('public_id')}) > 0

    if extendable_option.get('option_type') == OptionType.VULNERABILITY:
        return vulnerability_manager.count_items({"source": extendable_option.get('public_id')}) > 0

    if extendable_option.get('option_type') == OptionType.OBJECT_GROUP:
        return object_groups_manager.count_items({"categories": extendable_option.get('public_id')}) > 0

    # If option_type is not recognized
    return False

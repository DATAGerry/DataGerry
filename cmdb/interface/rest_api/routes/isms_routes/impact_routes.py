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
Implementation of all API routes for IsmsImpacts
"""
import logging
from flask import request, abort
from werkzeug.exceptions import HTTPException

from cmdb.manager import ImpactManager
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsImpact

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

from cmdb.errors.manager.impact_manager import (
    ImpactManagerInsertError,
    ImpactManagerGetError,
    ImpactManagerUpdateError,
    ImpactManagerDeleteError,
    ImpactManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

impact_blueprint = APIBlueprint('impacts', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@impact_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@impact_blueprint.protect(auth=True, right='base.isms.impact.add')
@impact_blueprint.validate(IsmsImpact.SCHEMA)
def insert_isms_impact(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert an IsmsImpact into the database

    Args:
        data (IsmsImpact.SCHEMA): Data of the IsmsImpact which should be inserted
        request_user (CmdbUser): User requesting this data

    Returns:
        InsertSingleResponse: The new IsmsImpact and its public_id
    """
    try:
        impact_manager: ImpactManager = ManagerProvider.get_manager(ManagerType.IMPACT, request_user)

        # There is a Limit of 10 Impact classes
        impact_count = impact_manager.count_impacts()

        if impact_count >= 10:
            return abort(403, "Only a maximum of 10 Impacts can be created!")

        try:
            data['calculation_basis'] = f"{float(data['calculation_basis']):.1f}"
        except Exception:
            return abort(400, "The calculation basis is either not provided or could not be converted to a float!")

        if impact_manager.impact_calculation_basis_exists(data['calculation_basis']):
            return abort(400, "The calculation basis is already used by another Impact!")

        result_id: int = impact_manager.insert_impact(data)

        created_impact: dict = impact_manager.get_impact(result_id)

        if created_impact:
            api_response = InsertSingleResponse(created_impact, result_id)

            return api_response.make_response()

        return abort(404, "Could not retrieve the created Impact from the database!")
    except HTTPException as http_err:
        raise http_err
    except ImpactManagerInsertError as err:
        LOGGER.error("[insert_isms_impact] ImpactManagerInsertError: %s", err, exc_info=True)
        return abort(400, "Could not insert the new Impact in the database!")
    except ImpactManagerGetError as err:
        LOGGER.error("[insert_isms_impact] ImpactManagerGetError: %s", err, exc_info=True)
        return abort(400, "Failed to retrieve the created Impact from the database!")
    except Exception as err:
        LOGGER.error("[insert_isms_impact] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@impact_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@impact_blueprint.protect(auth=True, right='base.isms.impact.view')
@impact_blueprint.parse_collection_parameters()
def get_isms_impacts(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple IsmsImpacts

    Args:
        params (CollectionParameters): Filter for requested IsmsImpacts
        request_user (CmdbUser): User requesting this data

    Returns:
        GetMultiResponse: All the IsmsImpacts matching the CollectionParameters
    """
    try:
        body = request.method == 'HEAD'

        impact_manager: ImpactManager = ManagerProvider.get_manager(ManagerType.IMPACT, request_user)

        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[IsmsImpact] = impact_manager.iterate(builder_params)
        impact_list = [IsmsImpact.to_json(impact) for impact in iteration_result.results]

        api_response = GetMultiResponse(impact_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)

        return api_response.make_response()
    except ImpactManagerIterationError as err:
        LOGGER.error("[get_isms_impacts] ImpactManagerIterationError: %s", err, exc_info=True)
        return abort(400, "Failed to retrieve Impacts from the database!")
    except Exception as err:
        LOGGER.error("[get_isms_impacts] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


@impact_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@impact_blueprint.protect(auth=True, right='base.isms.impact.view')
def get_isms_impact(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single IsmsImpact

    Args:
        public_id (int): public_id of the IsmsImpact
        request_user (CmdbUser): User requesting this data

    Returns:
        GetSingleResponse: The requested IsmsImpact
    """
    try:
        impact_manager: ImpactManager = ManagerProvider.get_manager(ManagerType.IMPACT, request_user)

        requested_impact = impact_manager.get_impact(public_id)

        if requested_impact:
            return GetSingleResponse(requested_impact, body = request.method == 'HEAD').make_response()

        return abort(404, f"The Impact with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except ImpactManagerGetError as err:
        LOGGER.error("[get_isms_impact] ImpactManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the Impact with ID: {public_id} from the database!")
    except Exception as err:
        LOGGER.error("[get_isms_impact] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@impact_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@impact_blueprint.protect(auth=True, right='base.isms.impact.edit')
@impact_blueprint.validate(IsmsImpact.SCHEMA)
def update_isms_impact(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single IsmsImpact

    Args:
        public_id (int): public_id of the IsmsImpact which should be updated
        data (IsmsImpact.SCHEMA): New IsmsImpact data
        request_user (CmdbUser): User requesting this data

    Returns:
        UpdateSingleResponse: The new data of the IsmsImpact
    """
    try:
        impact_manager: ImpactManager = ManagerProvider.get_manager(ManagerType.IMPACT, request_user)

        to_update_impact = impact_manager.get_impact(public_id)

        if not to_update_impact:
            return abort(404, f"The Impact with ID:{public_id} was not found!")

        impact = IsmsImpact.from_data(data)

        impact_manager.update_impact(public_id, impact)

        return UpdateSingleResponse(data).make_response()
    except HTTPException as http_err:
        raise http_err
    except ImpactManagerGetError as err:
        LOGGER.error("[update_isms_impact] ImpactManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the Impact with ID: {public_id} from the database!")
    except ImpactManagerUpdateError as err:
        LOGGER.error("[update_isms_impact] ImpactManagerUpdateError: %s", err, exc_info=True)
        return abort(400, f"Failed to update the Impact with ID: {public_id}!")
    except Exception as err:
        LOGGER.error("[update_isms_impact] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@impact_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@impact_blueprint.protect(auth=True, right='base.isms.impact.delete')
def delete_isms_impact(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single IsmsImpact

    Args:
        public_id (int): public_id of the IsmsImpact which should be deleted
        request_user (CmdbUser): User requesting this data

    Returns:
        DeleteSingleResponse: The deleted IsmsImpact data
    """
    try:
        impact_manager: ImpactManager = ManagerProvider.get_manager(ManagerType.IMPACT, request_user)

        to_delete_impact = impact_manager.get_impact(public_id)

        if not to_delete_impact:
            return abort(404, f"The Impact with ID:{public_id} was not found!")

        impact_manager.delete_impact(public_id)

        return DeleteSingleResponse(to_delete_impact).make_response()
    except HTTPException as http_err:
        raise http_err
    except ImpactManagerDeleteError as err:
        LOGGER.error("[delete_isms_impact] ImpactManagerDeleteError: %s", err, exc_info=True)
        return abort(400, f"Failed to delete the Impact with ID:{public_id}!")
    except ImpactManagerGetError as err:
        LOGGER.error("[delete_isms_impact] ImpactManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the Impact with ID:{public_id} from the database!")
    except Exception as err:
        LOGGER.error("[delete_isms_impact] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

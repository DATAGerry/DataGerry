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
"""document"""
#TODO: DOCUMENT-FIX
import logging
from datetime import datetime, timezone
from flask import abort, request

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager import (
    TypesManager,
    LocationsManager,
    ObjectsManager,
    ReportsManager,
)

from cmdb.models.user_model import CmdbUser
from cmdb.models.type_model import CmdbType
from cmdb.models.location_model.cmdb_location import CmdbLocation
from cmdb.models.object_model.cmdb_object import CmdbObject
from cmdb.framework.results import IterationResult
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.routes.framework_routes.type_parameters import TypeIterationParameters
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import (
    DeleteSingleResponse,
    UpdateSingleResponse,
    InsertSingleResponse,
    GetMultiResponse,
    GetSingleResponse,
    DefaultResponse,
)

from cmdb.errors.manager import (
    BaseManagerGetError,
    BaseManagerInsertError,
    BaseManagerUpdateError,
    BaseManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

types_blueprint = APIBlueprint('types', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@types_blueprint.route('/', methods=['POST'])
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.add')
@types_blueprint.validate(CmdbType.SCHEMA)
def insert_type(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route for insert a single type resource

    Args:
        data (CmdbType.SCHEMA): Insert data of a new type

    Returns:
        InsertSingleResponse: Insert response with the new type and its public_id
    """
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    data.setdefault('creation_time', datetime.now(timezone.utc))
    possible_id = data.get('public_id', None)

    if possible_id:
        try:
            types_manager.get_type(possible_id)
        except BaseManagerGetError:
            pass
        else:
            return abort(400, f'Type with PublicID {possible_id} already exists.')

    try:
        result_id = types_manager.insert_type(data)
        raw_doc = types_manager.get_type(result_id)
    except BaseManagerGetError:
        #TODO: ERROR-FIX
        return abort(404, "Can not retrieve the created Type from the database!")
    except BaseManagerInsertError as err:
        LOGGER.error("[insert_type] %s", err)
        return abort(400, "The Type could not be inserted!")

    api_response = InsertSingleResponse(result_id=result_id, raw=CmdbType.to_json(raw_doc))

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@types_blueprint.route('/', methods=['GET', 'HEAD'])
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.view')
@types_blueprint.parse_parameters(TypeIterationParameters)
def get_types(params: TypeIterationParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting a iterable collection of resources.

    Args:
        params (CollectionParameters): Passed parameters over the http query string

    Returns:
        GetMultiResponse: Which includes a IterationResult of the CmdbType.

    Example:
        You can pass any parameter based on the CollectionParameters.
        Optional parameters are passed over the function declaration.

    """
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    view = params.active

    if view:
        if isinstance(params.filter, dict):
            if params.filter.keys():
                params.filter.update({'active': view})
            else:
                params.filter = [{'$match': {'active': view}}, {'$match': params.filter}]
        elif isinstance(params.filter, list):
            params.filter.append({'$match': {'active': view}})

    builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

    try:
        iteration_result: IterationResult[CmdbType] = types_manager.iterate(builder_params)

        types = [CmdbType.to_json(type) for type in iteration_result.results]

        api_response = GetMultiResponse(types,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        body=request.method == 'HEAD')
    except BaseManagerIterationError:
        #TODO: ERROR-FIX
        return abort(400)
    except BaseManagerGetError:
        #TODO: ERROR-FIX
        return abort(404)

    return api_response.make_response()


@types_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@types_blueprint.protect(auth=True, right='base.framework.type.view')
def get_type(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for a single type resource.

    Args:
        public_id (int): Public ID of the type.

    Returns:
        GetSingleResponse: Which includes the json data of a CmdbType.
    """
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    try:
        type_ = types_manager.get_type(public_id)
    except BaseManagerGetError:
        return abort(404)
    api_response = GetSingleResponse(CmdbType.to_json(type_), body=request.method == 'HEAD')

    return api_response.make_response()


@types_blueprint.route('/count_objects/<int:public_id>', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.read')
def count_objects_of_type(public_id: int, request_user: CmdbUser):
    """
    Return the number of objects in der database with the given public_id as type_id
    Args:
        public_id (int): public_id of the type
    """
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    try:
        objects_count = objects_manager.count_objects({'type_id':public_id})
        api_response = DefaultResponse(objects_count)
    except BaseManagerGetError:
        #TODO: ERROR-FIX
        return abort(404)
    except Exception:
        #TODO: ERROR-FIX
        return abort(500)

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@types_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.edit')
@types_blueprint.validate(CmdbType.SCHEMA)
def update_type(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route for update a single type resource.

    Args:
        public_id (int): Public ID of the updatable type
        data (CmdbType.SCHEMA): New type data to update

    Returns:
        UpdateSingleResponse: With update result of the new updated type.
    """
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)
    locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS_MANAGER, request_user)
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    try:
        unchanged_type = types_manager.get_type(public_id)
        data['last_edit_time'] = datetime.now(timezone.utc)

        type_ = CmdbType.from_data(data)

        types_manager.update_type(public_id, CmdbType.to_json(type_))
        api_response = UpdateSingleResponse(result=data)
    except BaseManagerGetError as err:
        LOGGER.error("[update_type] %s", err)
        #TODO: ERROR-FIX
        return abort(404, "Could not retrieve the Type which should be updated!")
    except BaseManagerUpdateError as err:
        LOGGER.error("[update_type] %s", err)
        return abort(400, f"Type with public_id: {public_id} could not be updated!")
    except Exception as err:
        LOGGER.error("[update_type] Update Type Exception: %s", err)
        return abort(500, f"Type with public_id: {public_id} could not be updated!")

    # when types are updated, update all locations with relevant data from this type
    updated_type = types_manager.get_type(public_id)

    try:
        locations_with_type = locations_manager.get_locations_by(type_id=public_id)

        loc_data = {
            'type_label': updated_type.label,
            'type_icon': updated_type.render_meta.icon,
            'type_selectable': updated_type.selectable_as_parent
        }

        location: CmdbLocation
        for location in locations_with_type:
            locations_manager.update({'public_id':location.public_id}, loc_data)

        # check and update all multi data sections for the type if required
        updated_objects = types_manager.handle_mutli_data_sections(unchanged_type, data)
    except Exception as err:
        LOGGER.warning("[update_type] Handle locations Exception: %s", err)

    try:
        an_object: CmdbObject
        for an_object in updated_objects:
            objects_manager.update_object(an_object.public_id, CmdbObject.to_json(an_object))
    except Exception as err:
        LOGGER.warning("[update_type] Update objects Exception: %s", err)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@types_blueprint.route('/<int:public_id>', methods=['DELETE'])
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.delete')
def delete_type(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route for delete a single type resource.

    Args:
        public_id (int): Public ID of the deletable type

    Notes:
        Deleting the type will also delete all objects in this type!

    Returns:
        DeleteSingleResponse: Delete result with the deleted type as data.
    """
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)
    reports_manager: ReportsManager = ManagerProvider.get_manager(ManagerType.REPORTS_MANAGER, request_user)

    try:
        objects_count = objects_manager.count_objects({'type_id':public_id})

        # Only possible to delete types when there are no objects
        if objects_count > 0:
            return abort(403, "Delete not possible if objects of this type exist!")

        # Only possible to delete types when there are no reports using it
        reports_count = reports_manager.count_reports({'type_id':public_id})

        if reports_count > 0:
            return abort(403, "Delete not possible if reports exist which are using this type!")

        deleted_type = types_manager.delete_type(public_id)

        api_response = DeleteSingleResponse(raw=CmdbType.to_json(deleted_type))
    except BaseManagerGetError as err:
        #TODO: ERROR-FIX
        LOGGER.error("[delete_type] %s", err)
        return abort(404)
    except Exception as err:
        #TODO: ERROR-FIX
        LOGGER.error("[delete_type] Exception: %s", err)
        return abort(400)

    return api_response.make_response()

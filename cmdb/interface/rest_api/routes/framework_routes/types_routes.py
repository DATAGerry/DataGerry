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
Implementation of all API routes for CmdbTypes
"""
import logging
from datetime import datetime, timezone
from flask import abort, request
from werkzeug.exceptions import HTTPException

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager import (
    TypesManager,
    LocationsManager,
    ObjectsManager,
    ReportsManager,
    RelationsManager,
)

from cmdb.models.relation_model import CmdbRelation

from cmdb.models.user_model import CmdbUser
from cmdb.models.type_model import CmdbType
from cmdb.models.location_model.cmdb_location import CmdbLocation
from cmdb.models.object_model import CmdbObject
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
    BaseManagerUpdateError,
)
from cmdb.errors.manager.objects_manager import ObjectsManagerGetError
from cmdb.errors.manager.types_manager import (
    TypesManagerGetError,
    TypesManagerInsertError,
    TypesManagerDeleteError,
    TypesManagerIterationError,
    TypesManagerUpdateError,
    TypesManagerUpdateMDSError,
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
def insert_cmdb_type(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert a CmdbType into the database

    Args:
        data (CmdbType.SCHEMA): Data of the CmdbType which should be inserted
        request_user (CmdbUser): CmdbUser requesting this data

    Returns:
        InsertSingleResponse: The new CmdbType and its public_id
    """
    try:
        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)

        data.setdefault('creation_time', datetime.now(timezone.utc))
        possible_id = data.get('public_id', None)

        if possible_id:
            possible_type = types_manager.get_type(possible_id)

            if possible_type:
                return abort(400, f"Type with PublicID '{possible_id}' already exists!")

        result_id = types_manager.insert_type(data)
        created_type = types_manager.get_type(result_id)

        if created_type:
            api_response = InsertSingleResponse(result_id=result_id, raw=created_type)

            return api_response.make_response()
        return abort(404, "Could not retrieve the created Type from the database!")
    except HTTPException as http_err:
        raise http_err
    except TypesManagerGetError as err:
        LOGGER.error("[insert_cmdb_type] TypesManagerGetError: %s", err, exc_info=True)
        return abort(400, "Failed to retrieve the created Type from the database!")
    except TypesManagerInsertError as err:
        LOGGER.error("[insert_cmdb_type] %s", err)
        return abort(400, "Failed to insert the Type into the database!")


# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@types_blueprint.route('/', methods=['GET', 'HEAD'])
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.view')
@types_blueprint.parse_parameters(TypeIterationParameters)
def get_cmdb_types(params: TypeIterationParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple CmdbTypes

    Args:
        params (CollectionParameters): Filter for requested CmdbTypes
        request_user (CmdbUser): CmdbUser requesting this data

    Returns:
        GetMultiResponse: All the CmdbTypes matching the CollectionParameters
    """
    try:
        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)

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

        iteration_result: IterationResult[CmdbType] = types_manager.iterate(builder_params)

        types = [CmdbType.to_json(type) for type in iteration_result.results]

        api_response = GetMultiResponse(types,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        body=request.method == 'HEAD')

        return api_response.make_response()
    except TypesManagerIterationError as err:
        LOGGER.error("[get_cmdb_types] TypesManagerIterationError: %s", err, exc_info=True)
        return abort(400, "Failed to retrieve CmdbTypes from the database!")
    except Exception as err:
        LOGGER.error("[get_cmdb_types] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

@types_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@types_blueprint.protect(auth=True, right='base.framework.type.view')
def get_cmdb_type(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single CmdbType

    Args:
        public_id (int): public_id of the CmdbType
        request_user (CmdbUser): CmdbUser requesting this data

    Returns:
        GetSingleResponse: The requested CmdbType
    """
    try:
        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)

        requested_type = types_manager.get_type(public_id)

        if requested_type:
            api_response = GetSingleResponse(requested_type, body=request.method == 'HEAD')

            return api_response.make_response()
        return abort(404, f"The Type with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except TypesManagerGetError as err:
        LOGGER.error("[get_cmdb_type] TypesManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the Type with ID: {public_id} from the database!")
    except Exception as err:
        LOGGER.error("[get_cmdb_type] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


@types_blueprint.route('/count_objects/<int:public_id>', methods=['GET'])
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.view')
def count_objects_of_cmdb_type(public_id: int, request_user: CmdbUser):
    """
    Counts the number of CmdbObjects in the database with the given public_id as the type_id

    Args:
        public_id (int): The public_id of the CmdbType to count CmdbObjects for
        request_user (CmdbUser): CmdbUser requesting this data

    Returns:
        DefaultResponse: An API response containing the count of CmdbObjects for the given type_id
    """
    try:
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)

        objects_count = objects_manager.count_objects({'type_id':public_id})

        api_response = DefaultResponse(objects_count)

        return api_response.make_response()
    except ObjectsManagerGetError as err:
        LOGGER.error("[count_objects_of_cmdb_type] ObjectsManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to count Objects for Type with ID: {public_id}!")
    except Exception as err:
        LOGGER.error("[count_objects_of_cmdb_type] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")



# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@types_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.edit')
@types_blueprint.validate(CmdbType.SCHEMA)
def update_cmdb_type(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single CmdbType

    Args:
        public_id (int): public_id of the CmdbType which should be updated
        data (CmdbType.SCHEMA): New CmdbType data
        request_user (CmdbUser): CmdbUser requesting this data

    Returns:
        UpdateSingleResponse: The new data of the CmdbType
    """
    try:
        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)
        locations_manager: LocationsManager = ManagerProvider.get_manager(ManagerType.LOCATIONS, request_user)
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)

        unchanged_type = types_manager.get_type(public_id)

        if unchanged_type:
            data['last_edit_time'] = datetime.now(timezone.utc)

            new_type_data = CmdbType.from_data(data)

            types_manager.update_type(public_id, CmdbType.to_json(new_type_data))

            updated_type = types_manager.get_type(public_id)
            updated_type = CmdbType.from_data(updated_type)

            # when type are updated, update all locations with relevant data from this type
            locations_with_type = locations_manager.get_locations_by(type_id=public_id)

            loc_data = {
                'type_label': updated_type.label,
                'type_icon': updated_type.render_meta.icon,
                'type_selectable': updated_type.selectable_as_parent
            }

            location: CmdbLocation
            for location in locations_with_type:
                locations_manager.update_location(location.public_id, loc_data, False)

            # check and update all multi data sections for the type if required
            updated_objects = types_manager.handle_mutli_data_sections(CmdbType.from_data(unchanged_type),
                                                                       data)

            # Update Objects
            an_object: CmdbObject
            for an_object in updated_objects:
                objects_manager.update_object(an_object.public_id, CmdbObject.to_json(an_object))

            api_response = UpdateSingleResponse(result=data)

            return api_response.make_response()

        return abort(404, f"The Type with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except BaseManagerGetError as err:
        #TODO: ERROR-FIX (need to catch specific CmdbLocation exception)
        LOGGER.error("[update_cmdb_type] BaseManagerGetError: %s", err, exc_info=True)
        return abort(400, "Although the Type got updated, the update of Locations failed!")
    except BaseManagerUpdateError as err:
        #TODO: ERROR-FIX (need to catch specific CmdbObject exception)
        LOGGER.error("[update_cmdb_type] BaseManagerUpdateError: %s", err, exc_info=True)
        return abort(400, "Although the Type got updated, the update of Objects failed!")
    except TypesManagerGetError as err:
        LOGGER.error("[update_cmdb_type] TypesManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the Type with ID: {public_id} from the database!")
    except TypesManagerUpdateError as err:
        LOGGER.error("[update_cmdb_type] TypesManagerUpdateError: %s", err, exc_info=True)
        return abort(400, f"Failed to update the Type with ID: {public_id} from the database!")
    except TypesManagerUpdateMDSError as err:
        LOGGER.error("[update_cmdb_type] TypesManagerUpdateMDSError: %s", err, exc_info=True)
        return abort(400, "Although the Type got updated, the Multi-Data-Section updates failed!")
    except Exception as err:
        LOGGER.error("[update_cmdb_type] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@types_blueprint.route('/<int:public_id>', methods=['DELETE'])
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@insert_request_user
@types_blueprint.protect(auth=True, right='base.framework.type.delete')
def delete_cmdb_type(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single CmdbType

    Args:
        public_id (int): public_id of the CmdbType which should be deleted
        request_user (CmdbUser): CmdbUser requesting this data

    Returns:
        DeleteSingleResponse: The deleted CmdbType data
    """
    try:
        types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES, request_user)
        objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS, request_user)
        reports_manager: ReportsManager = ManagerProvider.get_manager(ManagerType.REPORTS, request_user)
        relations_manager: RelationsManager = ManagerProvider.get_manager(ManagerType.RELATIONS, request_user)

        to_delete_type = types_manager.get_type(public_id)

        if to_delete_type:
            objects_count = objects_manager.count_objects({'type_id':public_id})

            # Only possible to delete types when there are no objects
            if objects_count > 0:
                return abort(403, "Delete not possible if Objects of this Type exist!")

            # Only possible to delete types when there are no reports using it
            reports_count = reports_manager.count_reports({'type_id':public_id})

            if reports_count > 0:
                return abort(403, "Delete not possible if Reports exist which are using this Type!")

            types_manager.delete_type(public_id)

            # TODO: REFACTOR-FIX (move in seperate function)
            try:
                # Delete this type_id from all relations parent and child ids
                relevant_relations_filter = {'$or':[
                                {'parent_type_ids': {'$in': [public_id]}},
                                {'child_type_ids': {'$in': [public_id]}}
                            ]}


                builder_params = BuilderParameters(criteria=relevant_relations_filter)

                iteration_result: IterationResult[CmdbRelation] = relations_manager.iterate(builder_params)

                relation_list: list[CmdbRelation] = list(iteration_result.results)

                for relation in relation_list:
                    relation.remove_type_id_from_relation(public_id)

                    relations_manager.update_relation(relation.public_id, CmdbRelation.to_json(relation))
            except Exception as error:
                LOGGER.error("[delete_cmdb_type] Relation Exception: %s. Type: %s", error, type(error), exc_info=True)
                return abort(400, "Although the Type got deleted, Relations could not be updated!")

            api_response = DeleteSingleResponse(to_delete_type)

            return api_response.make_response()

        return abort(404, f"The Type with ID:{public_id} was not found!")
    except HTTPException as http_err:
        raise http_err
    except TypesManagerGetError as err:
        LOGGER.error("[delete_cmdb_type] TypesManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to retrieve the Type with ID: {public_id}!")
    except ObjectsManagerGetError as err:
        LOGGER.error("[delete_cmdb_type] ObjectsManagerGetError: %s", err, exc_info=True)
        return abort(400, f"Failed to count Objects for Type with ID: {public_id}!")
    except BaseManagerGetError as err:
        #TODO: ERROR-FIX (raise specific reports error)
        LOGGER.error("[delete_cmdb_type] BaseManagerGetError: %s", err, exc_info=True)
        return abort(400, "Failed to count Reports with this Type!")
    except TypesManagerDeleteError as err:
        LOGGER.error("[delete_cmdb_type] TypesManagerDeleteError: %s", err, exc_info=True)
        return abort(400, f"Failed to delete the Type with ID: {public_id}!")
    except Exception as err:
        LOGGER.error("[delete_cmdb_type] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

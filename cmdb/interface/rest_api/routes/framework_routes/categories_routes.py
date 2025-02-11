# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
Implementation of all API routes for CmdbCategories
"""
import logging
from datetime import datetime, timezone
from flask import request, abort

from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType
from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager import CategoriesManager

from cmdb.models.user_model import CmdbUser
from cmdb.models.category_model import CmdbCategory, CategoryTree
from cmdb.framework.results import IterationResult
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import (
    DeleteSingleResponse,
    UpdateSingleResponse,
    InsertSingleResponse,
    GetMultiResponse,
    GetSingleResponse,
)

from cmdb.errors.manager.categories_manager import (
    CategoriesManagerInsertError,
    CategoriesManagerGetError,
    CategoriesManagerUpdateError,
    CategoriesManagerDeleteError,
    CategoriesManagerIterationError,
    CategoriesManagerTreeInitError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

categories_blueprint = APIBlueprint('categories', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@categories_blueprint.route('/', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@categories_blueprint.protect(auth=True, right='base.framework.category.add')
@categories_blueprint.validate(CmdbCategory.SCHEMA)
def insert_category(data: dict, request_user: CmdbUser):
    """
    HTTP `POST` route to insert a CmdbCategory into the database

    Args:
        `data` (CmdbCategory.SCHEMA): Data of the CmdbCategory which should be inserted
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `InsertSingleResponse`: The new CmdbCategory and its public_id
    """
    try:
        categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER,
                                                                            request_user)

        data.setdefault('creation_time', datetime.now(timezone.utc))

        result_id: int = categories_manager.insert_category(data)

        created_category = categories_manager.get_category(result_id)

        api_response = InsertSingleResponse(created_category, result_id)

        return api_response.make_response()
    except CategoriesManagerInsertError as err:
        LOGGER.error("[insert_category] %s", err, exc_info=True)
        return abort(400, "Could not insert the new category in the database!")
    except CategoriesManagerGetError as err:
        LOGGER.error("[insert_category] %s", err, exc_info=True)
        return abort(404, "Could not retrieve the created category from the database!")
    except Exception as err:
        LOGGER.error("[insert_category] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@categories_blueprint.route('/', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@categories_blueprint.protect(auth=True, right='base.framework.category.view')
@categories_blueprint.parse_collection_parameters(view='list')
def get_categories(params: CollectionParameters, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route for getting multiple CmdbCategories

    Args:
        `params` (CollectionParameters): Filter for requested CmdbCategories
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `GetMultiResponse`: All the CmdbCategories matching the CollectionParameters
    """
    try:
        categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER,
                                                                            request_user)

        body = request.method == 'HEAD'

        if params.optional['view'] == 'tree':
            tree: CategoryTree = categories_manager.tree
            api_response = GetMultiResponse(CategoryTree.to_json(tree),
                                            len(tree),
                                            params,
                                            request.url,
                                            body)

            return api_response.make_response(pagination=False)

        # if view is not 'tree'
        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[CmdbCategory] = categories_manager.iterate(builder_params)

        category_list = [CmdbCategory.to_json(category) for category in iteration_result.results]

        api_response = GetMultiResponse(category_list,
                                        iteration_result.total,
                                        params,
                                        request.url,
                                        body)

        return api_response.make_response()
    except CategoriesManagerIterationError as err:
        LOGGER.error("[get_categories] %s", err, exc_info=True)
        return abort(400, "Could not retrieve categories from database!")
    except CategoriesManagerTreeInitError as err:
        LOGGER.error("[get_categories] %s", err, exc_info=True)
        return abort(500, "Could not place the categories into a tree structure!")
    except Exception as err:
        LOGGER.error("[get_categories] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


@categories_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@categories_blueprint.protect(auth=True, right='base.framework.category.view')
def get_category(public_id: int, request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve a single CmdbCategory

    Args:
        `public_id` (int): public_id of the CmdbCategory
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `GetSingleResponse`: The requested CmdbCategory
    """
    try:
        categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER,
                                                                            request_user)

        requested_category = categories_manager.get_category(public_id)

        api_response = GetSingleResponse(requested_category, body = request.method == 'HEAD')

        return api_response.make_response()
    except CategoriesManagerGetError as err:
        LOGGER.error("[get_category] %s", err, exc_info=True)
        return abort(404, "Could not retrieve the requested category from the database!")
    except Exception as err:
        LOGGER.error("[get_category] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")


# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@categories_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@categories_blueprint.protect(auth=True, right='base.framework.category.edit')
@categories_blueprint.validate(CmdbCategory.SCHEMA)
def update_category(public_id: int, data: dict, request_user: CmdbUser):
    """
    HTTP `PUT`/`PATCH` route to update a single CmdbCategory

    Args:
        `public_id` (int): public_id of the CmdbCategory which should be updated
        `data` (CmdbCategory.SCHEMA): New CmdbCategory data
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `UpdateSingleResponse`: The new data of the CmdbCategory
    """
    try:
        categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER,
                                                                            request_user)

        category = CmdbCategory.from_data(data)

        categories_manager.update_category(public_id, category)

        api_response = UpdateSingleResponse(result=data)
    except CategoriesManagerUpdateError as err:
        LOGGER.error("[update_category] %s", err, exc_info=True)
        return abort(400, "Could not update the category!")
    except Exception as err:
        LOGGER.error("[update_category] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@categories_blueprint.route('/<int:public_id>', methods=['DELETE'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.ADMIN)
@categories_blueprint.protect(auth=True, right='base.framework.category.delete')
def delete_category(public_id: int, request_user: CmdbUser):
    """
    HTTP `DELETE` route to delete a single CmdbCategory

    Args:
        `public_id` (int): public_id of the CmdbCategory which should be deleted
        `request_user` (CmdbUser): User requesting this data

    Returns:
        `DeleteSingleResponse`: The deleted CmdbCategory data
    """
    try:
        categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER,
                                                                            request_user)

        category_instance = categories_manager.get_category(public_id)
        categories_manager.delete_category(public_id)

        # Update 'parent' attribute on direct children
        categories_manager.reset_children_categories(public_id)

        api_response = DeleteSingleResponse(raw=category_instance)
        return api_response.make_response()
    except CategoriesManagerDeleteError as err:
        LOGGER.error("[delete_category] %s", err, exc_info=True)
        return abort(400, f"Could not delete the category with the ID:{public_id}")
    except CategoriesManagerGetError as err:
        LOGGER.error("[delete_category] %s", err, exc_info=True)
        return abort(404, "Could not retrieve a category from the database!")
    except CategoriesManagerUpdateError as err:
        LOGGER.error("[update_category] %s", err, exc_info=True)
        return abort(500, "Could not update a child category although the requested category got deleted!")
    except Exception as err:
        LOGGER.error("[delete_category] Exception: %s. Type: %s", err, type(err), exc_info=True)
        return abort(500, "Internal server error!")

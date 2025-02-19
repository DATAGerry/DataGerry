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
Implementation of the BaseManager for all Managers requiring a database connection
"""
import logging
from pymongo.results import DeleteResult

from cmdb.database import MongoDatabaseManager
from cmdb.manager.query_builder import BaseQueryBuilder, BuilderParameters

from cmdb.models.user_model import CmdbUser
from cmdb.security.acl.permission import AccessControlPermission

from cmdb.errors.database import DocumentGetError
from cmdb.errors.manager import (
    ManagerInsertError,
    ManagerGetError,
    ManagerUpdateError,
    ManagerDeleteError,
    ManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  BaseManager - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class BaseManager:
    """This is the base class for every FrameworkManager"""

    def __init__(self, collection: str, dbm: MongoDatabaseManager):
        self.collection = collection
        self.query_builder = BaseQueryBuilder()
        self.dbm: MongoDatabaseManager = dbm


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Auto disconnect the database connection when the Manager get destroyed
        """
        self.dbm.connector.disconnect()

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert(self, data: dict, skip_public: bool = False) -> int:
        """
        Insert document into database

        Args:
            data (dict): Data which should be inserted
            skip_public (bool): Skip the public id creation and counter increment

        Raises:
            ManagerInsertError: When the insertion failed

        Returns:
            int: New public_id of inserted document
            None: If anything goes wrong
        """
        try:
            return self.dbm.insert(self.collection, data, skip_public)
        except Exception as err:
            raise ManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def iterate_query(self,
                      builder_params: BuilderParameters,
                      user: CmdbUser = None,
                      permission: AccessControlPermission = None) -> tuple[list, int]:
        """
        Performs an aggregation on the database

        Args:
            `builder_params` (BuilderParameters): Contains input to identify the target of action
            `user` (CmdbUser, optional): User requesting this action
            `permission` (AccessControlPermission, optional): Permission which should be checked for the user

        Raises:
            `ManagerIterationError`: Raised when something goes wrong during the aggregation

        Returns:
            `tuple[list, int]`: Result which matches the builder_params and the number of results
        """
        try:
            query: list[dict] = self.query_builder.build(builder_params, user, permission)
            count_query: list[dict] = self.query_builder.count(builder_params.get_criteria())

            aggregation_result = list(self.aggregate(query))
            total_cursor = self.aggregate(count_query)

            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']

            return aggregation_result , total
        except Exception as err:
            raise ManagerIterationError(err) from err


    def get_one(self, *args, **kwargs):
        """
        Calls MongoDB find operation for a single document

        Raises:
            `ManagerGetError`: When the 'find_one' operation fails

        Returns:
            Cursor over the result set
        """
        try:
            return self.dbm.find_one(self.collection, *args, **kwargs)
        except Exception as err:
            raise ManagerGetError(err) from err


    def get_one_from_other_collection(self, collection: str, public_id: int):
        """
        Calls MongoDB find operation for a single document from another collection

        Raises:
            ManagerGetError: When the find_one operation fails
        
        Returns:
            Cursor over the result set
        """
        try:
            return self.dbm.find_one(collection, public_id)
        except DocumentGetError as err:
            raise ManagerGetError(err) from err


    def get_many_from_other_collection(self,
                                       collection: str,
                                       sort: str = 'public_id',
                                       direction: int = -1,
                                       limit: int = 0,
                                       **requirements: dict) -> list[dict]:
        """
        Get all documents from the database which have the passing requirements

        Args:
            collection (str): The target collection
            sort (str): sort by given key - default public_id
            direction (int): 1 = ascending, -1 = descending
            limit (int): limit the amount of 
            **requirements (dict): dictionary of key value pairs

        Raises:
            ManagerGetError: When documents could not be retrieved

        Returns:
            list: list of all retrieved documents
        """
        try:
            requirements_filter = {}
            formatted_sort = [(sort, direction)]

            for k, req in requirements.items():
                requirements_filter.update({k: req})

            return self.dbm.find_all(collection=collection,
                                    limit=limit,
                                    filter=requirements_filter,
                                    sort=formatted_sort)
        except Exception as err:
            LOGGER.debug("[get_many_from_other_collection] Exception: %s. Type: %s", err, type(err))
            raise ManagerGetError(str(err)) from err


    def get(self, *args, **kwargs):
        """
        General find function

        Raises:
            ManagerGetError: When something goes wrong while retrieving the documents

        Returns:
            Cursor: Result of the 'find'-Operation as Cursor
        """
        try:
            return self.dbm.find(self.collection, *args, **kwargs)
        except Exception as err:
            LOGGER.debug("[get] Error: %s , Type: %s", err, type(err))
            raise ManagerGetError(err) from err


    def find_all(self, *args, **kwargs):
        """calls find with all returns

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            list: list of found documents
        """
        found_documents = self.find(collection=self.collection, *args, **kwargs)

        return list(found_documents)


    def find(self, *args, criteria=None, **kwargs):
        """document"""
        #TODO: DOCUMENT-FIX
        try:
            return self.dbm.find(self.collection, filter=criteria, *args, **kwargs)
        except Exception as err:
            raise ManagerGetError(err) from err


    def get_one_by(self, criteria: dict) -> dict:
        """
        Retrieves a single document defined by the given critera

        Raises:
            ManagerGetError: When the 'find_one_by' operation fails
        Args:
            criteria (dict): Filter for the document
        """
        try:
            return self.dbm.find_one_by(self.collection, criteria)
        except DocumentGetError as err:
            raise ManagerGetError(err) from err


    def get_many(self,
                 sort: str = 'public_id',
                 direction: int = -1,
                 limit: int=0,
                 **requirements: dict) -> list[dict]:
        """
        Get all documents from the database filtered by the requirements

        Args:
            `sort` (str): sort by given key  (Default 'public_id')
            `direction` (int): Ascending = 1, Descending = -1 - (Default: -1)
            `limit` (int): Limits the amount of results, 0 equals no limit (Default: 0)
            `**requirements` (dict): dictionary of key value pairs as filter

        Raises:
            `ManagerGetError` : When retrieving the documents fails

        Returns:
            `list[dict]`: list of all documents
        """
        try:
            requirements_filter = {}
            formatted_sort = [(sort, direction)]

            for k, req in requirements.items():
                requirements_filter.update({k: req})

            return self.dbm.find_all(collection=self.collection,
                                    limit=limit,
                                    filter=requirements_filter,
                                    sort=formatted_sort)
        except Exception as err:
            raise ManagerGetError(err) from err


    def aggregate(self, *args, **kwargs):
        """
        Calls MongoDB aggregation with *args
        Args:
        Returns:
            - A :class:`~pymongo.command_cursor.CommandCursor` over the result set
        """
        try:
            return self.dbm.aggregate(self.collection, *args, **kwargs)
        except Exception as err:
            raise ManagerIterationError(err) from err


    def aggregate_from_other_collection(self, collection: str, *args, **kwargs):
        """
        Calls MongoDB aggregation with *args
        Args:
        Returns:
            - A :class:`~pymongo.command_cursor.CommandCursor` over the result set
        """
        try:
            return self.dbm.aggregate(collection, *args, **kwargs)
        except Exception as err:
            raise ManagerIterationError(err) from err


    def get_next_public_id(self):
        """
        Retrieves next public_id for the collection

        Returns:
            `int`: New highest public_id of the collection
        """
        # TODO: ERROR-FIX (create and catch error for this operation)
        return self.dbm.get_next_public_id(self.collection)


    def count_documents(self, collection: str, *args, **kwargs):
        """
        Counts the number of documents in a collection

        Args:
            collection: Name of the collection

        Raises:
            ManagerGetError: If an error occures during the 'count' operation

        Returns:
            int: Number of found documents with given filter 
        """
        try:
            return self.dbm.count(collection, *args, **kwargs)
        except Exception as err:
            LOGGER.debug("[count_documents] Exception: %s , Type: %s", err, type(err))
            raise ManagerGetError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    #TODO: ERROR-FIX (keyword before argument)
    def update(self, criteria: dict, data: dict, add_to_set: bool = True, *args, **kwargs):
        """
        Updates a document in the database

        Args:
            `criteria` (dict): Filter for which documents should match
            `data`: New values for the document

        Raises:
            `ManagerUpdateError`: When the update operation failed

        Returns:
            `UpdateResult`: The pymongo UpdateResult
        """
        #TODO: DOCUMENTATION-FIX (finish the function description)
        try:
            return self.dbm.update(self.collection, criteria, data, add_to_set, *args, **kwargs)
        except Exception as err:
            raise ManagerUpdateError(err) from err


    def update_many(self, criteria: dict, update: dict, add_to_set: bool = False):
        """
        Update all documents that match the filter from a collection

        Args:
            criteria (dict): Filter that matches the documents to update
            update (dict): The modifications to apply
        Returns:
            Acknowledgment of database
        """
        try:
            return self.dbm.update_many(self.collection, criteria, update, add_to_set)
        except Exception as err:
            raise ManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete(self, criteria: dict) -> bool:
        """
        Calls MongoDB delete operation

        Args:
            criteria (dict): Filter to match document

        Raises:
            ManagerDeleteError: Something went wrong while trying to delete document

        Returns:
            bool: True if deletion is successful
        """
        try:
            return self.dbm.delete(self.collection, criteria).acknowledged
        except Exception as err:
            raise ManagerDeleteError(err) from err


    def delete_many(self, filter_query: dict) -> DeleteResult:
        """
        Removes all documents that match the filter from a collection

        Args:
            filter (dict): Specifies deletion criteria using query operators

        Raises:
            ManagerDeleteError: If something goes wrong

        Returns:
            Acknowledgment of database
        """
        try:
            delete_result = self.dbm.delete_many(collection=self.collection, **filter_query)
        except Exception as err:
            raise ManagerDeleteError(str(err)) from err

        return delete_result

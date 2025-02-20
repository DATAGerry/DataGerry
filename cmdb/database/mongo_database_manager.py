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
This module provides the MongoDatabaseManager
"""
import logging
from typing import Union, Any
from collections.abc import MutableMapping
from pymongo.database import Database
from pymongo.errors import CollectionInvalid
from pymongo import IndexModel
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, UpdateResult

from cmdb.database import MongoConnector

from cmdb.models.location_model import get_root_location_data
from cmdb.framework.section_templates.section_template_creator import SectionTemplateCreator

from cmdb.errors.database import (
    CollectionAlreadyExistsError,
    CreateIndexesError,
    GetIndexesError,
    DatabaseConnectionError,
    DatabaseAlreadyExistsError,
    DatabaseNotFoundError,
    DeleteCollectionError,
    DocumentDeleteError,
    DocumentInsertError,
    DocumentUpdateError,
    DocumentGetError,
    DocumentAggregationError,
    GetCollectionError,
    PublicIdCounterInitError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

PUBLIC_ID_COUNTER_COLLECTION = "datastorage.counter"

# -------------------------------------------------------------------------------------------------------------------- #
#                                             MongoDatabaseManager - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class MongoDatabaseManager:
    """
    PyMongo (MongoDB) implementation of the Database Manager
    """
    def __init__(self, host: str, port: int, database_name: str, **kwargs):
        self.connector = MongoConnector(host, port, database_name, kwargs)


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures the database connection is closed when exiting a context
        """
        self.connector.disconnect()

# ---------------------------------------------- BASE DATABSE OPERATIONS --------------------------------------------- #

    def check_database_exists(self, name: str) -> bool:
        """
        Checks if a database with the given name exists

        Args:
            name (str): Name of the database which should be checked

        Raises:
            DatabaseConnectionError: If connection to database could not be established

        Returns:
            bool: True if database with given name exists, else False
        """
        try:
            database_names = self.connector.client.list_database_names()

            return name in database_names
        except Exception as err:
            raise DatabaseConnectionError(f"Failed to check if database '{name}' exists: {err}") from err


    def create_database(self, name: str) -> Database:
        """
        Create a new empty database if it does not already exist

        Args:
            name (str): Name of the new database

        Raises:
            DatabaseAlreadyExistsError: If a database with this name already exists
            DatabaseConnectionError: If the database connection fails

        Returns:
            Database: Instance of the newly created database
        """
        try:
            if name in self.connector.client.list_database_names():
                raise DatabaseAlreadyExistsError(f"Database '{name}' already exists.")

            return self.connector.client[name]
        except DatabaseAlreadyExistsError as err:
            raise err
        except Exception as err:
            raise DatabaseConnectionError(f"Failed to create database '{name}': {err}") from err


    def drop_database(self, database: Union[str, Database]) -> None:
        """
        Deletes an existing database

        Args:
            database (str, Database): Name or instance of the database to be dropped

        Raises:
            DatabaseNotFoundError: If the specified database does not exist
            DatabaseConnectionError: If the database connection fails during the operation
        """
        try:
            if isinstance(database, Database):
                database = database.name

            if database not in self.connector.client.list_database_names():
                raise DatabaseNotFoundError(f"Database '{database}' not found.")

            self.connector.client.drop_database(database)
        except DatabaseNotFoundError as err:
            raise err
        except Exception as err:
            raise DatabaseConnectionError(f"Failed to drop database '{database}': {err}") from err


    def create_collection(self, collection_name: str) -> str:
        """
        Creation an empty MongoDB collection

        Args:
            collection_name (str): Name of collection which should be created

        Raises:
            CollectionAlreadyExistsError: If the collection already exists
            DatabaseConnectionError: If there is an issue with the database connection

        Returns:
            str: The name of the created collection
        """
        try:
            all_collections = self.connector.database.list_collection_names()

            if collection_name not in all_collections:
                self.connector.database.create_collection(collection_name)

            return collection_name
        except Exception as err:
            if isinstance(err, CollectionInvalid):
                raise CollectionAlreadyExistsError(err) from err

            raise DatabaseConnectionError(f"Failed to create collection '{collection_name}': {err}") from err


    def get_collection(self, name: str) -> Collection:
        """
        Get a collection from the database

        Args:
            name (str): Collection name

        Raises:
            GetCollectionError: When the collection could not be retrieved

        Returns:
            (Collection): The requested collection
        """
        try:
            requested_collection = self.connector.database[name]

            return requested_collection
        except Exception as err:
            LOGGER.error("[get_collection] '%s' Exception: %s. Type: %s", name, err, type(err))
            raise GetCollectionError(err) from err


    def delete_collection(self, collection: str) -> dict[str, Any]:
        """
        Delete an existing collection

        Args:
            collection (str): collection name

        Raises:
            DeleteCollectionError: When collection can't be deleted

        Returns:
            delete ack
        """
        try:
            return self.connector.database.drop_collection(collection)
        except Exception as err:
            raise DeleteCollectionError(f"Failed to delete collection '{collection}': {err}") from err


    def create_indexes(self, collection: str, indexes: list[IndexModel]) -> list[str]:
        """
        Creates indexes for collection

        Args:
            collection (str): name of collection
            indexes (list[IndexModel]): list of IndexModels which should be created

        Raises:
            CreateIndexesError: When indexes can't be created

        Returns:
            list[str]: List of created indexes
        """
        try:
            return self.get_collection(collection).create_indexes(indexes)
        except Exception as err:
            raise CreateIndexesError(f"Failed to create indexes for collection '{collection}': {err}") from err


    def get_index_info(self, collection: str) -> MutableMapping[str, Any]:
        """
        Retrives index information for a collection

        Args:
            collection (str): name of collection

        Raises:
            GetIndexesError: When the index information could not be retrieved

        Returns:
            MutableMapping[str, Any]: Index information of the collection
        """
        try:
            return self.get_collection(collection).index_information()
        except Exception as err:
            raise GetIndexesError(
                f"Failed to retrieve index information for collection '{collection}': {err}"
            ) from err


    def status(self) -> bool:
        """
        Check if connector has connection to MongoDB

        Returns
            bool: True is connected, else False
        """
        return self.connector.is_connected()

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert(self, collection: str, data: dict, skip_public: bool = False) -> int:
        """
        Adds a document to a collection

        Args:
            collection (str): name of database collection
            data (dict): data which should be inserted
            skip_public (bool): Skip the public id creation and counter increment

        Raises:
            DocumentInsertError: When a document could not be created
        
        Returns:
            int: New public id of the document
        """
        try:
            if skip_public:
                return self.get_collection(collection).insert_one(data)

            if 'public_id' not in data:
                data['public_id'] = self.get_next_public_id(collection)

            self.get_collection(collection).insert_one(data)
            self.update_public_id_counter(collection, data['public_id'], increment=True)

            return data['public_id']
        except Exception as err:
            raise DocumentInsertError(f"Failed to insert document into collection '{collection}': {err}") from err


    def __init_public_id_counter(self, collection: str) -> int:
        """
        Initializes a public ID counter for the given collection

        Args:
            collection (str): Name of the collection for which the counter is initialised

        Raises:
            PublicIdCounterInitError: When the public_id counter could not be initialised

        Returns:
            int: The highest existing ID in the collection, which is set as the counter's initial value
        """
        try:
            highest_id = self.get_highest_id(collection)

            self.get_collection(PUBLIC_ID_COUNTER_COLLECTION).insert_one(
                {'_id': collection, 'counter': highest_id}
            )

            return highest_id
        except Exception as err:
            raise PublicIdCounterInitError(
                f"Failed to initialize public ID counter for collection '{collection}': {err}"
            ) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update(
            self,
            collection: str,
            criteria: dict,
            data: dict,
            *args,
            add_to_set: bool = True,
            **kwargs) -> UpdateResult:
        """
        Updates a document inside the specified collection

        Args:
            collection (str): The name of the database collection.
            criteria (dict): The filter used to match the document to be updated
            data (dict): The update data to apply
            add_to_set (bool, optional): If True, wraps `data` in '$set' unless it already contains update operators. 
                                         Defaults to True.
            *args: Additional positional arguments for the update operation
            **kwargs: Additional keyword arguments for the update operation

        Raises:
            DocumentUpdateError: When document could not be updated

        Returns:
            UpdateResult: The result of the update operation
        """
        try:
            # Apply '$set' only if no update operators are present
            update_data = {'$set': data} if add_to_set and not any(k.startswith('$') for k in data) else data

            result = self.get_collection(collection).update_one(criteria, update_data, *args, **kwargs)

            return result
        except Exception as err:
            LOGGER.error("[update] Exception: %s. Type: %s", err, type(err))
            raise DocumentUpdateError(f"Failed to update document in '{collection}': {err}") from err


    def unset_update_many(self, collection: str, criteria: dict, field: str, *args, **kwargs) -> UpdateResult:
        """
        Removes a field from multiple documents in the specified collection

        Args:
            collection (str): The name of the database collection
            criteria (dict): The filter used to match documents for updating
            field (str): The field to remove from the matched documents
            *args: Additional positional arguments for the update operation
            **kwargs: Additional keyword arguments for the update operation

        Raises:
            DocumentUpdateError: If the update operation fails

        Returns:
            UpdateResult: The result of the update operation
        """
        try:
            update_data = {'$unset': {field: 1}}

            result = self.get_collection(collection).update_many(criteria, update_data, *args, **kwargs)

            if result.modified_count == 0:
                LOGGER.warning(
                    "[unset_update_many] No documents matched criteria: %s in collection: %s", criteria, collection
                )

            return result
        except Exception as err:
            raise DocumentUpdateError(f"Failed to unset field '{field}' in '{collection}': {err}") from err


    def update_many(self, collection: str, criteria: dict, update: dict, add_to_set:bool = False) -> UpdateResult:
        """
        Updates multiple documents that match the filter in a collection

        Args:
            collection (str): Name of database collection
            criteria (dict): The filter used to match the documents for updating
            update (dict): The modifications to apply
            add_to_set(bool): If True, uses '$addToSet' to add values to an array without duplicates.
                              If False, uses '$set' to update fields. Defaults to False.

        Raises:
            DocumentUpdateError: If the update operation fails

        Returns:
            UpdateResult: The result of the update operation
        """
        try:
            update_operator = "$addToSet" if add_to_set else "$set"
            formatted_data = {update_operator: update}

            result = self.get_collection(collection).update_many(criteria, formatted_data)

            if result.modified_count == 0:
                LOGGER.warning(
                    "[update_many] No documents matched criteria: %s in collection: %s", criteria, collection
                )

            return result
        except Exception as err:
            raise DocumentUpdateError(f"Failed to update documents in '{collection}': {err}") from err


    def update_public_id_counter(self, collection: str, value: int = None, increment: bool = False) -> None:
        """
        Updates or increments the public_id counter for the given collection

        Args:
            collection (str): Name of the collection
            value (int, optional): The new value to set for the counter. Ignored if `increment` is True.
            increment (bool, optional): If True, increments the counter by 1. Defaults to False.

        Raises:
            DocumentUpdateError: If the counter update operation fails or no valid operation is provided
        """
        try:
            working_collection = self.get_collection(PUBLIC_ID_COUNTER_COLLECTION)
            query = {'_id': collection}

            # Fetch the current counter document
            counter_doc = working_collection.find_one(query)

            if not counter_doc:
                # If the counter document does not exist, initialize it
                self.__init_public_id_counter(collection)
                counter_doc = working_collection.find_one(query)

            if increment:
                # If increment flag is True, increment by 1
                update_query = {'$inc': {'counter': 1}}
            elif value is not None and value > counter_doc['counter']:
                # If a specific value is provided and it is greater than the current counter, update it
                counter_doc['counter'] = value
                update_query = {'$set': {'counter': counter_doc['counter']}}
            else:
                return

            # Perform the update operation
            result = working_collection.update_one(query, update_query)

            if result.modified_count == 0:
                raise DocumentUpdateError(f"Failed to update PublicID counter for '{collection}'.")

        except Exception as err:
            raise DocumentUpdateError(f"Failed to update PublicID counter for '{collection}': {err}") from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def find_all(self, collection, *args, **kwargs) -> list:
        """
        Retrives documents from the specified collection

        Args:
            collection (str): The name of the collection to search in
            *args: Positional arguments for the search operation
            **kwargs: Keyword arguments for filtering, sorting, etc

        Raises:
            DocumentGetError: When documents could not be retrieved

        Returns:
            list: A list of retrieved documents
        """
        try:
            found_documents = self.find(collection, *args, **kwargs)

            return list(found_documents)
        except Exception as err:
            LOGGER.debug("[find_all] Can't retrive documents. Error: %s", err)
            raise DocumentGetError(f"Failed to retrieve documents from '{collection}': {err}") from err


    def find(self, collection: str, *args, **kwargs) -> Cursor:
        """
        Retrieves documents from the specified collection with optional filters and projections
        
        Args:
            collection (str): The name of the collection to search in.
            *args: Positional arguments for the find operation (e.g., query filter).
            **kwargs: Keyword arguments for filtering, sorting, limiting, etc.
                    Automatically adds 'projection' to exclude _id if not provided

        Raises:
            DocumentGetError: When documents could not be retrieved

        Returns:
            Cursor: MongoDB Cursor object with the results of the query
        """
        try:
            if 'projection' not in kwargs:
                kwargs.update({'projection': {'_id': 0}})

            return self.get_collection(collection).find(*args, **kwargs)
        except Exception as err:
            raise DocumentGetError(f"Failed to retrieve documents from collection '{collection}': {err}") from err


    def find_one_by(self, collection: str, *args, **kwargs) -> dict:
        """
        Find one specific document by special requirements

        Args:
            collection (str): Name of the database collection
            *args: Positional arguments for the find operation (e.g., query filter)
            **kwargs: Keyword arguments for filtering, sorting, limiting, etc

        Raises:
            DocumentGetError: If the retrieval fails due to an error

        Returns:
            dict: The found document or None if no document matches the criteria
        """
        try:
            cursor_result = self.find(collection, limit=1, *args, **kwargs)

            result = next(cursor_result, None)

            return result  # Return None if no result is found
        except Exception as err:
            raise DocumentGetError(f"Failed to retrieve document from collection '{collection}': {err}") from err


    def find_one(self, collection: str, public_id: int, *args, **kwargs) -> dict:
        """
        Retrieves a single document with the given public_id from the specified collection

        Args:
            collection (str): Name of the database collection.
            public_id (int): The public_id of the document to retrieve
            *args: Additional arguments for the find operation
            **kwargs: Additional keyword arguments for the find operation

        Raises:
            DocumentGetError: If there is an issue retrieving the document

        Returns:
            dict: The document with the given public_id, or None if not found
        """
        try:
            cursor_result = self.find(collection, {'public_id': public_id}, limit=1, *args, **kwargs)

            for result in cursor_result.limit(-1):
                return result
        except Exception as err:
            raise DocumentGetError(
                f"Failed to retrieve document with public_id {public_id} from collection '{collection}': {err}"
            ) from err


    def count(self, collection: str, *args, criteria: dict = None, **kwargs) -> int:
        """
        Count documents based on criteria parameters

        Args:
            collection (str): Name of database collection
            *args: Additional arguments for the count operation
            criteria (dict): Document count requirements (default is empty criteria)
            **kwargs: Additional keyword arguments for the count operation

        Raises:
            DocumentGetError: When the count operation fails

        Returns:
            int: The count of the documents that match the criteria
        """
        # Ensure criteria is a dictionary (defaulting to empty if None is provided)
        criteria = criteria or {}

        try:
            return self.get_collection(collection).count_documents(criteria, *args, **kwargs)
        except Exception as err:
            raise DocumentGetError(
                f"Failed to count documents in collection '{collection}': {err}"
            ) from err


    def aggregate(self, collection: str, *args, **kwargs) -> Cursor:
        """
        Perform aggregation on MongoDB

        Args:
            collection (str): Name of the database collection
            *args: Additional arguments for the aggregation pipeline
            **kwargs: Additional keyword arguments for the aggregation operation (including allowDiskUse)

        Raises:
            DocumentAggregationError: If the aggregation operation fails

        Returns:
            Cursor: The computed aggregation results as a cursor
        """
        try:
            return self.get_collection(collection).aggregate(*args, **kwargs, allowDiskUse=True)
        except Exception as err:
            raise DocumentAggregationError(f"Aggregation operation failed: {err}") from err


    def get_highest_id(self, collection: str) -> int:
        """
        Wrapper function that calls get_document_with_highest_id() and returns the highest public_id

        Args:
            collection (str): Name of database collection

        Raises:
            DocumentGetError: When documents could not be retrieved

        Returns:
            int: Highest public id or 0 if no document is found
        """
        try:
            formatted_sort = [('public_id', -1)]

            # Get the highest public_id document
            highest_id_doc = self.find_one_by(collection=collection, sort=formatted_sort)

            # If no document is found, return 0
            if highest_id_doc is None:
                return 0

            return int(highest_id_doc['public_id'])

        except Exception as err:
            raise DocumentGetError(
                f"Failed to retrieve the highest public_id from collection '{collection}': {err}"
            ) from err


    def get_next_public_id(self, collection: str) -> int:
        """
        Retrieves the next public_id for the specified collection

        Args:
            collection (str): Name of the database collection

        Raises:
            DocumentGetError: If there was an error getting or updating the counter document

        Returns:
            int: The next available public_id for the collection
        """
        try:
            found_counter = self.get_collection(PUBLIC_ID_COUNTER_COLLECTION).find_one({'_id': collection})

            if found_counter:
                new_id = found_counter['counter'] + 1
            else:
                docs_count = self.__init_public_id_counter(collection)
                new_id = docs_count + 1

            self.update_public_id_counter(collection)

            return new_id
        except Exception as err:
            raise DocumentGetError(f"Error retrieving next public_id for collection '{collection}': {err}") from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete(self, collection: str, criteria: dict) -> DeleteResult:
        """
        Deletes a document from the specified collection based on the given criteria

        Args:
            collection (str): Name of the database collection
            criteria (dict): Filter query to identify the document to delete

        Raises:
            DocumentDeleteError: When the document could not be deleted

        Returns:
            DeleteResult: Contains the result of the delete operation
        """
        try:
            result = self.get_collection(collection).delete_one(criteria)

            return result
        except Exception as err:
            raise DocumentDeleteError(f"Error deleting document from collection '{collection}': {err}") from err


    def delete_many(self, collection: str, **requirements: dict) -> DeleteResult:
        """
        Removes all documents that match the filter from the collection

        Args:
            collection (str): Name of the database collection
            requirements (dict): Specifies the deletion criteria using query operators

        Raises:
            DocumentDeleteError: When documents could not be deleted

        Returns:
            DeleteResult: The result of the delete operation, including the number of documents deleted
        """
        try:
            return self.get_collection(collection).delete_many(requirements)
        except Exception as err:
            raise DocumentDeleteError(f"Error deleting documents from collection '{collection}': {err}") from err

# ---------------------------------------------- CmdbLocation - SECTION ---------------------------------------------- #

    #TODO: REFACTOR-FIX (Move to seperate file)
    def set_root_location(self, collection: str, create: bool = False) -> UpdateResult:
        """
        Set up the root location. If no counter for locations exists, it will be created

        Args:
            collection (str): The framework.locations collection
            create (bool): If true the root location will be created, else it will be updated

        Raises:
            DocumentUpdateError: If there is an error during the root location setup, including issues with the
                                 database operation or creation of the public ID counter
            
        Returns:
            status: status of location creation or update
        """
        try:
            # If creation is requested, ensure the counter exists
            if create:
                # Check if the counter exists, if not initialize it
                if not self.get_collection(PUBLIC_ID_COUNTER_COLLECTION).find_one({'_id': collection}):
                    self.__init_public_id_counter(collection)

                # Insert root location data
                status = self.insert(collection, get_root_location_data())

            else:
                # Update the root location data
                status = self.update(collection, {'public_id': 1}, get_root_location_data())

            return status

        except Exception as err:
            raise DocumentUpdateError(f"Error setting up root location for collection '{collection}': {err}") from err

# ------------------------------------------- CmdbSectionTemplate - Section ------------------------------------------ #

    #TODO: REFACTOR-FIX (Move to seperate file)
    def init_predefined_templates(self, collection: str) -> None:
        """
        Checks if all predefined templates are created, else creates them.

        Args:
            collection (str): The name of the collection where templates are stored

        Raises:
            DocumentInsertError: If there is an error inserting predefined templates into the collection
            DocumentGetError: If there is an error fetching data from the collection, such as when checking
                              for existing templates or counters
        """
        try:
            counter = self.get_collection(PUBLIC_ID_COUNTER_COLLECTION).find_one({'_id': collection})

            if not counter:
                self.__init_public_id_counter(collection)

            predefined_template_creator = SectionTemplateCreator()
            predefined_templates: list[dict] = predefined_template_creator.get_predefined_templates()

            for predefined_template in predefined_templates:
                # First, check if the template already exists
                template_name = predefined_template['name']
                result = self.get_collection(collection).find_one({'name': template_name})

                if not result:
                    # The template does not exist, create it
                    LOGGER.info("Creating Template: %s", template_name)
                    self.insert(collection, predefined_template)
        except DocumentGetError as err:
            raise DocumentGetError(
                f"Error retrieving templates or counter for collection '{collection}': {err}"
            ) from err
        except Exception as err:
            raise DocumentInsertError(
                f"Error initializing predefined templates for collection '{collection}': {err}"
            ) from err

# ----------------------------------------------- CmdbReport - Section ----------------------------------------------- #

    #TODO: REFACTOR-FIX (Move to seperate file)
    def create_general_report_category(self, collection: str) -> None:
        """
        Creates the General Report Category if it does not already exist

        Args:
            collection (str): The name of the collection where the general report category is stored

        Raises:
            DocumentGetError: If there is an error fetching the counter or the report category
            DocumentInsertError: If there is an error inserting the general report category into the collection
        """
        try:
            counter = self.get_collection(PUBLIC_ID_COUNTER_COLLECTION).find_one({'_id': collection})

            if not counter:
                self.__init_public_id_counter(collection)

            result = self.get_collection(collection).find_one({'name': 'General'})

            if not result:
                # The category does not exist, create it
                LOGGER.info("Creating 'General' Report Category")

                general_category = {
                    'name': 'General',
                    'predefined': True,
                }

                self.insert(collection, general_category)
        except DocumentGetError as err:
            LOGGER.error("[create_general_report_category] Error fetching document. Error: %s", err)
            raise DocumentGetError(
                f"Error retrieving counter or report category for collection '{collection}': {err}"
            ) from err
        except DocumentInsertError as err:
            LOGGER.error("[create_general_report_category] Error inserting report category. Error: %s", err)
            raise DocumentInsertError(
                f"Error creating 'General' report category for collection '{collection}': {err}"
            ) from err
        except Exception as err:
            LOGGER.error("[create_general_report_category] Unexpected error. Error: %s", err)
            raise DocumentInsertError(
                f"Unexpected error while creating 'General' report category for collection '{collection}': {err}"
            ) from err

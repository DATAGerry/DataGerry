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
This module provides the `MongoConnector` class to establish and manage a connection 
to a MongoDB database
"""
import os
import logging
from pymongo import MongoClient
from pymongo.database import Database

from cmdb.database.connection_status import ConnectionStatus

from cmdb.errors.database import DatabaseConnectionError, SetDatabaseError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                MongoConnector - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class MongoConnector:
    """
    MongoConnector is managing the connection to a MongoDB database using PyMongo
    """
    def __init__(self, host: str, port: int, database_name: str, client_options: dict = None):
        """
        Initialises the connection to MongoDB and the attributes of the `MongoConnector`

        Args:
            `host` (str): Host of the connection
            `port` (int): Port of the connection
            `database_name` (str): Name of the database
            `client_options` (dict, optional): Additional client options. Defaults to None.

        Raises:
            `DatabaseConnectionError`: When the connection initialisation failed
        """
        try:
            connection_string = os.getenv('CONNECTION_STRING')

            if connection_string:
                self.client = MongoClient(connection_string)
            else:
                # Use the provided host and port to create the client
                if client_options:
                    self.client = MongoClient(host=host, port=int(port), connect=False, **client_options)
                else:
                    self.client = MongoClient(host=host, port=int(port), connect=False)

            self.database: Database = self.client.get_database(database_name)
            self.host = host
            self.port = port
        except Exception as err:
            raise DatabaseConnectionError(err) from err


    def __exit__(self, *err):
        """
        Automatically disconnects the `MongoConnector` when exiting the context manager
        """
        self.disconnect()



    def set_database(self, db_name: str) -> None:
        """
        Sets the database of the `MongoConnector`

        Args:
            `db_name` (str): Name of the database

        Raises:
            `SetDatabaseError`: Raised when not possible to set connector to `db_name`
        """
        try:
            self.database = self.client.get_database(db_name)
        except Exception as err:
            raise SetDatabaseError(err) from err


    def connect(self) -> ConnectionStatus:
        """
        Checks if database is reachable

        Raises:
            DatabaseConnectionError: If the database connection check fails

        Returns:
            ConnectionStatus: The current connection status, indicating success or failure
        """
        try:
            response = self.client.admin.command('hello')
            if response.get("ok") == 1:
                return ConnectionStatus(connected=True, message=str(response))

            raise DatabaseConnectionError("Unexpected response from database: " + str(response))
        except Exception as err:
            raise DatabaseConnectionError(err) from err


    def disconnect(self) -> ConnectionStatus:
        """
        Closes the connection to the database

        Returns:
            ConnectionStatus: The status indicating the disconnection result
        """
        try:
            if self.client:
                self.client.close()
                return ConnectionStatus(connected=False, message="Successfully disconnected from the database.")

            return ConnectionStatus(connected=False, message="No active database connection to close.")
        except Exception as err:
            return ConnectionStatus(connected=False, message=f"Error while disconnecting: {err}")


    def is_connected(self) -> bool:
        """
        Checks the current connection status to the database
        
        Returns:
            bool: True if successfully connected to the database, False otherwise
        """
        return self.connect().get_status()

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
This module contains the implementation of the RelationsManager
"""
import logging

from cmdb.database import MongoDatabaseManager

from cmdb.manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.relation_model import CmdbRelation

from cmdb.framework.results import IterationResult

from cmdb.errors.manager import (
    ManagerInsertError,
    ManagerGetError,
    ManagerUpdateError,
    ManagerDeleteError,
)
from cmdb.errors.manager.relations_manager import (
    RelationsManagerInsertError,
    RelationsManagerGetError,
    RelationsManagerIterationError,
    RelationsManagerUpdateError,
    RelationsManagerDeleteError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                               RelationsManager - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class RelationsManager(BaseManager):
    """
    The RelationsManager handles the interaction between the CmdbRelations-API and the database
    `Extends`: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the RelationsManager

        Args:
            `dbm` (MongoDatabaseManager): Database interaction manager
            `database` (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE
        """
        if database:
            dbm.connector.set_database(database)

        super().__init__(CmdbRelation.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_relation(self, relation: dict) -> int:
        """
        Insert a CmdbRelation into the database

        Args:
            `relation` (dict): Raw data of the CmdbRelation

        Raises:
            `RelationsManagerInsertError`: When a CmdbRelation could not be inserted into the database

        Returns:
            `int`: The public_id of the created CmdbRelation
        """
        #TODO: ERROR-FIX (try-catch block)
        if isinstance(relation, CmdbRelation):
            relation = CmdbRelation.to_json(relation)

        try:
            return self.insert(relation)
        except ManagerInsertError as err:
            raise RelationsManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_relation(self, public_id: int) -> dict:
        """
        Retrieves a CmdbRelation from the database

        Args:
            `public_id` (int): public_id of the CmdbRelation

        Raises:
            `RelationsManagerGetError`: When a CmdbRelation could not be retrieved

        Returns:
            `dict`: Raw data of the CmdbRelation
        """
        try:
            return self.get_one(public_id)
        except ManagerGetError as err:
            raise RelationsManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbRelation]:
        """
        Retrieves multiple CmdbRelations

        Args:
            `builder_params` (BuilderParameters): Filter for which CmdbRelations should be retrieved

        Raises:
            `RelationsManagerIterationError`: When the iteration failed

        Returns:
            `IterationResult[CmdbRelation]`: All CmdbRelations matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            # TODO: ERROR-FIX (catch IterationResult exceptions)
            iteration_result: IterationResult[CmdbRelation] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbRelation)
        except Exception as err:
            raise RelationsManagerIterationError(err) from err

        return iteration_result

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_relation(self, public_id:int, data: dict) -> None:
        """
        Updates a CmdbRelation in the database

        Args:
            `public_id` (int): public_id of the CmdbRelation which should be updated
            `data` (dict): The data with new values for the CmdbRelation

        Raises:
            `RelationsManagerUpdateError`: When the update operation fails
        """
        try:
            self.update({'public_id':public_id}, CmdbRelation.to_json(data))
        except ManagerUpdateError as err:
            raise RelationsManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_relation(self, public_id: int) -> bool:
        """
        Deletes a CmdbRelation from the database

        Args:
            `public_id` (int): public_id of the CmdbRelation which should be deleted

        Raises:
            `RelationsManagerDeleteError`: When the delete operation fails

        Returns:
            `bool`: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except ManagerDeleteError as err:
            raise RelationsManagerDeleteError(err) from err

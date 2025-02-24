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
This module contains the implementation of the ObjectRelationsManager
"""
import logging
from typing import Optional

from cmdb.database import MongoDatabaseManager

from cmdb.manager import BaseManager
from cmdb.manager.query_builder import BuilderParameters

from cmdb.models.object_relation_model import CmdbObjectRelation

from cmdb.framework.results import IterationResult

from cmdb.errors.manager import (
    BaseManagerInsertError,
    BaseManagerGetError,
    BaseManagerUpdateError,
    BaseManagerDeleteError,
)
from cmdb.errors.manager.object_relations_manager import (
    ObjectRelationsManagerInitError,
    ObjectRelationsManagerInsertError,
    ObjectRelationsManagerGetError,
    ObjectRelationsManagerIterationError,
    ObjectRelationsManagerUpdateError,
    ObjectRelationsManagerDeleteError,
)
from cmdb.errors.models.cmdb_object_relation import (
    CmdbObjectRelationToJsonError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            ObjectRelationsManager - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectRelationsManager(BaseManager):
    """
    The ObjectRelationsManager handles the interaction between the CmdbObjectRelations-API and the database
    `Extends`: BaseManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection for the ObjectRelationsManager

        Args:
            dbm (MongoDatabaseManager): Database interaction manager
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE

        Raises:
            ObjectRelationsManagerInitError: If the ObjectRelationsManager could not be initialised
        """
        try:
            if database:
                dbm.connector.set_database(database)

            super().__init__(CmdbObjectRelation.COLLECTION, dbm)
        except Exception as err:
            raise ObjectRelationsManagerInitError(err) from err

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_object_relation(self, object_relation: dict) -> int:
        """
        Insert a CmdbObjectRelation into the database

        Args:
            object_relation (dict): Raw data of the CmdbObjectRelation

        Raises:
            ObjectRelationsManagerInsertError: When a CmdbObjectRelation could not be inserted into the database

        Returns:
            int: The public_id of the created CmdbObjectRelation
        """
        try:
            if isinstance(object_relation, CmdbObjectRelation):
                object_relation = CmdbObjectRelation.to_json(object_relation)

            return self.insert(object_relation)
        except CmdbObjectRelationToJsonError as err:
            raise ObjectRelationsManagerInsertError(err) from err
        except BaseManagerInsertError as err:
            raise ObjectRelationsManagerInsertError(err) from err
        except Exception as err:
            LOGGER.error("[insert_object_relation] Exception: %s. Type: %s", err, type(err))
            raise ObjectRelationsManagerInsertError(err) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_object_relation(self, public_id: int) -> Optional[dict]:
        """
        Retrieves a CmdbObjectRelation from the database

        Args:
            public_id (int): public_id of the CmdbObjectRelation

        Raises:
            ObjectRelationsManagerGetError: When a CmdbObjectRelation could not be retrieved

        Returns:
            Optional[dict]: Dict representation of the CmdbObjectRelation attributes if it exists else None
        """
        try:
            return self.get_one(public_id)
        except BaseManagerGetError as err:
            raise ObjectRelationsManagerGetError(err) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[CmdbObjectRelation]:
        """
        Retrieves multiple CmdbObjectRelations

        Args:
            builder_params (BuilderParameters): Filter for which CmdbObjectRelations should be retrieved

        Raises:
            ObjectRelationsManagerIterationError: When the iteration failed

        Returns:
            IterationResult[CmdbRelation]: All CmdbObjectRelations matching the filter
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params)

            iteration_result: IterationResult[CmdbObjectRelation] = IterationResult(aggregation_result,
                                                                                    total,
                                                                                    CmdbObjectRelation)

            return iteration_result
        except Exception as err:
            raise ObjectRelationsManagerIterationError(err) from err

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_object_relation(self, public_id:int, data: dict) -> None:
        """
        Updates a CmdbObjectRelation in the database

        Args:
            public_id (int): public_id of the CmdbObjectRelation which should be updated
            data (dict): The data with new values for the CmdbObjectRelation

        Raises:
            ObjectRelationsManagerUpdateError: When the update operation fails
        """
        try:
            self.update({'public_id':public_id}, CmdbObjectRelation.to_json(data))
        except CmdbObjectRelationToJsonError as err:
            raise ObjectRelationsManagerUpdateError(err) from err
        except BaseManagerUpdateError as err:
            raise ObjectRelationsManagerUpdateError(err) from err
        except Exception as err:
            LOGGER.error("[update_object_relation] Exception: %s. Type: %s", err, type(err))
            raise ObjectRelationsManagerUpdateError(err) from err

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_object_relation(self, public_id: int) -> bool:
        """
        Deletes a CmdbObjectRelation from the database

        Args:
            public_id (int): public_id of the CmdbObjectRelation which should be deleted

        Raises:
            ObjectRelationsManagerDeleteError: When the delete operation fails

        Returns:
            bool: True if deletion was successful
        """
        try:
            return self.delete({'public_id':public_id})
        except BaseManagerDeleteError as err:
            raise ObjectRelationsManagerDeleteError(err) from err

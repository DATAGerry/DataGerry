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
This module contains the implementation of the ObjectLinksManager
"""
import logging
from typing import Union
from datetime import datetime, timezone

from cmdb.database import MongoDatabaseManager

from cmdb.manager.query_builder import BuilderParameters
from cmdb.manager import BaseManager

from cmdb.models.user_model.user import UserModel
from cmdb.models.object_link_model.link import CmdbObjectLink
from cmdb.models.object_model.cmdb_object import CmdbObject
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.framework.results import IterationResult

from cmdb.errors.manager import ManagerGetError, ManagerInsertError, ManagerDeleteError
from cmdb.errors.manager.object_links_manager import (
    ObjectLinksManagerInsertError,
    ObjectLinksManagerGetError,
    ObjectLinksManagerGetObjectError,
    ObjectLinksManagerIterationError,
    ObjectLinksManagerDeleteError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              ObjectLinksManager - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectLinksManager(BaseManager):
    """
    The ObjectLinksManager handles the interaction between the CmdbObjectLink-API and the database
    Extends: BaseManager
    """

    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            dbm (MongoDatabaseManager): Active database managers instance
            database (str): Name of the database to which the 'dbm' should connect. Only used in CLOUD_MODE
        """
        if database:
            dbm.connector.set_database(database)

        super().__init__(CmdbObjectLink.COLLECTION, dbm)


# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_object_link(self, link: Union[dict, CmdbObjectLink]) -> int:
        """
        Insert a single CmdbObjectLink into the database

        Args:
            link (dict/CmdbObjectLink): Data of the CmdbObjectLink as object or dictionary

        Raises:
            ObjectLinksManagerInsertError: When the CmdbObjectLink could not be inserted in the database
            ObjectLinksManagerGetObjectError: When a CmdbObject could not be retrived

        Returns:
            int: The public_id of the new inserted object link
        """
        try:
            if isinstance(link, CmdbObjectLink):
                link = CmdbObjectLink.to_json(link)

            if 'creation_time' not in link:
                link['creation_time'] = datetime.now(timezone.utc)

            # Verify both objects exist
            primary_object = self.get_one_from_other_collection(CmdbObject.COLLECTION, link['primary'])
            secondary_object = self.get_one_from_other_collection(CmdbObject.COLLECTION, link['secondary'])

            if not primary_object:
                raise ObjectLinksManagerGetObjectError(f"Object with ID: {link['primary']} not found!")
            if not secondary_object:
                raise ObjectLinksManagerGetObjectError(f"Object with ID: {link['secondary']} not found!")

            new_link_public_id = self.insert(link)
        except ManagerInsertError as err:
            LOGGER.debug("[insert_object_link] %s", err.message)
            raise ObjectLinksManagerInsertError(err.message) from err
        except (ManagerGetError, ObjectLinksManagerGetObjectError) as err:
            LOGGER.debug("[insert_object_link] %s", err.message)
            raise ObjectLinksManagerGetObjectError(err.message) from err

        return new_link_public_id

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def iterate(
            self,
            builder_params: BuilderParameters,
            user: UserModel = None,
            permission: AccessControlPermission = None) -> IterationResult[CmdbObjectLink]:
        """
        Iterates over CmdbObjectLinks

        Args:
            builder_params (BuilderParameters): Iteration conditions
            user (UserModel): CmdbUser requesting this operation
            permission (AccessControlPermission): Required permission for this operation

        Raises:
            ObjectLinksManagerIterationError: When an error occured during iteration

        Returns:
            IterationResult[CmdbObjectLink]: All CmdbObjectLinks matching the builder_params
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params, user, permission)

            iteration_result: IterationResult[CmdbObjectLink] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbObjectLink)
        except Exception as err:
            LOGGER.debug("[iterate] Exception: %s", err)
            raise ObjectLinksManagerIterationError(err) from err

        return iteration_result


    def get_link(self, public_id: int) -> CmdbObjectLink:
        """
        Retrieve a single CmdbObjectLink by its public_id

        Args:
            public_id (int): public_id of the CmdbObjectLink

        Raises:
            ObjectLinksManagerGetError: When the CmdbObjectLink could not be retrieved

        Returns:
            CmdbObjectLink: Instance of CmdbLink
        """
        try:
            link_instance = self.get_one(public_id)

            link = CmdbObjectLink.from_data(link_instance)
        except ManagerGetError as err:
            LOGGER.debug("[get_link] %s", err.message)
            raise ObjectLinksManagerGetError(f'CmdbObjectLink with ID: {public_id} not found!') from err

        return link


    def check_link_exists(self, criteria: dict) -> bool:
        """
        Checks if an CmdbObjectLink exists with given primary and secondary public_id of CmdbObjects

        Args:
            criteria (dict): Dict with primary and secondary public_id's

        Returns:
            bool: True if CmdbObjectLink exists, else False
        """
        try:
            link_instance = self.get_one_by(criteria)

            return bool(link_instance)
        except ManagerGetError:
            return False

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_object_link(self, public_id: int) -> CmdbObjectLink:
        """
        Deletes a CmdbObjectLink with the given public_id

        Args:
            public_id (int): public_id of the CmdbObjectLink

        Raises:
            ObjectLinksManagerGetError: When the CmdbObjectLink could not be retrieved
            ObjectLinksManagerDeleteError: When the CmdbObjectlink could not be deleted

        Returns:
            CmdbObjectLink: The retrieved instance of the CmdbObjectLink before it was deleted
        """
        try:
            link: dict = self.get_one(public_id)

            self.delete({'public_id':public_id})
        except ManagerGetError as err:
            LOGGER.debug("[delete_object_link] %s", err.message)
            raise ObjectLinksManagerGetError(err) from err
        except ManagerDeleteError as err:
            LOGGER.debug("[delete_object_link] %s", err.message)
            raise ObjectLinksManagerDeleteError(err) from err

        return link

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
This module contains the implementation of the PersonsManager
"""
import logging

from cmdb.database import MongoDatabaseManager

from cmdb.manager.generic_manager import GenericManager

from cmdb.models.person_model import CmdbPerson

from cmdb.errors.manager.persons_manager import PERSONS_MANAGER_ERRORS
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                PersonsManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class PersonsManager(GenericManager):
    """
    The PersonsManager manages the interaction between CmdbPersons and the database

    Extends: GenericManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        super().__init__(dbm, CmdbPerson, PERSONS_MANAGER_ERRORS, database)

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

    def update_group_in_persons(self, group_id: int, persons_to_add: list[int], persons_to_delete: list[int]) -> None:
        """
        Updates a CmdbPerson in CmdbPersonGroups during an update operation

        Args:
            group_id (int): public_id of CmdbPersonGroup which should be updated
            persons_to_add (list[int]): public_id's of CmdbPersons where the CmdbPersonGroup should be added
            persons_to_delete (list[int]): list of CmdbPerson public_id's which should be deleted
        """
        self.add_group_to_persons(group_id, persons_to_add)
        self.delete_group_from_persons(group_id, persons_to_delete)


    def add_group_to_persons(self, group_id: int, person_ids: list[int]) -> None:
        """
        Adds a CmdbPerson to the given CmdbPersonGroups

        Args:
            group_id (int): public_id of CmdbPersonGroup which should be added
            person_ids (list[int]): public_id's of CmdbPersons where the CmdbPersonGroup should be added
        """
        for person_id in person_ids:
            cur_person = self.get_item(person_id, as_dict=True)

            if cur_person:
                current_groups: list = cur_person.get('groups', [])

                if group_id not in current_groups:
                    current_groups.append(group_id)
                    cur_person['groups'] = current_groups
                    self.update_item(person_id, cur_person)


    def delete_group_from_persons(self, group_id: int, persons_ids: list[int] = None) -> None:
        """
        Removes a CmdbPersonGroup from all CmdbPersons

        Args:
            group_id (int): public_id of CmdbPersonGroup which should be deleted
            persons_ids (list[int], optional): list of CmdbPerson public_id's which should be deleted
        """
        if persons_ids is not None:
            # Use provided group IDs
            persons_with_group = [self.get_item(person_id) for person_id in persons_ids]
        else:
            # Otherwise, find all groups containing the person
            persons_with_group = self.find_all(criteria={'groups': group_id})

        for person in persons_with_group:
            if person is None:
                continue  # Skip if person wasn't found

            person_id = person['public_id']
            current_groups: list = person.get('groups', [])

            if group_id in current_groups:
                current_groups.remove(group_id)
                person['groups'] = current_groups
                self.update_item(person_id, person)

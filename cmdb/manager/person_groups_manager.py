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
This module contains the implementation of the PersonGroupsManager
"""
import logging

from cmdb.database import MongoDatabaseManager

from cmdb.manager.generic_manager import GenericManager

from cmdb.models.person_group_model import CmdbPersonGroup

from cmdb.errors.manager.person_groups_manager import PERSON_GROUPS_MANAGER_ERRORS
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              PersonGroupsManager - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class PersonGroupsManager(GenericManager):
    """
    The PersonGroupsManager manages the interaction between CmdbPersonGroups and the database

    Extends: GenericManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        super().__init__(dbm, CmdbPersonGroup, PERSON_GROUPS_MANAGER_ERRORS, database)

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

    def update_person_in_groups(self, person_id: int, groups_to_add: list[int], groups_to_delete: list[int]) -> None:
        """
        Updates a CmdbPerson in CmdbPersonGroups during an update operation

        Args:
            person_id (int): public_id of CmdbPerson which should be updated
            groups_to_add (list[int]): public_id's of CmdbPersonGroups where the CmdbPerson should be added
            groups_to_delete (list[int]): list of CmdbPersonGroup public_id's which should be deleted
        """
        self.add_person_to_groups(person_id, groups_to_add)
        self.delete_person_from_groups(person_id, groups_to_delete)


    def add_person_to_groups(self, person_id: int, group_ids: list[int]) -> None:
        """
        Adds a CmdbPerson to the given CmdbPersonGroups

        Args:
            person_id (int): public_id of CmdbPerson which should be added
            group_ids (list[int]): public_id's of CmdbPersonGroups where the CmdbPerson should be added
        """
        for group_id in group_ids:
            cur_group = self.get_item(group_id, as_dict=True)

            if cur_group:
                current_members: list = cur_group.get('group_members', [])

                if person_id not in current_members:
                    current_members.append(person_id)
                    cur_group['group_members'] = current_members
                    self.update_item(group_id, cur_group)


    def delete_person_from_groups(self, person_id: int, groups_ids: list[int] = None) -> None:
        """
        Removes a CmdbPerson from all CmdbPersonGroups

        Args:
            person_id (int): public_id of CmdbPerson which should be deleted
            groups_ids (list[int], optional): list of CmdbPersonGroup public_id's which should be deleted
        """
        if groups_ids is not None:
            # Use provided group IDs
            groups_with_person = [self.get_item(group_id) for group_id in groups_ids]
        else:
            # Otherwise, find all groups containing the person
            groups_with_person = self.find_all(criteria={'group_members': person_id})

        for group in groups_with_person:
            if group is None:
                continue  # Skip if group wasn't found

            group_id = group['public_id']
            current_members: list = group.get('group_members', [])

            if person_id in current_members:
                current_members.remove(person_id)
                group['group_members'] = current_members
                self.update_item(group_id, group)

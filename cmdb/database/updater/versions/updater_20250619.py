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
Implementation of Update20250619
"""
import logging

from cmdb.database.updater.base_database_update import BaseDatabaseUpdate

from cmdb.models.object_model import CmdbObject
from cmdb.models.type_model import CmdbType

from cmdb.errors.updater import UpdaterException
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                Update20250619 - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class Update20250619(BaseDatabaseUpdate):
    """
    Implementation of Update20250619
    """


    def creation_date(self) -> int:
        return 20250619


    def description(self) -> str:
        return """
               Add the property 'ci_explorer_tooltip' to all CmdbObjects which don't have it

               Add the property 'ci_explorer_label' to all CmdbTypes which don't have it
               """


    def start_update(self) -> None:
        try:
            #Update all CmdbObjects
            object_collection = CmdbObject.COLLECTION
            all_objects: list[dict] = []

            all_objects = self.dbm.find_all(object_collection, self.db_name)

            for cur_obj in all_objects:
                # Check if the object already has the property 'ci_explorer_tooltip', else create it
                if not 'ci_explorer_tooltip' in cur_obj.keys():
                    cur_public_id = cur_obj['public_id']
                    cur_obj['ci_explorer_tooltip'] = None

                    self.dbm.update(collection=object_collection,
                                    db_name=self.db_name,
                                    criteria={'public_id':cur_public_id},
                                    data=cur_obj)
                    LOGGER.info("Updated 'ci_explorer_tooltip' for Object-ID: %s", cur_public_id)

            # Update all CmdbTypes
            type_collection = CmdbType.COLLECTION
            all_types: list[dict] = []

            all_types = self.dbm.find_all(type_collection, self.db_name)

            for cur_type in all_types:
                # Check if the type already has the property 'ci_explorer_label', else create it
                if not 'ci_explorer_label' in cur_type.keys():
                    cur_public_id = cur_type['public_id']
                    cur_type['ci_explorer_label'] = None

                    self.dbm.update(collection=type_collection,
                                    db_name=self.db_name,
                                    criteria={'public_id':cur_public_id},
                                    data=cur_type)
                    LOGGER.info("Updated 'ci_explorer_label' for Type-ID: %s", cur_public_id)

            self.increase_updater_version(self.creation_date())
        except Exception as err:
            raise UpdaterException(err) from err

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
Implementation of ObjectTemplateData
"""
import logging

from cmdb.manager import ObjectsManager

from cmdb.framework.rendering.cmdb_render import CmdbRender
from cmdb.framework.rendering.render_result import RenderResult

from cmdb.errors.manager.objects_manager import ObjectsManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              ObjectTemplateData - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectTemplateData:
    """
    Prepares and retrieves template data for a given RenderResult
    """
    def __init__(self, cmdb_render_object: RenderResult, objects_manager: ObjectsManager):
        """
        Initializes the ObjectTemplateData

        Args:
            cmdb_render_object (RenderResult): The RenderResult to extract data from
            objects_manager (ObjectsManager): The manager handling CmdbObject
        """
        self.objects_manager = objects_manager
        self.template_data = self.extract_object_data(cmdb_render_object, 3)


    def get_template_data(self) -> dict:
        """
        Retrieves the processed template data

        Returns:
            dict: The structured template data extracted from the RenderResult
        """
        return self.template_data


    def extract_object_data(self, cmdb_render_object: RenderResult, depth: int) -> dict:
        """
        Recursively extracts object data from a RenderResult

        Args:
            cmdb_render_object (RenderResult): The RenderResult to extract data from
            depth (int): The recursion depth limit for resolving references

        Returns:
            dict: The extracted object data
        """
        data = {
            "id": cmdb_render_object.object_information.get("object_id"),
            "fields": {}
        }

        for field in cmdb_render_object.fields:
            field_name = field.get("name")
            field_type = field.get("type")
            field_value = field.get("value")

            if not field_name:
                continue

            try:
                if field_type in ("ref", "location") and field_value and depth > 0:
                    # resolve type
                    related_object = self.objects_manager.get_object(field_value)
                    object_type = self.objects_manager.get_object_type(related_object.get_type_id())

                    related_render = CmdbRender(related_object, object_type, None, False, self.objects_manager.dbm)

                    data["fields"][field_name] = self.extract_object_data(related_render.result(), depth - 1)
                elif field_type == 'ref-section-field':
                    data["fields"][field_name] = {
                        "fields": {ref["name"]: ref["value"] for ref in field.get("references", {}).get("fields", [])}
                    }
                else:
                    data["fields"][field_name] = field_value
            except ObjectsManagerGetError:
                LOGGER.error("Failed to retrieve object for field '%s'. Skipping.", field_name)
            except Exception as err:
                LOGGER.error("Exception processing field '%s': %s", field_name, err)

        return data

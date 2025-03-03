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
Implementation of CmdbType
"""
import logging
from typing import Optional, Union
from datetime import datetime, timezone
from dateutil.parser import parse

from cmdb.security.acl.access_control_list import AccessControlList
from cmdb.models.cmdb_dao import CmdbDAO
from cmdb.models.type_model.type_summary import TypeSummary
from cmdb.models.type_model.type_external_link import TypeExternalLink
from cmdb.models.type_model.type_section import TypeSection
from cmdb.models.type_model.type_render_meta import TypeRenderMeta
from cmdb.class_schema.cmdb_type_schema import get_cmdb_type_schema

from cmdb.errors.models.cmdb_type import (
    CmdbTypeInitError,
    CmdbTypeInitFromDataError,
    CmdbTypeToJsonError,
    CmdbTypeFieldNotFoundError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   CmdbType - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
#pylint: disable=too-many-instance-attributes
class CmdbType(CmdbDAO):
    """
    Represents a CmdbType in DataGerry

    Extends: CmdbDAO
    """
    COLLECTION = "framework.types"
    MODEL = 'Type'
    DEFAULT_VERSION = '1.0.0'
    SCHEMA: dict = get_cmdb_type_schema()

    INDEX_KEYS = [{
        'keys': [('name', CmdbDAO.DAO_ASCENDING)],
        'name': 'name',
        'unique': True
    }]

    #pylint: disable=too-many-arguments
    #pylint: disable=too-many-locals
    def __init__(self, public_id: int,
                 name: str,
                 author_id: int,
                 render_meta: TypeRenderMeta,
                 creation_time: datetime = None,
                 last_edit_time: datetime = None,
                 editor_id: int = None,
                 active: bool = True,
                 selectable_as_parent: bool = True,
                 global_template_ids: list[int] = None,
                 fields: list = None, version: str = None,
                 label: str = None,
                 description: str = None,
                 acl: AccessControlList = None):
        """
        Initializes a CmdbType

        Args:
            public_id (int): unique public_id of the CmdbType
            name (str): The name of the CmdbType
            author_id (int): The public_id of the CmdbUser who created the CmdbType
            render_meta (TypeRenderMeta): Metadata related to rendering
            creation_time (datetime, optional): The time when the CmdbType was created.
                                                Defaults to the current UTC time if not provided
            last_edit_time (datetime, optional): The last time the CmdbType was edited
            editor_id (int, optional): The public_id of the CmdbUser who last edited the CmdbType
            active (bool): Indicates whether the object is active. Defaults to True
            selectable_as_parent (bool): Whether this CmdbType can be a parent Location. Defaults to True
            global_template_ids (list[int]): A list of global template public_ids used by this CmdbType
            fields (list): A list of fields associated with the CmdbType
            version (str): The version of the CmdbType. Defaults to 1.0.0
            label (str): A user-friendly label for the CmdbType. Defaults to a title-cased version of the name
            description (str, optional): A description of the CmdbType
            acl (AccessControlList, optional): AccessControlList for the CmdbType. Defaults to none

        Raises:
            CmdbTypeInitError: If initialization fails due to an error
        """
        try:
            self.name = name
            self.label = label or self.name.title()
            self.description = description
            self.version = version or CmdbType.DEFAULT_VERSION
            self.selectable_as_parent = selectable_as_parent
            self.global_template_ids = global_template_ids or []
            self.active = active
            self.author_id = author_id
            self.creation_time = creation_time or datetime.now(timezone.utc)
            self.editor_id = editor_id
            self.last_edit_time = last_edit_time
            self.render_meta = render_meta
            self.fields = fields or []
            self.acl = acl

            super().__init__(public_id=public_id)
        except Exception as err:
            raise CmdbTypeInitError(err) from err

# --------------------------------------------------- CLASS METHODS -------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "CmdbType":
        """
        Initialises a CmdbType from a dict

        Args:
            data (dict): Data with which the CmdbType should be initialised

        Raises:
            CmdbTypeInitFromDataError: If the initialisation with the given data fails

        Returns:
            CmdbType: CmdbType with the given data
        """
        try:
            creation_time = data.get('creation_time')
            if isinstance(creation_time, str):
                creation_time = parse(creation_time, fuzzy=True)

            last_edit_time = data.get('last_edit_time')
            if isinstance(last_edit_time, str):
                last_edit_time = parse(last_edit_time, fuzzy=True)

            return cls(
                public_id = data.get('public_id'),
                name = data.get('name'),
                selectable_as_parent = data.get('selectable_as_parent', True),
                global_template_ids = data.get('global_template_ids', []),
                active = data.get('active', True),
                author_id = data.get('author_id'),
                creation_time = creation_time,
                editor_id = data.get('editor_id', None),
                last_edit_time = last_edit_time,
                label = data.get('label', None),
                version = data.get('version', None),
                description = data.get('description', None),
                render_meta = TypeRenderMeta.from_data(data.get('render_meta', {})),
                fields = data.get('fields', None) or [],
                acl = AccessControlList.from_data(data.get('acl', {}))
            )
        except Exception as err:
            raise CmdbTypeInitFromDataError(err) from err


    @classmethod
    def to_json(cls, instance: "CmdbType") -> dict:
        """
        Converts a CmdbType into a json compatible dict

        Args:
            instance (CmdbType): The CmdbType which should be converted

        Raises:
            CmdbTypeToJsonError: If the CmdbType could not be converted to a json compatible dict

        Returns:
            dict: Json compatible dict of the CmdbType values
        """
        try:
            return {
                'public_id': instance.get_public_id(),
                'name': instance.name,
                'selectable_as_parent': instance.selectable_as_parent,
                'global_template_ids': instance.global_template_ids,
                'active': instance.active,
                'author_id': instance.author_id,
                'creation_time': instance.creation_time,
                'editor_id': instance.editor_id,
                'last_edit_time': instance.last_edit_time,
                'label': instance.label,
                'version': instance.version,
                'description': instance.description,
                'render_meta': TypeRenderMeta.to_json(instance.render_meta),
                'fields': instance.fields,
                'acl': AccessControlList.to_json(instance.acl)
            }
        except Exception as err:
            raise CmdbTypeToJsonError(err) from err

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

    def get_name(self) -> str:
        """
        Returns the name of the CmdbType

        Returns:
            str: The name of the CmdbType
        """
        return self.name


    def get_label(self) -> str:
        """
        Returns the display label of the CmdbType
        
        If no label is set, it defaults to the title-cased name
        
        Returns:
            str: The display label of the CmdbType
        """
        if not self.label:
            self.label = self.name.title()

        return self.label


    def get_externals(self) -> list[TypeExternalLink]:
        """
        Retrieves the external links from the TypeRenderMeta

        Returns:
            list[TypeExternalLink]: A list of external links associated with the TypeRenderMeta
        """
        return self.render_meta.externals


    def has_externals(self) -> bool:
        """
        Checks if the CmdbType has external links

        Returns:
            bool: True if external links exist, False otherwise
        """
        return bool(self.get_externals())


    def get_external(self, name: str) -> Optional[TypeExternalLink]:
        """
        Retrieves a TypeExternalLink by name

        Args:
            name (str): The name of the TypeExternalLink to retrieve

        Returns:
            Optional[TypeExternalLink]: The matching TypeExternalLink if found, otherwise None
        """
        return next((external for external in self.get_externals() if external.name == name), None)


    def has_summaries(self) -> bool:
        """
        Checks if there are any fields in the `summary` object of the TypeRenderMeta

        Returns:
            bool: True if there are fields in the summary, False otherwise
        """
        return self.render_meta.summary.has_fields()


    def get_nested_summaries(self) -> list[dict]:
        """
        Retrieves the nested summaries from fields of type 'ref'

        This method searches through the fields and returns any associated 'summaries' 
        for fields where the type is 'ref' and 'summaries' is present

        Returns:
            list[dict]: A list of dictionaries representing the nested summaries. 
                        If no matching fields are found, returns an empty list
        """
        return next((x['summaries'] for x in self.get_fields() if x['type'] == 'ref' and 'summaries' in x), [])


    def has_nested_prefix(self, nested_summaries: list[dict]) -> Union[str, bool]:
        """
        Checks if any of the nested summaries have a matching prefix for this instance

        This method looks for a nested summary with a matching `type_id` (equal to `self.public_id`)
        and returns the associated `prefix`. If no matching summary is found, it returns `False`

        Args:
            nested_summaries (List[dict]): A list of nested summary dictionaries that may contain a `type_id`
                                            and `prefix` key

        Returns:
            Union[str, bool]: The `prefix` of the matching nested summary if found, otherwise `False`
        """
        return next((x['prefix'] for x in nested_summaries if x['type_id'] == self.public_id), False)


    def get_nested_summary_fields(self, nested_summaries: list[dict]) -> list[str]:
        """
        Retrieves the fields from the nested summaries that match the current CmdbType's public_id

        This method looks through the `nested_summaries` to find a matching `type_id` that equals `self.public_id`.
        Once the matching nested summary is found, it gathers the corresponding field names and fetches their
        details using `get_field`. The fields are then returned as a list.

        Args:
            nested_summaries (list[dict]): A list of nested summary dictionaries containing `type_id` and `fields`

        Returns:
            list[str]: A list of fields corresponding to the nested summaries,
                       where each field is fetched using `get_field`.
        """
        complete_field_list = []

        _fields = next((x['fields'] for x in nested_summaries if x['type_id'] == self.public_id), [])

        for field_name in _fields:
            complete_field_list.append(self.get_field(field_name))

        return TypeSummary(complete_field_list).fields


    def get_nested_summary_line(self, nested_summaries: list[dict]) -> Optional[str]:
        """
        Retrieves the 'line' value from the nested summaries that match the current CmdbType's public_id

        This method looks through the `nested_summaries` to find a matching `type_id` that equals `self.public_id`
        Once the matching nested summary is found, it returns the associated `line` value.
        If no match is found, it returns `None`

        Args:
            nested_summaries (list[dict]): A list of nested summary dictionaries containing `type_id` and `line`

        Returns:
            Optional[str]: The `line` value from the matching nested summary if found, otherwise `None`
        """
        return next((x['line'] for x in nested_summaries if x['type_id'] == self.public_id), None)


    def get_summary(self) -> TypeSummary:
        """
        Retrieves the summary of fields from the TypeRenderMeta

        This method iterates over the fields defined in the `summary` of the TypeRenderMeta,
        fetches the details of each field using `get_field`, and returns a `TypeSummary` 
        containing these fields

        Returns:
            TypeSummary: A `TypeSummary` object containing the list of fields fetched from `get_field`
        """
        complete_field_list = [self.get_field(field_name) for field_name in self.render_meta.summary.fields]

        return TypeSummary(complete_field_list)


    def get_sections(self) -> list[TypeSection]:
        """
        Retrieves the sections from the TypeRenderMeta

        Returns:
            List[TypeSection]: A list of `TypeSection` objects defined in the `render_meta.sections`
        """
        return self.render_meta.sections


    def get_section(self, name: str) -> Optional[TypeSection]:
        """
        Retrieves a section with the given name

        Args:
            name (str): Name of the section

        Returns:
            Optional[TypeSection]: The Typesection with the given name else None
        """
        return next((section for section in self.get_sections() if section.name == name), None)



    def get_icon(self) -> Optional[str]:
        """
        Retrieves the icon of the current CmdbType

        This method returns the `icon` from the `render_meta` if available. If not, 
        it returns `None`

        Returns:
            Optional[str]: The icon as a string if available, otherwise `None`
        """
        return getattr(self.render_meta, 'icon', None)


    def has_sections(self) -> bool:
        """
        Checks if the CmdbType has any sections

        This method returns True if the CmdbType has one or more sections, otherwise it returns False

        Returns:
            bool: True if at least one section is present, False otherwise
        """
        return len(self.get_sections()) > 0


    def get_fields(self) -> list:
        """
        Retrieves all fields of the CmdbType

        This method returns the list of fields associated with the current `CmdbType`

        Returns:
            List: A list of fields for the current `CmdbType`
        """
        return self.fields


    def get_field(self, name: str) -> dict:
        """
        Retrieves a field by its name

        Args:
            name (str): The name of the field to retrieve

        Raises:
            CmdbTypeFieldNotFoundError: If no field with the specified name is found

        Returns:
            dict: The field as a dictionary
        """
        field = next((x for x in self.fields if x['name'] == name), None)

        if field:
            return field

        raise CmdbTypeFieldNotFoundError(f"Field '{name}' was not found!")


    def get_all_mds_fields(self) -> list:
        """
        Retrieves all fields from multi-data sections

        This method searches through the sections in the `render_meta` and collects all
        fields that belong to sections of type "multi-data-section"

        Returns:
            list: A list containing all fields from multi-data sections
        """
        mds_fields = []

        for section in self.render_meta.sections:
            if section.type == "multi-data-section":
                mds_fields.extend(section.fields)

        return mds_fields


    def get_all_fields_of_type(self, field_type: str) -> list[str]:
        """
        Retrieves all field names of the specified type

        This method iterates through the fields and collects the names of fields 
        that match the given `field_type`

        Args:
            field_type (str): The type of the field to search for

        Returns:
            list[str]: A list of field names that match the specified field type
        """
        field_names = [field["name"] for field in self.fields if field["type"] == field_type]

        return field_names

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
Represents a CmdbType in DataGerry
"""
import logging
from datetime import datetime, timezone
from dateutil.parser import parse

from cmdb.security.acl.control import AccessControlList
from cmdb.models.cmdb_dao import CmdbDAO
from cmdb.models.type_model.type_summary import TypeSummary
from cmdb.models.type_model.type_external_link import TypeExternalLink
from cmdb.models.type_model.type_section import TypeSection
from cmdb.models.type_model.type_render_meta import TypeRenderMeta
from cmdb.class_schema.cmdb_type_schema import get_cmdb_type_schema

from cmdb.errors.type import FieldNotFoundError, FieldInitError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   CmdbType - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
#pylint: disable=too-many-instance-attributes
class CmdbType(CmdbDAO):
    """
    Model for CmdbType in DataGerry
    `Extends`: CmdbDAO
    
    Attributes:
        COLLECTION (str): Name of the database collection
        MODEL (Model): Name of the DAO
        DEFAULT_VERSION (str): The default "starting" version number
        SCHEMA (dict): The validation schema for this DAO
        INDEX_KEYS (list): sList of index keys for the database
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
            LOGGER.debug("[__init__] Exception: %s, Type: %s", err, type(err))
            #TODO: ERROR-FIX (proper error required)
            raise Exception(err) from err

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "CmdbType":
        """
        Generates a CmdbType instance from a dict

        Args:
            data (dict): Data with which the CmdbType should be instantiated

        Returns:
            CmdbType: CmdbType instance with given data
        """
        try:
            creation_time = data.get('creation_time', None)
            if creation_time and isinstance(creation_time, str):
                creation_time = parse(creation_time, fuzzy=True)

            last_edit_time = data.get('last_edit_time', None)
            if last_edit_time and isinstance(last_edit_time, str):
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
            #TODO: ERROR-FIX (specific required)
            LOGGER.debug("[from_data] Exception: %s, Type: %s", err, type(err))
            raise Exception(err) from err


    @classmethod
    def to_json(cls, instance: "CmdbType") -> dict:
        """
        Convert a CmdbType instance to json conform data
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
            #TODO: ERROR-FIX (specific required)
            LOGGER.debug("[to_json] Exception: %s, Type: %s", err, type(err))
            raise Exception(err) from err

# ------------------------------------------------- GENERAL FUNCTIONS ------------------------------------------------ #

    def get_name(self) -> str:
        """Get the name of the type"""
        return self.name


    def get_label(self) -> str:
        """Get the display name"""
        if not self.label:
            self.label = self.name.title()

        return self.label


    def get_externals(self) -> list[TypeExternalLink]:
        """Get the render meta values of externals"""
        return self.render_meta.externals


    def has_externals(self) -> bool:
        """Check if type has external links"""
        return len(self.get_externals()) > 0


    def get_external(self, name) -> TypeExternalLink:
        """Retrive an external link"""
        return next((external for external in self.get_externals() if external.name == name), None)


    def has_summaries(self) -> bool:
        """Checks if there are any fields in the render_meta.summary object"""
        return self.render_meta.summary.has_fields()


    def get_nested_summaries(self):
        """document"""
        #TODO: DOCUMENT-FIX
        return next((x['summaries'] for x in self.get_fields() if x['type'] == 'ref' and 'summaries' in x), [])


    def has_nested_prefix(self, nested_summaries):
        """document"""
        #TODO: DOCUMENT-FIX
        return next((x['prefix'] for x in nested_summaries if x['type_id'] == self.public_id), False)


    def get_nested_summary_fields(self, nested_summaries) -> list[str]:
        """document"""
        #TODO: DOCUMENT-FIX
        _fields = next((x['fields'] for x in nested_summaries if x['type_id'] == self.public_id), [])
        complete_field_list = []
        for field_name in _fields:
            complete_field_list.append(self.get_field(field_name))

        return TypeSummary(fields=complete_field_list).fields


    def get_nested_summary_line(self, nested_summaries):
        """document"""
        #TODO: DOCUMENT-FIX
        return next((x['line'] for x in nested_summaries if x['type_id'] == self.public_id), None)


    def get_summary(self) -> TypeSummary:
        """document"""
        #TODO: DOCUMENT-FIX
        complete_field_list = []
        for field_name in self.render_meta.summary.fields:
            complete_field_list.append(self.get_field(field_name))
        return TypeSummary(fields=complete_field_list)


    def get_sections(self) -> list[TypeSection]:
        """document"""
        #TODO: DOCUMENT-FIX
        return self.render_meta.sections


    def get_section(self, name: str) -> TypeSection:
        """
        Retrieves a section with the given name

        Args:
            name (str): Name of the section

        Returns:
            TypeSection: The Typesection with the given name else None
        """
        try:
            return next((section for section in self.get_sections() if section.name == name), None)
        except IndexError:
            return None


    def get_icon(self) -> str:
        """Retrieves the icon of the current CmdbType"""
        try:
            return self.render_meta.icon
        except IndexError:
            return None


    def has_sections(self) -> bool:
        """
        Checks if the CmdbType has any sections

        Returns:
            (bool): True if at least one section is present else False
        """
        return self.get_sections() > 0


    def get_fields(self) -> list:
        """Retuns all fields of the CmdbType"""
        return self.fields


    def count_fields(self) -> int:
        """Returns the number of fields"""
        return len(self.fields)


    def get_fields_of_type_with_value(self, input_type: str, _filter: str, value) -> list:
        """document"""
        #TODO: DOCUMENT-FIX
        fields = [x for x in self.fields if
                  x['type'] == input_type and (value in x.get(_filter, None) if isinstance(x.get(_filter, None), list)
                                               else x.get(_filter, None) == value)]
        if fields:
            return fields

        raise FieldNotFoundError(f"Field '{value}' was not found!")


    def get_field(self, name) -> dict:
        """document"""
        #TODO: DOCUMENT-FIX
        field = [x for x in self.fields if x['name'] == name]
        if field:
            try:
                return field[0]
            except Exception as err:
                #TODO: ERROR-FIX
                raise FieldInitError(f"Field '{name}' could not be initialized") from err

        raise FieldNotFoundError(f"Field '{name}' was not found!")


    def get_all_mds_fields(self) -> list:
        """document"""
        #TODO: DOCUMENT-FIX
        mds_fields = []

        for a_section in self.render_meta.sections:
            if a_section.type == "multi-data-section":
                for a_field in a_section.fields:
                    mds_fields.append(a_field)

        return mds_fields


    def get_all_fields_of_type(self, field_type: str) -> list:
        """document"""
        #TODO: DOCUMENT-FIX
        date_fields = []

        for a_field in self.fields:
            if a_field['type'] == field_type:
                date_fields.append(a_field['name'])

        return date_fields

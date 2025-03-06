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
The schema of a CmdbObject
"""
# -------------------------------------------------------------------------------------------------------------------- #
# pylint: disable=R0801
def get_cmdb_object_schema() -> dict:
    """
    Returns the CmdbObjectSchema

    Returns:
        dict: Schema of the CmdbObject
    """
    return {
        'public_id': {
            'type': 'integer'
        },
        'type_id': {
            'type': 'integer'
        },
        'version': {
            'type': 'string',
            'default': '1.0.0'
        },
        'author_id': {
            'type': 'integer',
            'required': True
        },
        'creation_time': {
            'type': 'dict',
            'nullable': True,
            'required': False
        },
        'last_edit_time': {
            'type': 'dict',
            'nullable': True,
            'required': False
        },
        'active': {
            'type': 'boolean',
            'required': False,
            'default': True
        },
        'fields': {
            'type': 'list',
            'required': True,
            'default': [],
        },
        'multi_data_sections': {
            'type': 'list',
            'required': False,
            'default': [],
        }
    }

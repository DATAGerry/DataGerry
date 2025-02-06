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
"""TODO: document"""
# -------------------------------------------------------------------------------------------------------------------- #

def get_cmdb_category_schema() -> dict:
    """
    Returns the CmdbCategorySchema

    Returns:
        dict: Schema of the CmdbCategory
    """
    return {
        'public_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string',
            'required': True,
            'regex': r'(\w+)-*(\w)([\w-]*)'  # kebab case validation,
        },
        'label': {
            'type': 'string',
            'required': False
        },
        'parent': {
            'type': 'integer',
            'nullable': True,
            'default': None
        },
        'types': {
            'type': 'list',
            'default': []
        },
        'meta': {
            'type': 'dict',
            'schema': {
                'icon': {
                    'type': 'string',
                    'empty': True
                },
                'order': {
                    'type': 'integer',
                    'nullable': True
                }
            },
            'default': {
                'icon': '',
                'order': None,
            }
        }
    }
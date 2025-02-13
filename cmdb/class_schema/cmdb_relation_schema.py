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
The schema of a CmdbRelation
"""
# -------------------------------------------------------------------------------------------------------------------- #

def get_cmdb_relation_schema() -> dict:
    """
    Returns the CmdbRelationSchema

    Returns:
        dict: Schema of the CmdbRelation
    """
    return {
        'public_id': { # public_id of CmdbRelation
            'type': 'integer'
        },
        'relation_name': {  # Name of the CmdbRelation
            'type': 'string',
            'required': True
        },
        'relation_name_parent': { # Name of parent to child relation
            'type': 'string',
            'required': True
        },
        'relation_icon_parent': { # Icon of the parent to child relation
            'type': 'string',
            'required': False
        },
        'relation_color_parent': { # Color of the parent to child relation
            'type': 'string',
            'required': False
        },
        'relation_name_child': {  # Name of child to parent relation
            'type': 'string',
            'required': True
        },
        'relation_icon_child': { # Icon of the child to parent relation
            'type': 'string',
            'required': False
        },
        'relation_color_child': { # Color of the child to parent relation
            'type': 'string',
            'required': False
        },
        'description': { # General description of the Relation
            'type': 'string',
            'nullable': True,
            'required': False
        },
        'parent_type_ids': { # public_ids of allowed parent CmdbTypes
            'type': 'dict',
            'required': True,
        },
        'child_type_ids': { # public_ids of allowed child CmdbTypes
            'type': 'dict',
            'required': True
        },
        'sections': { # all sections of the CmdbRelation
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    "type": { # Type of the section, currently only "section" available
                        'type': 'string',
                        'required': True
                    },
                    "name": { # Unique identifier of the section
                        'type': 'string',
                        'required': True
                    },
                    "label": { # Label of the section
                        'type': 'string',
                        'required': True
                    },
                    'fields': { # All fields of the section
                        'type': 'list',
                        'empty': True,
                    }
                }
            },
            'empty': True
        },
        'fields': { # All fields for the section
            'type': 'list',
            'required': False,
            'default': None,
            'schema': {
                'type': 'dict',
                'schema': {
                    "type": {
                        'type': 'string',  # Text, Password, Textarea, radio, select, date etc.
                        'required': True
                    },
                    "required": { # If field is required
                        'type': 'boolean',
                        'required': False
                    },
                    "name": { # Unique identifier for the field
                        'type': 'string',
                        'required': True
                    },
                    "rows": { # Number of rows for TextArea Field
                        'type': 'integer',
                        'required': False
                    },
                    "label": { # Label of the field
                        'type': 'string',
                        'required': True
                    },
                    "description": { # Description of the field
                        'type': 'string',
                        'required': False,
                    },
                    "regex": { # Regex of the field
                        'type': 'string',
                        'required': False
                    },
                    "placeholder": { # Placeholder of the field
                        'type': 'string',
                        'required': False,
                    },
                    "value": { # The value for this field
                        'required': False,
                        'nullable': True,
                    },
                    "helperText": { # Helpertext for this field
                        'type': 'string',
                        'required': False,
                    },
                    "options": { # Options for RadioField and SelectField
                        'type': 'list',
                        'empty': True,
                        'required': False,
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                "name": { # Name of the option (not visible to the user)
                                    'type': 'string',
                                    'required': True
                                },
                                "label": { # Value of the option (visible to the user)
                                    'type': 'string',
                                    'required': True
                                },
                            }
                        }
                    }
                }
            },
        }
    }

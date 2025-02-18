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
This module contains the implementation of CmdbReportCategory, which is representing
a category of a report in Datagarry
"""
import logging

from cmdb.models.cmdb_dao import CmdbDAO
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              CmdbReportCategory - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class CmdbReportCategory(CmdbDAO):
    """document"""
    #TODO: DOCUMENT-FIX
    COLLECTION = 'framework.reportCategories'
    MODEL = 'Report_Category'
    DEFAULT_VERSION: str = '1.0.0'
    REQUIRED_INIT_KEYS = ['name', 'predefined']

    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string',
            'required': True,
        },
        'predefined': {
            'type': 'boolean',
            'default': False
        },
    }

# ---------------------------------------------------- CONSTRUCTOR --------------------------------------------------- #

    def __init__(self, name: str, predefined: bool = False, **kwargs):
        """document"""
        #TODO: DOCUMENT-FIX
        self.name = name
        self.predefined = predefined
        super().__init__(**kwargs)

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "CmdbReportCategory":
        """document"""
        #TODO: DOCUMENT-FIX
        return cls(
            public_id = data.get('public_id'),
            name = data.get('name'),
            predefined = data.get('predefined', False),
        )


    @classmethod
    def to_json(cls, instance: "CmdbReportCategory") -> dict:
        """document"""
        #TODO: DOCUMENT-FIX
        return {
            'public_id': instance.get_public_id(),
            'name': instance.name,
            'predefined': instance.predefined,
        }


    @classmethod
    def to_data(cls, instance: "CmdbReportCategory") -> dict:
        """document"""
        #TODO: DOCUMENT-FIX
        return {
            'public_id': instance['public_id'],
            'name': instance['name'],
            'predefined': instance['predefined'],
        }

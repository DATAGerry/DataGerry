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
Implementation of IsmsImpactCategory in DataGerry - ISMS
"""
import logging

from cmdb.models.cmdb_dao import CmdbDAO

from cmdb.errors.models.isms_impact_category import (
    IsmsImpactCategoryInitError,
    IsmsImpactCategoryInitFromDataError,
    IsmsImpactCategoryToJsonError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              IsmsImpactCategory - CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class IsmsImpactCategory(CmdbDAO):
    """
    Implementation of IsmsImpactCategory which represents an impact category

    Extends: CmdbDAO
    """
    COLLECTION = "isms.impactCategory"
    MODEL = 'ImpactCategory'

    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'impact_descriptions': {
            'type': 'list',
             "schema": {
                "type": "dict", 
                    "schema": {
                        "impact_id": {
                            "type": "integer",
                            "min": 1,
                        },
                        "value": {
                            "type": "string",
                        }
                    }
            }
        }
    }


    #pylint: disable=too-many-positional-arguments
    def __init__(self, public_id: int, name: str, impact_descriptions: list):
        """
        Initialises an IsmsImpactCategory

        Args:
            public_id (int): public_id of the IsmsImpactCategory
            name (str): The name of the IsmsImpactCategory
            impact_descriptions (list): The descriptions for each IsmsImpact

        Raises:
            IsmsImpactCategoryInitFromDataError: When the IsmsImpact could not be initialised
        """
        try:
            self.name = name
            self.impact_descriptions = impact_descriptions

            super().__init__(public_id=public_id)
        except Exception as err:
            raise IsmsImpactCategoryInitError(err) from err

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "IsmsImpactCategory":
        """
        Initialises a IsmsImpactCategory from a dict

        Args:
            data (dict): Data with which the IsmsImpactCategory should be initialised

        Raises:
            IsmsImpactCategoryInitFromDataError: If the initialisation with the given data fails

        Returns:
            IsmsImpactCategory: IsmsImpactCategory with the given data
        """
        try:
            return cls(
                public_id = data.get('public_id'),
                name = data.get('name'),
                impact_descriptions = data.get('impact_descriptions'),
            )
        except Exception as err:
            raise IsmsImpactCategoryInitFromDataError(err) from err


    @classmethod
    def to_json(cls, instance: "IsmsImpactCategory") -> dict:
        """
        Converts a IsmsImpactCategory into a json compatible dict

        Args:
            instance (IsmsImpactCategory): The IsmsImpactCategory which should be converted

        Raises:
            IsmsImpactCategoryToJsonError: If the IsmsImpactCategory could not be converted to a json compatible dict

        Returns:
            dict: Json compatible dict of the IsmsImpactCategory values
        """
        try:
            return {
                'public_id': instance.get_public_id(),
                'name': instance.name,
                'impact_descriptions': instance.impact_descriptions,
            }
        except Exception as err:
            raise IsmsImpactCategoryToJsonError(err) from err

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
Implementation of IsmsImpact in DataGerry - ISMS
"""
import logging

from cmdb.models.cmdb_dao import CmdbDAO

from cmdb.errors.models.isms_impact import (
    IsmsImpactInitError,
    IsmsImpactInitFromDataError,
    IsmsImpactToJsonError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  IsmsImpact - CLASS                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class IsmsImpact(CmdbDAO):
    """
    Implementation of IsmsImpact which represents the impact of events

    Extends: CmdbDAO
    """
    COLLECTION = "isms.impact"
    MODEL = 'Impact'
    # pylint: disable=R0801
    SCHEMA: dict = {
        'public_id': {
            'type': 'integer',
            'min': 1,
        },
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'calculation_basis': {
            'type': 'float',
            'min': 0.0,
            'required': True,
            'empty': False
        },
        'description': {
            'type': 'string',
            'required': False
        }
    }


    def __init__(self, public_id: int, name: str, calculation_basis: str, description: str = None):
        """
        Initialises an IsmsImpact

        Args:
            public_id (int): public_id of the IsmsImpact
            name (str): The name of the IsmsImpact
            calculation_basis (float): The calculation_basis of the IsmsImpact
            description (str): The description of the IsmsImpact

        Raises:
            IsmsImpactInitError: If the IsmsImpact could not be initialised
        """
        try:
            self.name = name
            self.calculation_basis = calculation_basis
            self.description = description

            super().__init__(public_id=public_id)
        except Exception as err:
            raise IsmsImpactInitError(err) from err

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "IsmsImpact":
        """
        Initialises a IsmsImpact from a dict

        Args:
            data (dict): Data with which the IsmsImpact should be initialised

        Raises:
            IsmsImpactInitFromDataError: If the initialisation with the given data fails

        Returns:
            IsmsImpact: IsmsImpact with the given data
        """
        try:
            return cls(
                public_id = data.get('public_id'),
                name = data.get('name'),
                calculation_basis = data.get('calculation_basis'),
                description = data.get('description'),
            )
        except Exception as err:
            raise IsmsImpactInitFromDataError(err) from err


    @classmethod
    def to_json(cls, instance: "IsmsImpact") -> dict:
        """
        Converts a IsmsImpact into a json compatible dict

        Args:
            instance (IsmsImpact): The IsmsImpact which should be converted

        Raises:
            IsmsImpactToJsonError: If the IsmsImpact could not be converted to a json compatible dict

        Returns:
            dict: Json compatible dict of the IsmsImpact values
        """
        try:
            return {
                'public_id': instance.get_public_id(),
                'name': instance.name,
                'calculation_basis': instance.calculation_basis,
                'description': instance.description,
            }
        except Exception as err:
            raise IsmsImpactToJsonError(err) from err

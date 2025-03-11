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
Implementation of IsmsLikelihood in DataGerry - ISMS
"""
import logging

from cmdb.models.cmdb_dao import CmdbDAO
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                IsmsLikelihood - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class IsmsLikelihood(CmdbDAO):
    """
    Implementation of IsmsRiskClass which represents a risk class of the ISMS general configuration

    Extends: CmdbDAO
    """
    COLLECTION = "isms.likelihood"
    MODEL = 'Likelihood'

    SCHEMA: dict = {
        'public_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'description': {
            'type': 'string',
            'required': False
        },
        'calculation_basis': {
            'type': 'float',
            'required': True,
            'empty': False
        },
        'sort': {
            'type': 'integer',
            'required': False
        }
    }


    #pylint: disable=too-many-positional-arguments
    def __init__(self, public_id: int, name: str, calculation_basis: str, sort: int = None, descrption: str = None):
        """
        Initialises an IsmsLikelihood

        Args:
            public_id (int): public_id of the IsmsLikelihood
            name (str): The name of the IsmsLikelihood
            calculation_basis (float): The calculation_basis of the IsmsLikelihood
            sort (int): The sort order of the IsmsLikelihood
            descrption (str): The description of the IsmsLikelihood
        """
        self.name = name
        self.calculation_basis = calculation_basis
        self.sort = sort
        self.description = descrption

        super().__init__(public_id=public_id)

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "IsmsLikelihood":
        """
        Initialises a IsmsLikelihood from a dict

        Args:
            data (dict): Data with which the IsmsLikelihood should be initialised

        Returns:
            IsmsLikelihood: IsmsLikelihood with the given data
        """
        return cls(
            public_id = data.get('public_id'),
            name = data.get('name'),
            calculation_basis = data.get('calculation_basis'),
            sort = data.get('sort'),
            description = data.get('description'),
        )


    @classmethod
    def to_json(cls, instance: "IsmsLikelihood") -> dict:
        """
        Converts a IsmsLikelihood into a json compatible dict

        Args:
            instance (IsmsLikelihood): The IsmsLikelihood which should be converted

        Returns:
            dict: Json compatible dict of the IsmsLikelihood values
        """
        return {
            'public_id': instance.get_public_id(),
            'name': instance.name,
            'calculation_basis': instance.calculation_basis,
            'sort': instance.sort,
            'description': instance.description,
        }

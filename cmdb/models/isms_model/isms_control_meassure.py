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
Implementation of IsmsControlMeassure in DataGerry - ISMS
"""
import logging

from cmdb.models.cmdb_dao import CmdbDAO

from cmdb.models.isms_model.control_meassure_type_enum import ControlMeassureType
from cmdb.errors.models.isms_control_meassure import (
    IsmsControlMeassureInitError,
    IsmsControlMeassureInitFromDataError,
    IsmsControlMeassureToJsonError,
)

# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              IsmsControlMeassure - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class IsmsControlMeassure(CmdbDAO):
    """
    Implementation of IsmsControlMeassure which represents a threat in ISMS

    Extends: CmdbDAO
    """
    COLLECTION = "isms.controlMeassure"
    MODEL = 'ControlMeassure'
    # pylint: disable=R0801
    SCHEMA: dict = {
        'public_id': {
            'type': 'integer',
            'min': 1,
        },
        'title': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'control_meassure_type': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'source': {
            'type': 'integer',
        },
        'implementation_state': {
            'type': 'integer',
        },
        'identifier': {
            'type': 'string',
        },
        'chapter': {
            'type': 'string',
        },
        'description': {
            'type': 'string',
        },
        'is_applicable': {
            'type': 'boolean',
        },
        'reason': {
            'type': 'string',
        }
    }

    #pylint: disable=R0913, R0917
    def __init__(
            self,
            public_id: int,
            title: str,
            control_meassure_type: ControlMeassureType,
            source: int,
            implementation_state: int,
            identifier: str = None,
            chapter: str = None,
            description: str = None,
            is_applicable: bool = False,
            reason: str = None,
        ):
        """
        Initialises an IsmsControlMeassure

        Args:
            title (str): The title of the IsmsControlMeassure
            control_meassure_type (ControlMeassureType): A ControlMeassureType of the IsmsControlMeassure
            source: (int): public_id of CmdbExtendableOption('CONTROL_MEASSURE') of the IsmsControlMeassure
            implementation_state: (int): public_id of CmdbExtendableOption('IMPLEMENTATION_STATE')
                                         of the IsmsControlMeassure
            identifier (str, optional): The identifier of the IsmsControlMeassure
            chapter (str, optional): The chapter of the IsmsControlMeassure
            description (str, optional): The description of the IsmsControlMeassure
            is_applicable (bool): = If True then the IsmsControlMeassure is applicable. Defaults to False
            reason (str, optional): The reason of the IsmsControlMeassure
        Raises:
            IsmsControlMeassureInitError: If the IsmsControlMeassure could not be initialised
        """
        try:
            self.title = title
            self.control_meassure_type = control_meassure_type
            self.source = source
            self.implementation_state = implementation_state
            self.identifier = identifier
            self.chapter = chapter
            self.description = description
            self.is_applicable = is_applicable
            self.reason = reason

            super().__init__(public_id = public_id)
        except Exception as err:
            raise IsmsControlMeassureInitError(err) from err

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "IsmsControlMeassure":
        """
        Initialises a IsmsControlMeassure from a dict

        Args:
            data (dict): Data with which the IsmsControlMeassure should be initialised

        Raises:
            IsmsControlMeassureInitFromDataError: If the initialisation with the given data fails

        Returns:
            IsmsControlMeassure: IsmsControlMeassure with the given data
        """
        try:
            return cls(
                public_id = data.get('public_id'),
                title = data.get('title'),
                control_meassure_type = data.get('control_meassure_type'),
                source = data.get('source'),
                implementation_state = data.get('implementation_state'),
                identifier = data.get('identifier'),
                chapter = data.get('chapter'),
                description = data.get('description'),
                is_applicable = data.get('is_applicable'),
                reason = data.get('reason'),
            )
        except Exception as err:
            raise IsmsControlMeassureInitFromDataError(err) from err


    @classmethod
    def to_json(cls, instance: "IsmsControlMeassure") -> dict:
        """
        Converts a IsmsControlMeassure into a json compatible dict

        Args:
            instance (IsmsControlMeassure): The IsmsControlMeassure which should be converted

        Raises:
            IsmsControlMeassureToJsonError: If the IsmsControlMeassure could not be converted to a json compatible dict

        Returns:
            dict: Json compatible dict of the IsmsControlMeassure values
        """
        try:
            return {
                'public_id': instance.get_public_id(),
                'title': instance.title,
                'control_meassure_type': instance.control_meassure_type,
                'source': instance.source,
                'implementation_state': instance.implementation_state,
                'identifier': instance.identifier,
                'chapter': instance.chapter,
                'description': instance.description,
                'is_applicable': instance.is_applicable,
                'reason': instance.reason,
            }
        except Exception as err:
            raise IsmsControlMeassureToJsonError(err) from err

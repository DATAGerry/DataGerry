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
Implementation of IsmsControlMeassureAssignment in DataGerry - ISMS
"""
import logging
from datetime import datetime
from dateutil.parser import parse

from cmdb.models.cmdb_dao import CmdbDAO
from cmdb.models.isms_model.priority_enum import Priority
from cmdb.models.person_group_model.person_reference_type_enum import PersonReferenceType

from cmdb.errors.models.isms_control_meassure_assignment import (
    IsmsControlMeassureAssignmentInitError,
    IsmsControlMeassureAssignmentInitFromDataError,
    IsmsControlMeassureAssignmentToJsonError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                         IsmsControlMeassureAssignment - CLASS                                        #
# -------------------------------------------------------------------------------------------------------------------- #
class IsmsControlMeassureAssignment(CmdbDAO):
    """
    Implementation of IsmsControlMeassureAssignment

    Extends: CmdbDAO
    """
    COLLECTION = "isms.controlMeassureAssignment"
    MODEL = 'ControlMeassureAssignment'

    SCHEMA: dict = {
        'public_id': { # public_id of the IsmsControlMeassureAssignment
            'type': 'integer',
            'min': 1,
        },
        'control_meassure_id': { # public_id of IsmsControlMeassure
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'risk_assessment_id': { # public_id of IsmsRiskAssessment
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'planned_implementation_date': { # Date of planned implementation
            'type': 'dict',
        },
        'implementation_status': { # public_id of CmdbExtendableOption 'IMPLEMENTATION_STATE'
            'type': 'integer',
            'required': True,
            'empty': False
        },
        'finished_implementation_date': { # Date of finished implementation
            'type': 'dict',
        },
        'priority': { # Priority enum (1 = Low, 2 = Medium, 3 = High, 4 = Very high)
            'type': 'integer'
        },
        'responsible_for_implementation_id_ref_type': { # PersonReferenceType Enum
            'type': 'string',
        },
        'responsible_for_implementation_id': { # public_id of CmdbPerson or CmdbPersonGroup
            'type': 'integer',
            'min': 1,
        },
    }


    #pylint: disable=R0913, R0917
    def __init__(
            self,
            public_id: int,
            control_meassure_id: int,
            risk_assessment_id:int,
            planned_implementation_date: datetime,
            implementation_status: int,
            finished_implementation_date: datetime,
            priority: Priority,
            responsible_for_implementation_id_ref_type: PersonReferenceType,
            responsible_for_implementation_id: int):
        """
        Initialises an IsmsControlMeassureAssignment

        Args:
            public_id (int): public_id of the IsmsControlMeassureAssignment
            control_meassure_id (int): public_id of IsmsControlMeassure
            risk_assessment_id (int): public_id of IsmsRiskAssessment
            planned_implementation_date (datetime): # Date of planned implementation
            implementation_status (int): public_id of CmdbExtendableOption 'IMPLEMENTATION_STATE'
            finished_implementation_date (datetime): Date of finished implementation
            priority (Priority): Priority enum (1 = Low, 2 = Medium, 3 = High, 4 = Very high)
            responsible_for_implementation_id_ref_type (PersonReferenceType): # PersonReferenceType Enum
            responsible_for_implementation_id (int): # public_id of CmdbPerson or CmdbPersonGroup

        Raises:
            IsmsControlMeassureAssignmentInitError: When the IsmsControlMeassureAssignment could not be initialised
        """
        try:
            self.control_meassure_id = control_meassure_id
            self.risk_assessment_id = risk_assessment_id
            self.planned_implementation_date = planned_implementation_date
            self.implementation_status = implementation_status
            self.finished_implementation_date = finished_implementation_date
            self.priority = priority
            self.responsible_for_implementation_id_ref_type = responsible_for_implementation_id_ref_type
            self.responsible_for_implementation_id = responsible_for_implementation_id

            super().__init__(public_id=public_id)
        except Exception as err:
            raise IsmsControlMeassureAssignmentInitError(err) from err

# -------------------------------------------------- CLASS FUNCTIONS ------------------------------------------------- #

    @classmethod
    def from_data(cls, data: dict) -> "IsmsControlMeassureAssignment":
        """
        Initialises a IsmsControlMeassureAssignment from a dict

        Args:
            data (dict): Data with which the IsmsControlMeassureAssignment should be initialised

        Raises:
            IsmsControlMeassureAssignmentInitFromDataError: If the initialisation with the given data fails

        Returns:
            IsmsControlMeassureAssignment: IsmsControlMeassureAssignment with the given data
        """
        try:
            planned_implementation_date = data.get('planned_implementation_date', None)
            finished_implementation_date = data.get('finished_implementation_date', None)

            if isinstance(planned_implementation_date, str):
                planned_implementation_date = parse(planned_implementation_date, fuzzy=True)

            if isinstance(finished_implementation_date, str):
                finished_implementation_date = parse(finished_implementation_date, fuzzy=True)

            return cls(
                public_id = data.get('public_id'),
                control_meassure_id = data.get('control_meassure_id'),
                risk_assessment_id = data.get('risk_assessment_id'),
                planned_implementation_date = planned_implementation_date,
                implementation_status = data.get('implementation_status'),
                finished_implementation_date = finished_implementation_date,
                priority = data.get('priority'),
                responsible_for_implementation_id_ref_type = data.get('responsible_for_implementation_id_ref_type'),
                responsible_for_implementation_id = data.get('responsible_for_implementation_id'),
            )
        except Exception as err:
            raise IsmsControlMeassureAssignmentInitFromDataError(err) from err


    @classmethod
    def to_json(cls, instance: "IsmsControlMeassureAssignment") -> dict:
        """
        Converts a IsmsControlMeassureAssignment into a json compatible dict

        Args:
            instance (IsmsControlMeassureAssignment): The IsmsControlMeassureAssignment which should be converted

        Raises:
            IsmsControlMeassureAssignmentToJsonError: If the IsmsControlMeassureAssignment could not be converted
                                                      to a json compatible dict

        Returns:
            dict: Json compatible dict of the IsmsControlMeassureAssignment values
        """
        try:
            return {
                'public_id': instance.get_public_id(),
                'control_meassure_id': instance.control_meassure_id,
                'risk_assessment_id': instance.risk_assessment_id,
                'planned_implementation_date': instance.planned_implementation_date,
                'implementation_status': instance.implementation_status,
                'finished_implementation_date': instance.finished_implementation_date,
                'priority': instance.priority,
                'responsible_for_implementation_id_ref_type': instance.responsible_for_implementation_id_ref_type,
                'responsible_for_implementation_id': instance.responsible_for_implementation_id,
            }
        except Exception as err:
            raise IsmsControlMeassureAssignmentToJsonError(err) from err

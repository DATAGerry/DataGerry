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
This module contains the classes of all ControlMeassureAssignmentManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class ControlMeassureAssignmentManagerError(Exception):
    """
    Raised to catch all ControlMeassureAssignmentManager related errors
    """
    def __init__(self, err: str):
        """
        Raised to catch all ControlMeassureAssignmentManager related errors
        """
        super().__init__(err)

# ------------------------------------------ ControlMeassureAssignmentManager - ERRORS ------------------------------------------ #

class ControlMeassureAssignmentManagerInitError(ControlMeassureAssignmentManagerError):
    """
    Raised when ControlMeassureAssignmentManager could not be initialised
    """


class ControlMeassureAssignmentManagerInsertError(ControlMeassureAssignmentManagerError):
    """
    Raised when ControlMeassureAssignmentManager could not insert an IsmsControlMeassureAssignment
    """


class ControlMeassureAssignmentManagerGetError(ControlMeassureAssignmentManagerError):
    """
    Raised when ControlMeassureAssignmentManager could not retrieve an IsmsControlMeassureAssignment
    """


class ControlMeassureAssignmentManagerUpdateError(ControlMeassureAssignmentManagerError):
    """
    Raised when ControlMeassureAssignmentManager could not update an IsmsControlMeassureAssignment
    """


class ControlMeassureAssignmentManagerDeleteError(ControlMeassureAssignmentManagerError):
    """
    Raised when ControlMeassureAssignmentManager could not delete an IsmsControlMeassureAssignment
    """


class ControlMeassureAssignmentManagerIterationError(ControlMeassureAssignmentManagerError):
    """
    Raised when ControlMeassureAssignmentManager could not iterate over IsmsControlMeassureAssignments
    """

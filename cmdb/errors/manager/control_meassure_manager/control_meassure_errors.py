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
This module contains the classes of all ControlMeassureManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class ControlMeassureManagerError(Exception):
    """
    Raised to catch all ControlMeassureManager related errors
    """
    def __init__(self, err: str):
        """
        Raised to catch all ControlMeassureManager related errors
        """
        super().__init__(err)

# ------------------------------------------ ControlMeassureManager - ERRORS ----------------------------------------- #

class ControlMeassureManagerInitError(ControlMeassureManagerError):
    """
    Raised when ControlMeassureManager could not be initialised
    """


class ControlMeassureManagerInsertError(ControlMeassureManagerError):
    """
    Raised when ControlMeassureManager could not insert an IsmsControlMeassure
    """


class ControlMeassureManagerGetError(ControlMeassureManagerError):
    """
    Raised when ControlMeassureManager could not retrieve an IsmsControlMeassure
    """


class ControlMeassureManagerUpdateError(ControlMeassureManagerError):
    """
    Raised when ControlMeassureManager could not update an IsmsControlMeassure
    """


class ControlMeassureManagerDeleteError(ControlMeassureManagerError):
    """
    Raised when ControlMeassureManager could not delete an IsmsControlMeassure
    """


class ControlMeassureManagerIterationError(ControlMeassureManagerError):
    """
    Raised when ControlMeassureManager could not iterate over IsmsControlMeassures
    """

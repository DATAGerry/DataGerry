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
This module contains the classes of all GroupsManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class GroupsManagerError(Exception):
    """
    Raised to catch all GroupsManager related errors
    """
    def __init__(self, message: str):
        """
        Raised to catch all GroupsManager related errors
        """
        super().__init__(message)

# ------------------------------------------- DocapiTemplatesManager errors ------------------------------------------ #

class GroupsManagerInsertError(GroupsManagerError):
    """
    Raised when GroupsManager could not insert a CmdbUserGroup
    """
    def __init__(self, err: str):
        """
        Raised when GroupsManager could not insert a CmdbUserGroup
        """
        super().__init__(f"GroupsManagerInsertError: {err}")


class GroupsManagerGetError(GroupsManagerError):
    """
    Raised when GroupsManager could not retrieve a CmdbUserGroup
    """
    def __init__(self, err: str):
        """
        Raised when GroupsManager could not retrieve a CmdbUserGroup
        """
        super().__init__(f"GroupsManagerGetError: {err}")


class GroupsManagerIterationError(GroupsManagerError):
    """
    Raised when GroupsManager could not iterate over CmdbUserGroups
    """
    def __init__(self, err: str):
        """
        Raised when GroupsManager could not iterate over CmdbUserGroups
        """
        super().__init__(f"GroupsManagerIterationError: {err}")


class GroupsManagerUpdateError(GroupsManagerError):
    """
    Raised when GroupsManager could not update a CmdbUserGroup
    """
    def __init__(self, err: str):
        """
        Raised when GroupsManager could not update a CmdbUserGroup
        """
        super().__init__(f"GroupsManagerUpdateError: {err}")


class GroupsManagerDeleteError(GroupsManagerError):
    """
    Raised when GroupsManager could not delete a CmdbUserGroup
    """
    def __init__(self, err: str):
        """
        Raised when GroupsManager could not delete a CmdbUserGroup
        """
        super().__init__(f"GroupsManagerDeleteError: {err}")

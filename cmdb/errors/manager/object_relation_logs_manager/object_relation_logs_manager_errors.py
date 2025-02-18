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
This module contains the classes of all ObjectRelationLogsManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectRelationLogsManagerError(Exception):
    """
    Raised to catch all ObjectRelationLogsManager related errors
    """
    def __init__(self, message: str):
        """
        Raised to catch all ObjectRelationLogsManager related errors
        """
        super().__init__(message)

# ---------------------------------------- ObjectRelationsManagerError errors ---------------------------------------- #

class ObjectRelationLogsManagerInsertError(ObjectRelationLogsManagerError):
    """
    Raised when ObjectRelationLogsManager could not insert a CmdbObjectRelationLog
    """
    def __init__(self, err: str):
        """
        Raised when ObjectRelationLogsManager could not insert a CmdbObjectRelationLog
        """
        super().__init__(f"ObjectRelationLogsManagerInsertError: {err}")


class ObjectRelationLogsManagerGetError(ObjectRelationLogsManagerError):
    """
    Raised when ObjectRelationLogsManager could not retrieve a CmdbObjectRelationLog
    """
    def __init__(self, err: str):
        """
        Raised when ObjectRelationLogsManager could not retrieve a CmdbObjectRelationLog
        """
        super().__init__(f"ObjectRelationLogsManagerGetError: {err}")


class ObjectRelationLogsManagerDeleteError(ObjectRelationLogsManagerError):
    """
    Raised when ObjectRelationLogsManager could not delete a CmdbObjectRelationLog
    """
    def __init__(self, err: str):
        """
        Raised when ObjectRelationLogsManager could not delete a CmdbObjectRelationLog
        """
        super().__init__(f"ObjectRelationLogsManagerDeleteError: {err}")


class ObjectRelationLogsManagerIterationError(ObjectRelationLogsManagerError):
    """
    Raised when ObjectRelationLogsManager could not iterate over CmdbObjectRelationLog
    """
    def __init__(self, err: str):
        """
        Raised when ObjectRelationLogsManager could not iterate over CmdbObjectRelationLog
        """
        super().__init__(f"ObjectRelationLogsManagerIterationError: {err}")

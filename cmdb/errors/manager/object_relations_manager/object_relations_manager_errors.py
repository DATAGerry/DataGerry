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
This module contains the classes of all ObjectRelationsManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectRelationsManagerError(Exception):
    """
    Raised to catch all ObjectRelationsManager related errors
    """
    def __init__(self, message: str):
        """
        Raised to catch all ObjectRelationsManager related errors
        """
        super().__init__(message)

# ---------------------------------------- ObjectRelationsManagerError errors ---------------------------------------- #

class ObjectRelationsManagerInsertError(ObjectRelationsManagerError):
    """
    Raised when ObjectRelationsManager could not insert a CmdbObjectRelation
    """
    def __init__(self, err: str):
        """
        Raised when ObjectRelationsManager could not insert a CmdbObjectRelation
        """
        super().__init__(f"ObjectRelationsManagerInsertError: {err}")


class ObjectRelationsManagerGetError(ObjectRelationsManagerError):
    """
    Raised when ObjectRelationsManager could not retrieve a CmdbObjectRelation
    """
    def __init__(self, err: str):
        """
        Raised when ObjectRelationsManager could not retrieve a CmdbObjectRelation
        """
        super().__init__(f"ObjectRelationsManagerGetError: {err}")


class ObjectRelationsManagerUpdateError(ObjectRelationsManagerError):
    """
    Raised when ObjectRelationsManager could not update a CmdbObjectRelation
    """
    def __init__(self, err: str):
        """
        Raised when ObjectRelationsManager could not update a CmdbObjectRelation
        """
        super().__init__(f"ObjectRelationsManagerUpdateError: {err}")


class ObjectRelationsManagerDeleteError(ObjectRelationsManagerError):
    """
    Raised when ObjectRelationsManager could not delete a CmdbObjectRelation
    """
    def __init__(self, err: str):
        """
        Raised when ObjectRelationsManager could not delete a CmdbObjectRelation
        """
        super().__init__(f"ObjectRelationsManagerDeleteError: {err}")


class ObjectRelationsManagerIterationError(ObjectRelationsManagerError):
    """
    Raised when ObjectRelationsManager could not iterate over CmdbObjectRelations
    """
    def __init__(self, err: str):
        """
        Raised when ObjectRelationsManager could not iterate over CmdbObjectRelations
        """
        super().__init__(f"ObjectRelationsManagerIterationError: {err}")

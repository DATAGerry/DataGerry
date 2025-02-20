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
Contains general BaseManager Error Classes
"""
# -------------------------------------------------------------------------------------------------------------------- #

class BaseManagerError(Exception):
    """
    Raised to catch all BaseManager related errors
    """
    def __init__(self, err: str):
        """
        Raised to catch all BaseManager related errors
        """
        super().__init__(err)

# -------------------------------------------------- MANAGER ERRORS -------------------------------------------------- #

class BaseManagerInitError(BaseManagerError):
    """
    When the BaseManager could not be initialised
    """


class BaseManagerGetError(BaseManagerError):
    """
    When the BaseManager could not retrieve a document
    """


class BaseManagerIterationError(BaseManagerError):
    """
    When the BaseManager iteration fails
    """


class BaseManagerInsertError(BaseManagerError):
    """
    When the BaseManager could not insert a document
    """


class BaseManagerUpdateError(BaseManagerError):
    """
    When the BaseManager could not update a document
    """


class BaseManagerDeleteError(BaseManagerError):
    """
    When the BaseManager could not delete a document
    """

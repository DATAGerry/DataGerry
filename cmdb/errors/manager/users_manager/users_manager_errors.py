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
This module contains the classes of all UsersManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class UsersManagerError(Exception):
    """
    Raised to catch all UsersManager related errors
    """
    def __init__(self, message: str):
        """
        Raised to catch all UsersManager related errors
        """
        super().__init__(message)

# ----------------------------------------------- UsersManager Errors ------------------------------------------------ #

class UsersManagerGetError(UsersManagerError):
    """
    Raised when UsersManager could not retrieve a CmdbUser
    """
    def __init__(self, err: str):
        """
        Raised when UsersManager could not retrieve a CmdbUser
        """
        super().__init__(f"UsersManagerGetError: {err}")


class UsersManagerInsertError(UsersManagerError):
    """
    Raised when UsersManager could not create a CmdbUser
    """
    def __init__(self, err: str):
        """
        Raised when UsersManager could not create a CmdbUser
        """
        super().__init__(f"UsersManagerInsertError: {err}")


#TODO: ERROR-FIX (not used)
class UsersManagerUpdateError(UsersManagerError):
    """
    Raised when UsersManager could not update a CmdbUser
    """
    def __init__(self, err: str):
        """
        Raised when UsersManager could not update a CmdbUser
        """
        super().__init__(f"UsersManagerUpdateError: {err}")


class UsersManagerDeleteError(UsersManagerError):
    """
    Raised when UsersManager could not delete a CmdbUser
    """
    def __init__(self, err: str):
        """
        Raised when UsersManager could not delete a CmdbUser
        """
        super().__init__(f"UsersManagerDeleteError: {err}")


class UsersManagerIterationError(UsersManagerError):
    """
    Raised when UsersManager could not iterate CmdbUsers
    """
    def __init__(self, err: str):
        """
        Raised when UsersManager could not iterate CmdbUsers
        """
        super().__init__(f"UsersManagerIterationError: {err}")

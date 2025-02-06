# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
This module contains the classes of all ObjectLinksManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectLinksManagerError(Exception):
    """
    Base ObjectLinksManager error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# --------------------------------------------- ObjectLinksManager errors -------------------------------------------- #

class ObjectLinksManagerInsertError(ObjectLinksManagerError):
    """
    Raised when ObjectLinksManager could not insert a CmdbObjectLink
    """
    def __init__(self, err: str):
        self.message = f"ObjectLinksManagerInsertError: {err}"
        super().__init__(self.message)


class ObjectLinksManagerGetError(ObjectLinksManagerError):
    """
    Raised when ObjectLinksManager could not retrieve a CmdbObjectLink
    """
    def __init__(self, err: str):
        self.message = f"ObjectLinksManagerGetError: {err}"
        super().__init__(self.message)


class ObjectLinksManagerGetObjectError(ObjectLinksManagerError):
    """
    Raised when ObjectLinksManager could not retrieve an CmdbObject
    """
    def __init__(self, err: str):
        self.message = f"ObjectLinksManagerGetObjectError: {err}"
        super().__init__(self.message)


class ObjectLinksManagerIterationError(ObjectLinksManagerError):
    """
    Raised when ObjectLinksManager could not iterate over CmdbObjectLinks
    """
    def __init__(self, err: str):
        self.message = f"ObjectLinksManagerIterationError: {err}"
        super().__init__(self.message)


class ObjectLinksManagerDeleteError(ObjectLinksManagerError):
    """
    Raised when ObjectLinksManager could not delete a CmdbObjectLink
    """
    def __init__(self, err: str):
        self.message = f"ObjectLinksManagerDeleteError: {err}"
        super().__init__(self.message)

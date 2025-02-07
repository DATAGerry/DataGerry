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
This module contains the classes of all CategoriesManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class CategoriesManagerError(Exception):
    """
    Raised to catch all CategoriesManager related errors
    """
    def __init__(self, message: str):
        """
        Raised to catch all CategoriesManager related errors
        """
        super().__init__(message)

# --------------------------------------------- CategoriesManager errors --------------------------------------------- #

class CategoriesManagerInsertError(CategoriesManagerError):
    """
    Raised when CategoriesManager could not insert a CmdbCategory
    """
    def __init__(self, err: str):
        """
        Raised when CategoriesManager could not insert a CmdbCategory
        """
        super().__init__(f"CategoriesManagerInsertError: {err}")


class CategoriesManagerGetError(CategoriesManagerError):
    """
    Raised when CategoriesManager could not retrieve a CmdbCategory
    """
    def __init__(self, err: str):
        """
        Raised when CategoriesManager could not retrieve a CmdbCategory
        """
        super().__init__(f"CategoriesManagerGetError: {err}")


class CategoriesManagerUpdateError(CategoriesManagerError):
    """
    Raised when CategoriesManager could not update a CmdbCategory
    """
    def __init__(self, err: str):
        """
        Raised when CategoriesManager could not update a CmdbCategory
        """
        super().__init__(f"CategoriesManagerUpdateError: {err}")


class CategoriesManagerDeleteError(CategoriesManagerError):
    """
    Raised when CategoriesManager could not delete a CmdbCategory
    """
    def __init__(self, err: str):
        """
        Raised when CategoriesManager could not delete a CmdbCategory
        """
        super().__init__(err)


class CategoriesManagerIterationError(CategoriesManagerError):
    """
    Raised when CategoriesManager could not iterate over CmdbCategories
    """
    def __init__(self, err: str):
        """
        Raised when CategoriesManager could not iterate over CmdbCategories
        """
        super().__init__(f"CategoriesManagerIterationError: {err}")


class CategoriesManagerTreeInitError(CategoriesManagerError):
    """
    Raised when CategoriesManager could not initialise the CategoryTree
    """
    def __init__(self, err: str):
        """
        Raised when CategoriesManager could not initialise the CategoryTree
        """
        super().__init__(f"CategoriesManagerTreeInitError: {err}")

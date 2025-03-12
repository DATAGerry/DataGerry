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
This module contains the classes of all ImpactCategoryManager errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class ImpactCategoryManagerError(Exception):
    """
    Raised to catch all ImpactCategoryManager related errors
    """
    def __init__(self, err: str):
        """
        Raised to catch all ImpactCategoryManager related errors
        """
        super().__init__(err)

# ------------------------------------------ ImpactCategoryManager - ERRORS ------------------------------------------ #

class ImpactCategoryManagerInitError(ImpactCategoryManagerError):
    """
    Raised when ImpactCategoryManager could not be initialised
    """

class ImpactCategoryManagerInsertError(ImpactCategoryManagerError):
    """
    Raised when ImpactCategoryManager could not insert an IsmsImpactCategory
    """


class ImpactCategoryManagerGetError(ImpactCategoryManagerError):
    """
    Raised when ImpactCategoryManager could not retrieve an IsmsImpactCategory
    """


class ImpactCategoryManagerUpdateError(ImpactCategoryManagerError):
    """
    Raised when ImpactCategoryManager could not update an IsmsImpactCategory
    """


class ImpactCategoryManagerDeleteError(ImpactCategoryManagerError):
    """
    Raised when ImpactCategoryManager could not delete an IsmsImpactCategory
    """


class ImpactCategoryManagerIterationError(ImpactCategoryManagerError):
    """
    Raised when ImpactCategoryManager could not iterate over IsmsImpactCategories
    """

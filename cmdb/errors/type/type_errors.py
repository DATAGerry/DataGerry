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
This module contains all error classes for CmdbTypes
"""
# -------------------------------------------------------------------------------------------------------------------- #

class CmdbTypeError(Exception):
    """
    Raised to catch all CmdbType related errors
    """
    def __init__(self, err: str):
        """
        Raised to catch all CmdbType related errors
        """
        super().__init__(err)

# -------------------------------------------------- CmdbType ERRORS ------------------------------------------------- #
#TODO: REFACTOR-FIX (move to model errors)


class TypeNotFoundError(CmdbTypeError):
    """
    Raised when a CmdbType was not found
    """


class ExternalFillError(CmdbTypeError):
    """
    Raised if href of TypeExternalLink could not filled with input data
    """


class TypeReferenceLineFillError(CmdbTypeError):
    """
    Raised if summary line of TypeReferences could not filled with input data
    """


class FieldNotFoundError(CmdbTypeError):
    """
    Raised if field does not exists
    """


class FieldInitError(CmdbTypeError):
    """
    Error if field could not be initialized
    """

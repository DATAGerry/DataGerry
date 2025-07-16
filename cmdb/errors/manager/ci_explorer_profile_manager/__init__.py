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
This module provides all errors for the CiExplorerProfileManager
"""
from .ci_explorer_profile_manager_errors import (
    CiExplorerProfileManagerError,
    CiExplorerProfileManagerInitError,
    CiExplorerProfileManagerInsertError,
    CiExplorerProfileManagerGetError,
    CiExplorerProfileManagerUpdateError,
    CiExplorerProfileManagerDeleteError,
    CiExplorerProfileManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

__all__ = [
    'CiExplorerProfileManagerError',
    'CiExplorerProfileManagerInitError',
    'CiExplorerProfileManagerInsertError',
    'CiExplorerProfileManagerGetError',
    'CiExplorerProfileManagerUpdateError',
    'CiExplorerProfileManagerDeleteError',
    'CiExplorerProfileManagerIterationError',
]


CI_EXPLORER_PROFILE_MANAGER_ERRORS = {
    "init": CiExplorerProfileManagerInitError,
    "insert": CiExplorerProfileManagerInsertError,
    "get": CiExplorerProfileManagerGetError,
    "update": CiExplorerProfileManagerUpdateError,
    "delete": CiExplorerProfileManagerDeleteError,
    "iterate": CiExplorerProfileManagerIterationError,
}

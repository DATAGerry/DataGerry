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
This module provides all errors for the ThreatManager
"""
from .threat_manager_errors import (
    ThreatManagerError,
    ThreatManagerInitError,
    ThreatManagerInsertError,
    ThreatManagerGetError,
    ThreatManagerUpdateError,
    ThreatManagerDeleteError,
    ThreatManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

__all__ = [
    'ThreatManagerError',
    'ThreatManagerInitError',
    'ThreatManagerInsertError',
    'ThreatManagerGetError',
    'ThreatManagerUpdateError',
    'ThreatManagerDeleteError',
    'ThreatManagerIterationError',
]


THREAT_MANAGER_ERRORS = {
    "init": ThreatManagerInitError,
    "insert": ThreatManagerInsertError,
    "get": ThreatManagerGetError,
    "update": ThreatManagerUpdateError,
    "delete": ThreatManagerDeleteError,
    "iterate": ThreatManagerIterationError,
}

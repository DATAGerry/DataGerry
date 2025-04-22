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
This module provides all errors for the ControlMeasureManager
"""
from .control_measure_errors import (
    ControlMeasureManagerError,
    ControlMeasureManagerInitError,
    ControlMeasureManagerInsertError,
    ControlMeasureManagerGetError,
    ControlMeasureManagerUpdateError,
    ControlMeasureManagerDeleteError,
    ControlMeasureManagerIterationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

__all__ = [
    'ControlMeasureManagerError',
    'ControlMeasureManagerInitError',
    'ControlMeasureManagerInsertError',
    'ControlMeasureManagerGetError',
    'ControlMeasureManagerUpdateError',
    'ControlMeasureManagerDeleteError',
    'ControlMeasureManagerIterationError',
]


CONTROL_MEASURE_MANAGER_ERRORS = {
    "init": ControlMeasureManagerInitError,
    "insert": ControlMeasureManagerInsertError,
    "get": ControlMeasureManagerGetError,
    "update": ControlMeasureManagerUpdateError,
    "delete": ControlMeasureManagerDeleteError,
    "iterate": ControlMeasureManagerIterationError,
}

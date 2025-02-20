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
This module contains the classes of all system config file errors
"""
# -------------------------------------------------------------------------------------------------------------------- #

class ConfigFileError(Exception):
    """
    Raised to catch all system config file related errors
    """
    def __init__(self, err: str):
        """
        Raised to catch all system config file related errors
        """
        super().__init__(err)

# ------------------------------------------------ CONFIG FILE ERRORS ------------------------------------------------ #
#TODO: REFACTOR-FIX (better naming convention for all error classes)


class ConfigFileSetError(ConfigFileError):
    """
    Raises if values of loaded config file are tryed to get edited
    """


class ConfigFileNotFound(ConfigFileError):
    """
    Error if local config file could not be loaded
    """


class ConfigNotLoaded(ConfigFileError):
    """
    Error if config file was not loaded correctly is not loaded
    """


class SectionError(ConfigFileError):
    """
    Error if section does not exist
    """


class KeySectionError(ConfigFileError):
    """
    Error if key does not exist in section
    """

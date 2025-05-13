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
Implementation of CmdbProcess
"""
import logging
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  CmdbProcess - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class CmdbProcess:
    """
    Implementation of CmdbProcess
    """

    def __init__(self, name: str, classname: str):
        """
        Create a new instance of CmdbProcess

        Args:
            name(str): name of the process
            classname(str): classname of the process
        """
        self.__name = name
        self.__classname = classname


    def get_name(self):
        """
        Return the process name

        Returns:
            str: name of the process
        """
        return self.__name


    def get_class(self):
        """
        Return the class name

        Returns:
            str: name of the class
        """
        return self.__classname

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
Implementation of APIPager
"""
import logging
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   APIPager - CLASS                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
class APIPager:
    """
    A utility class for paginating API responses.
    
    This class provides metadata about the pagination state, including the current page,
    page size, and total number of pages.
    """

    def __init__(self, page: int, page_size: int, total_pages: int = None):
        """
        Initialises the APIPager

        Args:
            page (int): The current page number
            page_size (int): The number of items per page
            total_pages (int, optional): The total number of pages. Defaults to None
        """
        self.page = page
        self.page_size = page_size
        self.total_pages = total_pages


    def to_dict(self) -> dict:
        """
        Converts the APIPager properties to a dictionary

        Returns:
            dict: A dictionary containing APIPager properties
        """
        return {
            'page': self.page,
            'page_size': self.page_size,
            'total_pages': self.total_pages,
        }

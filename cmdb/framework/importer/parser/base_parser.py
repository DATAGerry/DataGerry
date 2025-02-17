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
"""document"""
#TODO: DOCUMENT-FIX
import logging

from cmdb.framework.importer.responses.base_parser_response import BaseParserResponse
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  BaseParser - CLASS                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class BaseParser:
    """document"""
    #TODO: DOCUMENT-FIX
    DEFAULT_CONFIG = {}

    def __new__(cls, *args, **kwargs):
        return super(BaseParser, cls).__new__(cls)


    def __init__(self, parser_config: dict = None):
        _parser_config = parser_config or self.DEFAULT_CONFIG
        self.parser_config: dict = {**self.DEFAULT_CONFIG, **_parser_config}


    def get_config(self) -> dict:
        """document"""
        #TODO: DOCUMENT-FIX
        return self.parser_config


    def parse(self, file) -> BaseParserResponse:
        """document"""
        #TODO: DOCUMENT-FIX
        raise NotImplementedError

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
Implementation of JSONContent
"""
from cmdb.framework.importer.content_types.base_content import BaseContent
# -------------------------------------------------------------------------------------------------------------------- #

class JSONContent(BaseContent):
    """
    Identifier for JavaScript Object Notation files
    """
    ICON = 'fas fa-file-code'
    CONTENT_TYPE = 'application/json'
    FILE_TYPE = 'json'

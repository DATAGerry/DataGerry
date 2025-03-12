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
Implementation of GroupDeleteMode
"""
from enum import Enum
# -------------------------------------------------------------------------------------------------------------------- #

class GroupDeleteMode(Enum):
    """
    Represents the deletion mode for a group

    Attributes:
        NONE: No deletion action is performed
        MOVE: The group's content is moved before deletion
        DELETE: The group is permanently deleted
    """
    NONE = None
    MOVE = 'MOVE'
    DELETE = 'DELETE'

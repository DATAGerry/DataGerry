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
Implementation of CmdbObjectRelationLog
"""
import logging
from datetime import datetime, timezone

from cmdb.models.cmdb_dao import CmdbDAO
from cmdb.models.log_model import LogInteraction
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                             CmdbObjectRelationLog - CLASS                                            #
# -------------------------------------------------------------------------------------------------------------------- #
class CmdbObjectRelationLog(CmdbDAO):
    """
    Implementation of CmdbObjectRelationLog
    """
    COLLECTION = 'framework.objectRelationLogs'
    MODEL = 'CmdbObjectRelationLog'

    INDEX_KEYS = [{
        'keys': [('object_relation_id', CmdbDAO.DAO_ASCENDING)],
        'name': 'object_relation_id',
        'unique': True
    }]

    def __init__(self,
                 public_id: int,
                 object_relation_id: int,
                 object_relation_parent_id: int,
                 object_relation_child_id: int,
                 creation_time: datetime,
                 action: LogInteraction,
                 author_id: int,
                 author_name: str,
                 changes: dict = None):
        """
        Creates an instance of CmdbObjectRelationLog

        Args:
            public_id (int): public_id of the CmdbObjectRelationLog
            object_relation_id (int): public_id of the CmdbObjectRelation
            object_relation_parent_id (int): public_id of the parent CmdbObject of the CmdbObjectRelation
            object_relation_child_id (int): public_id of the child CmdbObject of the CmdbObjectRelation
            creation_time (datetime): When the CmdbObjectRelationLog was created
            action: (LogInteraction): CREATE, EDIT or DELETE
            author_id (int): public_id of the CmdbUser who have done the change to the CmdbObjectRelation
            author_name (str, optional): Name of the CmdbbUser if any.
            changes (dict, optional): Changes to the CmdbObjectRelation. Defaults to None (When deleted).
        """
        self.object_relation_id = object_relation_id
        self.object_relation_parent_id = object_relation_parent_id
        self.object_relation_child_id = object_relation_child_id
        self.creation_time = creation_time or datetime.now(timezone.utc)
        self.action = action
        self.author_id = author_id
        self.author_name = author_name
        self.changes = changes

        super().__init__(public_id=public_id)

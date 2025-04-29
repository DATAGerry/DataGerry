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
This module contains the implementation of the ObjectGroupsManager
"""
import logging

from cmdb.database import MongoDatabaseManager

from cmdb.manager.generic_manager import GenericManager

from cmdb.models.object_group_model import CmdbObjectGroup, ObjectReferenceType
from cmdb.models.isms_model import IsmsRiskAssessment, IsmsControlMeasureAssignment

from cmdb.errors.manager.object_groups_manager import OBJECT_GROUPS_MANAGER_ERRORS
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                              ObjectGroupsManager- CLASS                                              #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectGroupsManager(GenericManager):
    """
    The ObjectGroupsManager manages the interaction between CmdbObjectGroups and the database

    Extends: GenericManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        super().__init__(dbm, CmdbObjectGroup, OBJECT_GROUPS_MANAGER_ERRORS, database)

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_with_follow_up(self, public_id: int) -> bool:
        """
        Deletes a CmdbObjectGroup and cleans all affected collections from it

        Args:
            public_id (int): public_id of CmdbObjectGroup which should be deleted

        Returns:
            bool: True if deletion was a success, else False
        """
        self.delete_object_group_from_risk_assessment_cascade(public_id)

        return self.delete_item(public_id)


    def delete_object_group_from_risk_assessment_cascade(self, deleted_group_id: int) -> None:
        """
        Deletes all RiskAssessments and their associated ControlMeasureAssignments that reference 
        the given CmdbObjectGroup.

        This function performs the following steps:
        1. Finds all RiskAssessments where 'object_id_ref_type' is 'OBJECT_GROUP' and 
        'object_id' matches the deleted group ID
        2. Deletes these RiskAssessments
        3. Deletes all ControlMeasureAssignments referencing the deleted RiskAssessments

        Args:
            deleted_group_id (int): The public_id of the deleted CmdbObjectGroup
        """
        # Find all RiskAssessments referencing this ObjectGroup
        risk_assessment_query = {
            'object_id_ref_type': ObjectReferenceType.OBJECT_GROUP,
            'object_id': deleted_group_id
        }

        matching_risk_assessments = list(self.dbm.find(
            IsmsRiskAssessment.COLLECTION,
            risk_assessment_query,
            projection={'public_id': 1}
        ))

        if not matching_risk_assessments:
            return  # Nothing to delete

        # Collect all RiskAssessment public_ids
        risk_assessment_ids = [ra['public_id'] for ra in matching_risk_assessments]

        if risk_assessment_ids:
            # Delete the RiskAssessments
            self.dbm.delete_many(
                IsmsRiskAssessment.COLLECTION,
                {'public_id': {'$in': risk_assessment_ids}},
                plain=True
            )

            # Delete all ControlMeasureAssignments referencing those RiskAssessments
            self.dbm.delete_many(
                IsmsControlMeasureAssignment.COLLECTION,
                {'risk_assessment_id': {'$in': risk_assessment_ids}},
                plain=True
            )

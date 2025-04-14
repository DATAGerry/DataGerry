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
Implementation of all DataGerry rights
"""
from cmdb.models.right_model.levels_enum import Levels
from cmdb.models.right_model.import_rights import ImportRight, ImportObjectRight, ImportTypeRight
from cmdb.models.right_model.base_right import BaseRight
from cmdb.models.right_model.system_rights import SystemRight
from cmdb.models.right_model.constants import GLOBAL_RIGHT_IDENTIFIER
from cmdb.models.right_model.user_management_rights import (
    UserManagementRight,
    UserRight,
    GroupRight,
    PersonRight,
    PersonGroupRight,
)
from cmdb.models.right_model.framework_rights import (
    FrameworkRight,
    ObjectRight,
    TypeRight,
    CategoryRight,
    LogRight,
    SectionTemplateRight,
    WebhookRight,
    RelationRight,
    ObjectRelationRight,
    ObjectRelationLogRight,
    ExtendableOptionRight,
    ObjectGroupRight,
)
from cmdb.models.right_model.isms_rights import (
    IsmsRight,
    RiskClassRight,
    LikelihoodRight,
    ImpactRight,
    ImpactCategoryRight,
    ProtectionGoalRight,
    RiskMatrixRight,
    ThreatRight,
    VulnerabilityRight,
    RiskRight,
    ControlMeassureRight,
    RiskAssessmentRight,
    ControlMeassureAssignment,
)
from cmdb.models.right_model.export_rights import ExportRight, ExportObjectRight, ExportTypeRight
from cmdb.models.right_model.docapi_rights import DocapiRight, DocapiTemplateRight
# -------------------------------------------------------------------------------------------------------------------- #

SYSTEM_RIGHTS = (
    SystemRight(GLOBAL_RIGHT_IDENTIFIER, description='System and settings'),
    (
        SystemRight('view', description='View system configurations and settings'),
        SystemRight('edit', description='Edit system configurations and settings'),
        SystemRight('reload', description='Reload system configurations')
    )
)


FRAMEWORK_RIGHTS = (
    FrameworkRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage the core framework'),
    (
        ObjectRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage objects from framework'),
        (
            ObjectRight('view', description='View objects'),
            ObjectRight('add', description='Add objects'),
            ObjectRight('edit', Levels.PROTECTED, description='Edit objects'),
            ObjectRight('delete', Levels.SECURE, description='Delete objects'),
            ObjectRight('activation', Levels.SECURE, description='Activate/Deactivate objects')
        )
    ),
    (
        TypeRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage types from framework'),
        (
            TypeRight('view', Levels.PROTECTED, description='View types'),
            TypeRight('add', Levels.PROTECTED, description='Add types'),
            TypeRight('edit', Levels.SECURE, description='Edit types'),
            TypeRight('delete', Levels.SECURE, description='Delete types'),
            TypeRight('activation', Levels.SECURE, description='Activate/Deactivate types'),
            TypeRight('clean', Levels.SECURE, description='Clean type fields')
        )
    ),
    (
        CategoryRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage categories from framework'),
        (
            CategoryRight('view', description='View category'),
            CategoryRight('add', description='Add category'),
            CategoryRight('edit', Levels.PROTECTED, description='Edit category'),
            CategoryRight('delete', Levels.SECURE, description='Delete category')
        )
    ),
    (
        SectionTemplateRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage section templates from framework'),
        (
            SectionTemplateRight('view', description='View section templates'),
            SectionTemplateRight('add', description='Add section templates'),
            SectionTemplateRight('edit', Levels.PROTECTED, description='Edit section templates'),
            SectionTemplateRight('delete', Levels.SECURE, description='Delete section templates'),
        )
    ),
    (
        WebhookRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage webhooks'),
        (
            WebhookRight('view', description='View webhooks'),
            WebhookRight('add', description='Add webhooks'),
            WebhookRight('edit', Levels.PROTECTED, description='Edit webhooks'),
            WebhookRight('delete', Levels.DANGER, description='Delete webhooks'),
        )
    ),
    (
        LogRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage framework logs'),
        (
            LogRight('view', description='View logs'),
            LogRight('reload', Levels.SECURE, description='Reload logs'),
            LogRight('delete', Levels.DANGER, description='Delete logs')
        )
    ),
    (
        RelationRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage relations'),
        (
            RelationRight('view', description='View relations'),
            RelationRight('add', description='Add relations'),
            RelationRight('edit', Levels.PROTECTED, description='Edit relations'),
            RelationRight('delete', Levels.DANGER, description='Delete relations'),
        )
    ),
    (
        ObjectRelationRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage object relations'),
        (
            ObjectRelationRight('view', description='View object relations'),
            ObjectRelationRight('add', description='Add object relations'),
            ObjectRelationRight('edit', Levels.PROTECTED, description='Edit object relations'),
            ObjectRelationRight('delete', Levels.DANGER, description='Delete object relations'),
        )
    ),
    (
        ObjectRelationLogRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage object relation logs'),
        (
            ObjectRelationLogRight('view', description='View object relation logs'),
            ObjectRelationLogRight('delete', Levels.DANGER, description='Delete object relation logs'),
        )
    ),
        ExtendableOptionRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage extendable options'),
        (
            ExtendableOptionRight('view', description='View extendable options'),
            ExtendableOptionRight('add', description='Add extendable options'),
            ExtendableOptionRight('edit', Levels.PROTECTED, description='Edit extendable options'),
            ExtendableOptionRight('delete', Levels.SECURE, description='Delete extendable options'),
        ),
        ObjectGroupRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage ObjectGroups'),
        (
            ObjectGroupRight('view', description='View ObjectGroups'),
            ObjectGroupRight('add', description='Add ObjectGroups'),
            ObjectGroupRight('edit', Levels.PROTECTED, description='Edit ObjectGroups'),
            ObjectGroupRight('delete', Levels.SECURE, description='Delete ObjectGroups'),
        ),
)


ISMS_RIGHTS = (
    IsmsRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage ISMS rights'),
    (
        RiskClassRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage RiskClasses of ISMS'),
        (
            RiskClassRight('view', description='View ISMS RiskClasses'),
            RiskClassRight('add', description='Add ISMS RiskClasses'),
            RiskClassRight('edit', Levels.PROTECTED, description='Edit ISMS RiskClasses'),
            RiskClassRight('delete', Levels.SECURE, description='Delete ISMS RiskClasses'),
        ),
        LikelihoodRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage Likelihoods of ISMS'),
        (
            LikelihoodRight('view', description='View ISMS Likelihoods'),
            LikelihoodRight('add', description='Add ISMS Likelihoods'),
            LikelihoodRight('edit', Levels.PROTECTED, description='Edit ISMS Likelihoods'),
            LikelihoodRight('delete', Levels.SECURE, description='Delete ISMS Likelihoods'),
        ),
        ImpactRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage Impacts of ISMS'),
        (
            ImpactRight('view', description='View ISMS Impacts'),
            ImpactRight('add', description='Add ISMS Impacts'),
            ImpactRight('edit', Levels.PROTECTED, description='Edit ISMS Impacts'),
            ImpactRight('delete', Levels.SECURE, description='Delete ISMS Impacts'),
        ),
        ImpactCategoryRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage ImpactCategories of ISMS'),
        (
            ImpactCategoryRight('view', description='View ISMS ImpactCategories'),
            ImpactCategoryRight('add', description='Add ISMS ImpactCategories'),
            ImpactCategoryRight('edit', Levels.PROTECTED, description='Edit ISMS ImpactCategories'),
            ImpactCategoryRight('delete', Levels.SECURE, description='Delete ISMS ImpactCategories'),
        ),
        ProtectionGoalRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage ProtectionGoals of ISMS'),
        (
            ProtectionGoalRight('view', description='View ISMS ProtectionGoals'),
            ProtectionGoalRight('add', description='Add ISMS ProtectionGoals'),
            ProtectionGoalRight('edit', Levels.PROTECTED, description='Edit ISMS ProtectionGoals'),
            ProtectionGoalRight('delete', Levels.SECURE, description='Delete ISMS ProtectionGoals'),
        ),
        RiskMatrixRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage the RiskMatrix of ISMS'),
        (
            RiskMatrixRight('view', description='View ISMS RiskMatrix'),
            RiskMatrixRight('edit', Levels.PROTECTED, description='Edit ISMS RiskMatrix'),
        ),
        ThreatRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage Threats of ISMS'),
        (
            ThreatRight('view', description='View ISMS Threats'),
            ThreatRight('add', description='Add ISMS Threats'),
            ThreatRight('edit', Levels.PROTECTED, description='Edit ISMS Threats'),
            ThreatRight('delete', Levels.SECURE, description='Delete ISMS Threats'),
        ),
        VulnerabilityRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage Vulnerabilities of ISMS'),
        (
            VulnerabilityRight('view', description='View ISMS Vulnerabilities'),
            VulnerabilityRight('add', description='Add ISMS Vulnerabilities'),
            VulnerabilityRight('edit', Levels.PROTECTED, description='Edit ISMS Vulnerabilities'),
            VulnerabilityRight('delete', Levels.SECURE, description='Delete ISMS Vulnerabilities'),
        ),
        RiskRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage Risks of ISMS'),
        (
            RiskRight('view', description='View ISMS Risks'),
            RiskRight('add', description='Add ISMS Risks'),
            RiskRight('edit', Levels.PROTECTED, description='Edit ISMS Risks'),
            RiskRight('delete', Levels.SECURE, description='Delete ISMS Risks'),
        ),
        ControlMeassureRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage ControlMeassures of ISMS'),
        (
            ControlMeassureRight('view', description='View ISMS ControlMeassures'),
            ControlMeassureRight('add', description='Add ISMS ControlMeassures'),
            ControlMeassureRight('edit', Levels.PROTECTED, description='Edit ISMS ControlMeassures'),
            ControlMeassureRight('delete', Levels.SECURE, description='Delete ISMS ControlMeassures'),
        ),
        RiskAssessmentRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage RiskAssessments of ISMS'),
        (
            RiskAssessmentRight('view', description='View ISMS RiskAssessments'),
            RiskAssessmentRight('add', description='Add ISMS RiskAssessments'),
            RiskAssessmentRight('edit', Levels.PROTECTED, description='Edit ISMS RiskAssessments'),
            RiskAssessmentRight('delete', Levels.SECURE, description='Delete ISMS RiskAssessments'),
        ),
        ControlMeassureAssignment(GLOBAL_RIGHT_IDENTIFIER, description='Manage ControlMeassure Assignments of ISMS'),
        (
            ControlMeassureAssignment('view', description='View ISMS ControlMeassure Assignments'),
            ControlMeassureAssignment('add', description='Add ISMS ControlMeassure Assignments'),
            ControlMeassureAssignment('edit', Levels.PROTECTED, description='Edit ISMS ControlMeassure Assignments'),
            ControlMeassureAssignment('delete', Levels.SECURE, description='Delete ISMS ControlMeassure Assignments'),
        ),
    ),
)


EXPORT_RIGHTS = (
    ExportRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage exports'),
    (
        ExportObjectRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage object exports')
    ),
    (
        ExportTypeRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage type exports')
    )
)


IMPORT_RIGHTS = (
    ImportRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage imports'),
    (
        ImportObjectRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage object imports')
    ),
    (
        ImportTypeRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage type imports')
    )
)


USER_MANAGEMENT_RIGHTS = (
    UserManagementRight(GLOBAL_RIGHT_IDENTIFIER, description='CmdbUser management'),
    (
        UserRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage users'),
        (
            UserRight('view', description='View users'),
            UserRight('add', description='Add users'),
            UserRight('edit', Levels.SECURE, description='Edit users'),
            UserRight('delete', Levels.SECURE, description='Delete users')
        ),
        GroupRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage groups'),
        (
            GroupRight('view', description='View groups'),
            GroupRight('add', Levels.DANGER, description='Add groups'),
            GroupRight('edit', Levels.DANGER, description='Edit groups'),
            GroupRight('delete', Levels.SECURE, description='Delete groups')
        ),
        PersonRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage persons'),
        (
            PersonRight('view', description='View persons'),
            PersonRight('add', description='Add persons'),
            PersonRight('edit', Levels.SECURE, description='Edit persons'),
            PersonRight('delete', Levels.SECURE, description='Delete persons')
        ),
        PersonGroupRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage person groups'),
        (
            PersonGroupRight('view', description='View person groups'),
            PersonGroupRight('add', description='Add person groups'),
            PersonGroupRight('edit', Levels.SECURE, description='Edit person groups'),
            PersonGroupRight('delete', Levels.SECURE, description='Delete person groups')
        ),
    )
)


DOCAPI_RIGHTS = (
    DocapiRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage DocAPI'),
    (
        DocapiTemplateRight(GLOBAL_RIGHT_IDENTIFIER, description='Manage DocAPI templates'),
        (
            DocapiTemplateRight('view', description='View template'),
            DocapiTemplateRight('add', description='Add template'),
            DocapiTemplateRight('edit', Levels.SECURE, description='Edit template'),
            DocapiTemplateRight('delete', Levels.SECURE, description='Delete template'),
        ),
    )
)

#TODO: fix this
__all__ = (
    BaseRight(
        Levels.NOTSET, GLOBAL_RIGHT_IDENTIFIER, description='Base application right'
    ),
    SYSTEM_RIGHTS,
    FRAMEWORK_RIGHTS,
    EXPORT_RIGHTS,
    IMPORT_RIGHTS,
    USER_MANAGEMENT_RIGHTS,
    DOCAPI_RIGHTS,
    ISMS_RIGHTS,
)

# ------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------- #

def flat_rights_tree(right_tree) -> list[BaseRight]:
    """
    Flat the right tree to list

    Args:
        right_tree: Tuple tree of rights

    Returns:
        list[BaseRight]: Flatted right tree
    """
    rights: list[BaseRight] = []

    for right in right_tree:
        if isinstance(right, (tuple, list)):
            rights = rights + flat_rights_tree(right)
        else:
            rights.append(right)

    return rights

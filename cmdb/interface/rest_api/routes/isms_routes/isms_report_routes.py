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
Implementation of all API routes for Isms Reports
"""
import logging
from flask import abort

from cmdb.manager.extendable_options_manager import ExtendableOptionsManager
from cmdb.manager.isms_manager.risk_matrix_manager import RiskMatrixManager
from cmdb.manager.isms_manager.risk_assessment_manager import RiskAssessmentManager
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsReportBuilder

from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import DefaultResponse

# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

isms_report_blueprint = APIBlueprint('isms_report', __name__)

# ---------------------------------------------------- CRUD-CREATE --------------------------------------------------- #

@isms_report_blueprint.route('/risk_matrix', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@isms_report_blueprint.protect(auth=True, right='base.isms.report.view')
def get_isms_risk_matrix_report(request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve the IsmsRiskMatrix Report

    Args:
        request_user (CmdbUser): CmdbUser requesting the RiskMatrix report

    Returns:
        DefaultResponse: The RiskMatrix report as a dictionary
    """
    try:
        risk_assessment_manager: RiskAssessmentManager = ManagerProvider.get_manager(
                                                                            ManagerType.RISK_ASSESSMENT,
                                                                            request_user)
        risk_matrix_manager: RiskMatrixManager = ManagerProvider.get_manager(
                                                                    ManagerType.RISK_MATRIX,
                                                                    request_user)
        extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(
                                                                                ManagerType.EXTENDABLE_OPTIONS,
                                                                                request_user)

        isms_report_builder = IsmsReportBuilder(
            risk_assessment_manager,
            risk_matrix_manager,
            extendable_options_manager
        )

        risk_matrix_report = isms_report_builder.build_risk_matrix_report()

        return DefaultResponse(risk_matrix_report).make_response()
    except Exception as err:
        LOGGER.error("[get_isms_risk_matrix_report] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving the RiskMatrix report!")

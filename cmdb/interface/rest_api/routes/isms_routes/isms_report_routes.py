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
import re
from flask import abort

from cmdb.manager.extendable_options_manager import ExtendableOptionsManager
from cmdb.manager.isms_manager.risk_matrix_manager import RiskMatrixManager
from cmdb.manager.isms_manager.risk_assessment_manager import RiskAssessmentManager
from cmdb.manager.isms_manager.control_measure_manager import ControlMeasureManager
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsReportBuilder
from cmdb.models.extendable_option_model import OptionType

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
    HTTP `GET`/`HEAD` route to retrieve the IsmsRiskMatrix report

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


@isms_report_blueprint.route('/soa', methods=['GET', 'HEAD'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@isms_report_blueprint.protect(auth=True, right='base.isms.report.view')
def get_isms_soa_report(request_user: CmdbUser):
    """
    HTTP `GET`/`HEAD` route to retrieve the Statement of Applicability(SOA) report

    Args:
        request_user (CmdbUser): CmdbUser requesting the RiskMatrix report

    Returns:
        DefaultResponse: The RiskMatrix report as a dictionary
    """
    try:
        control_measure_manager: ControlMeasureManager = ManagerProvider.get_manager(
                                                                            ManagerType.CONTROL_MEASURE,
                                                                            request_user)
        extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(
                                                                                ManagerType.EXTENDABLE_OPTIONS,
                                                                                request_user)

        # Get all implementation states for IsmsControlMeasures
        all_implementation_states = extendable_options_manager.get_many(
                                                                filter={'option_type':OptionType.IMPLEMENTATION_STATE}
                                                               )

        # Create a lookup map from public_id to value for implementation states
        implementation_state_lookup = {
            option['public_id']: option['value'] for option in all_implementation_states
        }

        all_control_meassures = control_measure_manager.get_many()

        # Replace implementation_state public_id with its corresponding value
        for cm in all_control_meassures:
            original_id = cm.get('implementation_state')
            if original_id in implementation_state_lookup:
                cm['implementation_state'] = implementation_state_lookup[original_id]

        all_sources = extendable_options_manager.get_many(
                                                    filter={'option_type':OptionType.CONTROL_MEASURE}
                                                 )

        # Create a lookup map from public_id to value for sources
        source_lookup = {
            option['public_id']: option['value'] for option in all_sources
        }

        # Replace source public_id with its corresponding value
        for cm in all_control_meassures:
            source_id = cm.get('source')
            if source_id in source_lookup:
                cm['source'] = source_lookup[source_id]

        # Order all control measures
        all_control_meassures.sort(key=sort_key)

        return DefaultResponse(all_control_meassures).make_response()
    except Exception as err:
        LOGGER.error("[get_isms_soa_report] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while retrieving the SOA report!")


# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

def sort_key(cm: dict) -> tuple:
    """
    Sort key function for Control Measures
    - First, prioritize sources where source = "ISO 27001:2022"
    - Then, sort by the identifier
    - If identifier is empty, place it last
    
    Args:
        cm (dict): Control Measure data containing 'source' and 'identifier'.

    Returns:
        tuple: A tuple that will be used for sorting:
            (priority_for_source, priority_for_empty_identifier, sorted_identifier)
    """
    # 1. Put ISO 27001:2022 first
    source_priority: int = 0 if cm.get('source') == 'ISO 27001:2022' else 1

    # 2. Identifiers that are empty or missing should come last
    identifier = cm.get('identifier')
    identifier_is_empty = not identifier or not identifier.strip()

    # This ensures that empty identifiers get a higher "penalty"
    empty_priority: int = 1 if identifier_is_empty else 0

    # 3. Convert the identifier into a list of integers for numeric sorting
    identifier_sort_value: list[int] = [int(part) if part.isdigit() else part
                                        for part in re.split(r'(\D+|\d+)', identifier or '')]

    return (source_priority, empty_priority, identifier_sort_value)

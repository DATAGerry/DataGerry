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
Implementation of all API routes for Isms Imports
"""
import io
from csv import DictReader, Sniffer, Error, excel
import logging
from typing import Optional
from flask import request, abort
from werkzeug.exceptions import HTTPException
from werkzeug.datastructures import FileStorage

from cmdb.manager import (
    ThreatManager,
    ExtendableOptionsManager,
    VulnerabilityManager,
    RiskManager,
    ControlMeassureManager,
    ProtectionGoalManager,
)
from cmdb.manager.manager_provider_model import ManagerProvider, ManagerType

from cmdb.models.user_model import CmdbUser
from cmdb.models.isms_model import IsmsImportType, ControlMeassureType, RiskType
from cmdb.models.extendable_option_model import OptionType

from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import insert_request_user, verify_api_access
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import DefaultResponse
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

isms_importer_blueprint = APIBlueprint('isms_importer', __name__)

REQUEST_FILE = "file"

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@isms_importer_blueprint.route('/<string:target>', methods=['POST'])
@insert_request_user
@verify_api_access(required_api_level=ApiLevel.LOCKED)
@isms_importer_blueprint.protect(auth=True, right='base.isms.import.add')
def import_isms_objects(target: str, request_user: CmdbUser):
    """
    Import IsmsThreats, IsmsMeassureControls, IsmsVulnerabilities and IsmsRisks

    Args:
        target (str): The ISMS object which should be imported (see IsmsImportType)
        request_user (CmdbUser): CmdbUser requesting the import
    """
    try:
        if not IsmsImportType.is_valid(target):
            abort(400, f"'{target}' is not a valid ImportType for ISMS!")

        if REQUEST_FILE not in request.files:
            LOGGER.error("[import_isms_objects] No import file!")
            abort(400, "No import file was provided!")

        csv_file: FileStorage = request.files.get(REQUEST_FILE)

        target_enum = IsmsImportType(target)
        results = handle_isms_import(csv_file, target_enum, request_user)

        return DefaultResponse(results).make_response()
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        LOGGER.error("[import_isms_objects] Exception: %s. Type: %s", err, type(err), exc_info=True)
        abort(500, "An internal server error occured while trying to import ISMS Objects!")

# -------------------------------------------------- ISMS Importers -------------------------------------------------- #

def handle_isms_import(csv_file: FileStorage, target: IsmsImportType, request_user: CmdbUser) -> dict:
    """
    Selects the handler for the provided csv file and starts the import workflow for it

    Args:
        csv_file (FileStorage): The file containing the data which should be imported
        target (IsmsImportType): The ISMS object which should be imported (see IsmsImportType)
        request_user (CmdbUser): CmdbUser requesting the import

    Returns:
        dict: The results of the import
    """
    extendable_options_manager: ExtendableOptionsManager = ManagerProvider.get_manager(ManagerType.EXTENDABLE_OPTIONS,
                                                                                       request_user)

    handlers = {
        IsmsImportType.THREAT: handle_threats_import,
        IsmsImportType.VULNERABILITY: handle_vulnerabilities_import,
        IsmsImportType.RISK: handle_risks_import,
        IsmsImportType.CONTROL_MEASSURE: handle_control_meassures_import,
    }

    handler = handlers.get(target)

    if not handler:
        abort(400, f"No handler implemented for target: {target}!")

    if target == IsmsImportType.RISK:
        return handler(csv_file, request_user)

    return handler(csv_file, request_user, extendable_options_manager)


def handle_threats_import(
        csv_file: FileStorage,
        request_user: CmdbUser,
        extendable_options_manager: ExtendableOptionsManager) -> dict:
    """
    Handles the import of IsmsThreats

    Args:
        csv_file (FileStorage): The file containing the data which should be imported
        request_user (CmdbUser): CmdbUser requesting the import
        extendable_options_manager (ExtendableOptionsManager): Manager for CmdbExtendableOptions

    Returns:
        dict: Results of IsmsThreat imports
    """
    created_threats = 0
    existing_threats = 0
    invalid_threats = []

    expected_threat_headers = {"name", "source", "identifier", "description"}

    reader = read_csv_file(csv_file, expected_threat_headers)

    threats = []
    for row in reader:
        source = handle_extendable_option(row.get("source"), extendable_options_manager, OptionType.THREAT)

        threat = {
            "name": row["name"].strip() if row.get("name") else None,
            "source": source,
            "identifier": row["identifier"].strip() if row.get("identifier") else None,
            "description": row["description"].strip() if row.get("description") else None,
        }

        # Basic validation for 'name' (required field)
        if not threat["name"]:
            invalid_threats.append(threat)
            continue

        threats.append(threat)

    threat_manager: ThreatManager = ManagerProvider.get_manager(ManagerType.THREAT, request_user)

    for a_threat in threats:
        possible_threat = threat_manager.get_one_by(a_threat)

        # An IsmsThreat already exists with the given values
        if possible_threat:
            existing_threats += 1
            continue

        threat_manager.insert_item(a_threat)
        created_threats += 1

    return {
        "imported_objects": len(threats),
        "created_objects": created_threats,
        "existing_objects": existing_threats,
        "invalid_objects": invalid_threats,
    }


def handle_vulnerabilities_import(
        csv_file: FileStorage,
        request_user: CmdbUser,
        extendable_options_manager: ExtendableOptionsManager) -> dict:
    """
    Handles the import of IsmsVulnerabilities

    Args:
        csv_file (FileStorage): The file containing the data which should be imported
        request_user (CmdbUser): CmdbUser requesting the import
        extendable_options_manager (ExtendableOptionsManager): Manager for CmdbExtendableOptions

    Returns:
        dict: Results of IsmsVulnerabilities imports
    """
    created_vulerabilities = 0
    existing_vulerabilities = 0
    invalid_vulerabilities = []

    expected_vulnerability_headers = {"name", "source", "identifier", "description"}

    reader = read_csv_file(csv_file, expected_vulnerability_headers)

    vulerabilities = []
    for row in reader:
        source = handle_extendable_option(row.get("source"), extendable_options_manager, OptionType.VULNERABILITY)

        vulnerability = {
            "name": row["name"].strip() if row.get("name") else None,
            "source": source,
            "identifier": row["identifier"].strip() if row.get("identifier") else None,
            "description": row["description"].strip() if row.get("description") else None,
        }

        # Basic validation for 'name' (required field)
        if not vulnerability["name"]:
            invalid_vulerabilities.append(vulnerability)
            continue  # or raise an error

        vulerabilities.append(vulnerability)

    vulnerability_manager: VulnerabilityManager = ManagerProvider.get_manager(ManagerType.VULNERABILITY, request_user)

    for a_vulnerability in vulerabilities:
        possible_vulnerability = vulnerability_manager.get_one_by(a_vulnerability)

        # An IsmsVulnerability already exists with the given values
        if possible_vulnerability:
            existing_vulerabilities += 1
            continue

        vulnerability_manager.insert_item(a_vulnerability)
        created_vulerabilities += 1

    return {
        "imported_objects": len(vulerabilities),
        "created_objects": created_vulerabilities,
        "existing_objects": existing_vulerabilities,
        "invalid_objects": invalid_vulerabilities,
    }


def handle_risks_import(csv_file: FileStorage, request_user: CmdbUser) -> dict:
    """
    Handles the import of IsmsRisks

    Args:
        csv_file (FileStorage): The file containing the data which should be imported
        request_user (CmdbUser): CmdbUser requesting the import

    Returns:
        dict: Results of IsmsRisks imports
    """
    protection_goal_manager: ProtectionGoalManager = ManagerProvider.get_manager(ManagerType.PROTECTION_GOAL,
                                                                                 request_user)

    threat_manager: ThreatManager = ManagerProvider.get_manager(ManagerType.THREAT, request_user)
    vulnerability_manager: VulnerabilityManager = ManagerProvider.get_manager(ManagerType.VULNERABILITY,
                                                                              request_user)

    created_risks = 0
    existing_risks = 0
    invalid_risks = []

    expected_risk_headers = {
        "name",
        "risk_type",
        "protection_goals",
        "threats",
        "vulnerabilities",
        "identifier",
        "consequences",
        "description",
    }

    reader = read_csv_file(csv_file, expected_risk_headers)

    risks = []
    for row in reader:
        is_valid = True

        risk_type = row["risk_type"].strip().upper()
        consequences = row["consequences"].strip()
        description = row["description"].strip()
        threats = parse_list_of_strings("threats", row)
        vulnerabilities = parse_list_of_strings("vulnerabilities", row)
        protection_goals = parse_list_of_strings("protection_goals", row)

        if not RiskType.is_valid(risk_type):
            is_valid = False

        if is_valid and risk_type == RiskType.THREAT_X_VULNERABILITY:
            if consequences or not threats or not vulnerabilities:
                is_valid = False
            else:
                threats = handle_threats(threats, threat_manager)
                vulnerabilities = handle_vulnerabilities(vulnerabilities, vulnerability_manager)

        if is_valid and risk_type == RiskType.THREAT:
            if consequences or vulnerabilities or not threats:
                is_valid = False
            else:
                threats = handle_threats(threats, threat_manager)

        if is_valid and risk_type == RiskType.EVENT:
            if not consequences or not description or vulnerabilities or threats:
                is_valid = False

        if is_valid:
            if protection_goals:
                protection_goals = handle_protection_goals(protection_goals, protection_goal_manager)

        risk = {
            "name": row["name"].strip() if row.get("name") else None,
            "risk_type": risk_type if is_valid else row["risk_type"].strip(),
            "identifier": row["identifier"].strip() if row.get("identifier") else None,
            "protection_goals": protection_goals if is_valid else row.get("protection_goals"),
            "threats": threats if is_valid else row.get("threats"),
            "vulnerabilities": vulnerabilities if is_valid else row.get("vulnerabilities"),
            "consequences": row["consequences"].strip() if row.get("consequences") else None,
            "description": row["description"].strip() if row.get("description") else None,
        }

        if not risk["name"] or not risk["risk_type"] or not is_valid:
            invalid_risks.append(risk)
            continue

        risks.append(risk)

    risk_manager: RiskManager = ManagerProvider.get_manager(ManagerType.RISK, request_user)

    for a_risk in risks:
        possible_risk = risk_manager.get_one_by(a_risk)

        # An IsmsRisk already exists with the given values
        if possible_risk:
            existing_risks += 1
            continue

        risk_manager.insert_item(a_risk)
        created_risks += 1

    return {
        "imported_objects": len(risks),
        "created_objects": created_risks,
        "existing_objects": existing_risks,
    }


def handle_control_meassures_import(
        csv_file: FileStorage,
        request_user: CmdbUser,
        extendable_options_manager: ExtendableOptionsManager) -> dict:
    """
    Handles the import of IsmsControlMeassures

    Args:
        csv_file (FileStorage): The file containing the data which should be imported
        request_user (CmdbUser): CmdbUser requesting the import
        extendable_options_manager (ExtendableOptionsManager): Manager for CmdbExtendableOptions

    Returns:
        dict: Results of IsmsControlMeassures imports
    """
    created_control_meassures = 0
    existing_control_meassures = 0
    invalid_control_meassures = []

    expected_control_meassure_headers = {
        "title",
        "control_meassure_type",
        "source",
        "implementation_state",
        "identifier",
        "chapter",
        "description",
        "is_applicable",
        "reason",
    }

    reader = read_csv_file(csv_file, expected_control_meassure_headers)

    control_meassures = []
    for row in reader:
        is_valid = True

        control_meassure_type = row["control_meassure_type"].strip().upper()
        source = handle_extendable_option(row.get("source"), extendable_options_manager, OptionType.CONTROL_MEASSURE)
        implementation_state = handle_extendable_option(
                                    row.get("implementation_state"),
                                    extendable_options_manager,
                                    OptionType.IMPLEMENTATION_STATE
        )
        is_applicable = row["is_applicable"].strip() if row.get("is_applicable") else None

        if not ControlMeassureType.is_valid(control_meassure_type):
            is_valid = False

        control_meassure = {
            "title": row["title"].strip() if row.get("title") else None,
            "control_meassure_type": control_meassure_type if is_valid else row["control_meassure_type"].strip(),
            "source": source,
            "implementation_state": implementation_state if is_valid else row.get("implementation_state"),
            "identifier": row["identifier"].strip() if row.get("identifier") else None,
            "chapter": row["chapter"].strip() if row.get("chapter") else None,
            "description": row["description"].strip() if row.get("description") else None,
            "is_applicable": parse_bool(is_applicable),
            "reason": row["reason"].strip() if row.get("reason") else None,
        }

        # Basic validation for 'name' (required field)
        if not control_meassure["title"] or not control_meassure["control_meassure_type"] or not is_valid:
            invalid_control_meassures.append(control_meassure)
            continue

        control_meassures.append(control_meassure)

    control_meassure_manager: ControlMeassureManager = ManagerProvider.get_manager(ManagerType.CONTROL_MEASSURE,
                                                                                   request_user)

    for a_control_meassure in control_meassures:
        possible_control_meassure = control_meassure_manager.get_one_by(a_control_meassure)

        # An IsmsControlMeassure already exists with the given values
        if possible_control_meassure:
            existing_control_meassures += 1
            continue

        control_meassure_manager.insert_item(a_control_meassure)
        created_control_meassures += 1

    return {
        "imported_objects": len(control_meassures),
        "created_objects": created_control_meassures,
        "existing_objects": existing_control_meassures,
        "invalid_objects": invalid_control_meassures,
    }

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

def read_csv_file(csv_file: FileStorage, expected_headers: set) -> DictReader:
    """
    Extracts the data from the given csv file and checks for the that all required headers are present in the data

    Args:
        csv_file (FileStorage): The csv-file containing the data
        expected_headers (set): The required headers in the csv-file

    Returns:
        DictReader: The extracted data
    """
    stream = io.StringIO(csv_file.stream.read().decode("utf-8"))

    # Detect delimiter
    sample = stream.read(1024)  # Read first 1KB for sniffing
    stream.seek(0)  # Reset stream to start again

    try:
        dialect = Sniffer().sniff(sample, delimiters=";,")
    except Error:
        dialect = excel
    reader = DictReader(stream, dialect=dialect)

    # Validate headers
    file_headers = set(reader.fieldnames or [])
    missing_headers = expected_headers - file_headers

    if missing_headers:
        abort(400, f"The following headers for Threats are missing in the CSV: {', '.join(missing_headers)}")

    return reader


def handle_extendable_option(
        option: str,
        extendable_options_manager: ExtendableOptionsManager,
        option_type: OptionType) -> Optional[int]:
    """
    Retrieves the public_id of CmdbExtendableOptions based on the value.

    If the CmdbExtendableOption does not exist, it will be created

    Args:
        option (str): _description_
        extendable_options_manager (ExtendableOptionsManager): _description_
        option_type (OptionType): _description_

    Returns:
        Optional[int]: The public_id of the corresponding CmdbExtendableOption, if an option was provided
    """
    if not option:
        return None

    possible_option = extendable_options_manager.get_one_by({'value': option, 'option_type': option_type})

    if possible_option:
        # Return the public_id of the existing CmdbExtendableOption
        return possible_option.get('public_id')

    option_dict = {
        'value':option,
        'option_type': option_type,
        'predefined': False,
    }

    # Return the public_id of the newly created CmdbExtendableOption
    return extendable_options_manager.insert_item(option_dict)


def handle_protection_goals(protection_goals: list[str], protection_goal_manager: ProtectionGoalManager) -> list:
    """
    Handles IsmsProtectionGoals which should be imported by transforming the given names to
    public_ids of IsmsProtectionGoals

    Args:
        protection_goals (list[str]): A list of protection goals
        protection_goal_manager (ProtectionGoalManager): Manager for IsmsProtectionGoals

    Returns:
        list: A list with the corresponding public_ids of IsmsProtectionGoals
    """
    proctection_goal_ids = []

    for protection_goal_name in protection_goals:
        possible_protection_goal = protection_goal_manager.get_one_by({'name': protection_goal_name})

        if possible_protection_goal:
            proctection_goal_ids.append(possible_protection_goal.get('public_id'))
        else:
            new_goal_dict = {
                'name': protection_goal_name,
                'predefined': False,
            }

            new_goal_id = protection_goal_manager.insert_item(new_goal_dict)
            proctection_goal_ids.append(new_goal_id)

    return proctection_goal_ids


def handle_threats(threats: list[str], threat_manager: ThreatManager) -> list:
    """
    Handles IsmsThreats which should be imported by transforming the given names to
    public_ids of IsmsThreats

    Args:
        threats (list[str]): A list of threats
        threat_manager (ThreatManager): Manager for IsmsThreats

    Returns:
        list: A list with the corresponding public_ids of IsmsThreats
    """
    threat_ids = []

    for threat_name in threats:
        possible_threat = threat_manager.get_one_by({'name': threat_name})

        if possible_threat:
            threat_ids.append(possible_threat.get('public_id'))
        else:
            new_threat_dict = {
                "name": threat_name,
                "source": None,
                "identifier": None,
                "description": None,
            }

            new_threat_id = threat_manager.insert_item(new_threat_dict)
            threat_ids.append(new_threat_id)

    return threat_ids


def handle_vulnerabilities(vulnerabilities: list[str], vulnerability_manager: VulnerabilityManager) -> list:
    """
    Handles IsmsVulnerabilities which should be imported by transforming the given names to
    public_ids of IsmsVulnerabilities

    Args:
        vulnerabilities (list[str]): A list of vulnerabilities
        vulnerability_manager (VulnerabilityManager): Manager for IsmsVulnerabilities

    Returns:
        list: A list with the corresponding public_ids of IsmsVulnerabilities
    """
    vulnerability_ids = []

    for vulnerability_name in vulnerabilities:
        possible_vulnerability = vulnerability_manager.get_one_by({'name': vulnerability_name})

        if possible_vulnerability:
            vulnerability_ids.append(possible_vulnerability.get('public_id'))
        else:
            new_vulnerability_dict = {
                "name": vulnerability_name,
                "source": None,
                "identifier": None,
                "description": None,
            }

            new_vulnerability_id = vulnerability_manager.insert_item(new_vulnerability_dict)
            vulnerability_ids.append(new_vulnerability_id)

    return vulnerability_ids


def parse_list_of_strings(field: str, row: dict) -> list[str]:
    """
    Safely parses a CSV field expected to be a stringified list of strings

    Args:
        field (str): The CSV field name
        row (dict): The CSV row as a dict
        line_num (int, optional): Line number for better error messages

    Returns:
        list[str]: Parsed list of strings
    """
    raw = row.get(field)

    if not raw:
        return []

    # Strip spaces and split by comma
    items = [item.strip() for item in raw.split(",") if item.strip()]

    return items


def parse_bool(value: str = None) -> bool:
    """
    Parses a flexible boolean value from a string

    Args:
        value (str, optional): The raw value (string or something convertible to string)

    Returns:
        bool: True or False, based on common truthy/falsy representations
    """
    truthy = {"true", "yes", "1"}
    falsy = {"false", "no", "0"}

    if value is None:
        return False

    if isinstance(value, bool):
        return value

    normalized = str(value).strip().lower()

    if normalized in truthy:
        return True

    if normalized in falsy:
        return False

    # Unknown values will be mapped to False
    return False

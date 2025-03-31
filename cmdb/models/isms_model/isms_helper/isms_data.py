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
This module stores all static data and methods for ISMS
"""
from cmdb.models.extendable_option_model import OptionType
# -------------------------------------------------------------------------------------------------------------------- #

def get_default_protection_goals() -> list:
    """
    All default IsmsProtectionGoals as data. Used when DataGerry is setup

    Returns:
        list: All default IsmsProtectionGoals as data
    """
    return [
        {
            'public_id': 1,
            'name': 'Confidentiality'
        },
        {
            'public_id': 2,
            'name': 'Integrity'
        },
        {
            'public_id': 3,
            'name': 'Availability'
        }
    ]


def get_default_risk_matrix() -> dict:
    """
    The default IsmsRiskMatrix. Used when DataGerry is setup

    Returns:
        list: The default IsmsRiskMatrix
    """
    return {
        'public_id': 1,
        'risk_matrix': [],
        'matrix_unit': None
    }


def get_predefined_isms_extendable_options() -> list:
    """
    All predefined CmdbExtendableOptions as data. Used when DataGerry is setup

    Returns:
        list: All default CmdbExtendableOptions as data
    """
    return [
        {
            'value': 'Open',
            'option_type': OptionType.IMPLEMENTATION_STATE,
            'predefined': True,
        },
        {
            'value': 'In Progress',
            'option_type': OptionType.IMPLEMENTATION_STATE,
            'predefined': True,
        },
        {
            'value': 'Implemented',
            'option_type': OptionType.IMPLEMENTATION_STATE,
            'predefined': True,
        }
    ]

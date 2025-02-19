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
This module contains the Root Location data
"""
# -------------------------------------------------------------------------------------------------------------------- #

def get_root_location_data() -> dict:
    """
    This method holds the correct root location data
    
    Returns:
        (dict): Returns valid root location data
    """
    return {
        "public_id":1,
        "name":"Root",
        "parent":0,
        "object_id":0,
        "type_id":0,
        "type_label":"Root",
        "type_icon":"fas fa-globe",
        "type_selectable":True
    }


def validate_root_location(tested_location: dict) -> bool:
    """
    Checks if a given location holds valid root location data

    Args:
        tested_location (dict): location data which should be tested

    Returns:
        (bool): Returns boolean if the given dict has valid root location data
    """
    root_location = get_root_location_data()

    for root_key, root_value in root_location.items():
        if root_key not in tested_location.keys():
            return False

        # check if value is valid
        if root_value != tested_location[root_key]:
            return False

    return True

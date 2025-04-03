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
Implementation of all database updater helpers
"""
import logging
# import os
# import requests

# from cmdb.errors.security import (
#     InvalidCloudUserError,
#     NoAccessTokenError,
#     RequestTimeoutError,
#     RequestError,
# )
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #

def get_db_names_from_service_portal(local_mode: bool = False) -> list[str]:
    """
    Retrieves all database names which need to be checked for updates

    Args:
        local_mode: Set to True to not retrieve db_names from Service Portal

    Returns:
        list[str]: Names of all databases
    """
    if local_mode:
        return []

    return []

    # x_access_token = os.getenv("X-ACCESS-TOKEN")

    # if not x_access_token:
    #     raise NoAccessTokenError("No x-access-token provided!")

    # headers = {
    #     "x-access-token": x_access_token
    # }

    # target = os.getenv("SERVICE-PORTAL-DATABASES-URL")

    # try:
    #     response = requests.post(target, headers=headers, timeout=3)

    #     if response.status_code == 200:
    #         return response.json()

    #     raise InvalidCloudUserError(response.json()['message'])
    # except requests.exceptions.Timeout as err:
    #     raise RequestTimeoutError(err) from err
    # except requests.exceptions.RequestException as err:
    #     raise RequestError(err) from err

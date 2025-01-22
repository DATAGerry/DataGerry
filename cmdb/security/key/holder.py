# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
"""TODO: document"""
import os
import base64
import logging
from flask import current_app

from cmdb.database import MongoDatabaseManager
from cmdb.manager import SettingsReaderManager
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                   KeyHolder - CLASS                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
class KeyHolder:
    """TODO: document"""

    def __init__(self, dbm: MongoDatabaseManager):
        """
        Args:
            key_directory: key based directory
        """
        self.settings_reader = SettingsReaderManager(dbm)
        self.rsa_public = self.get_public_key()
        self.rsa_private = self.get_private_key()


    def get_public_key(self):
        """TODO: document"""
        if current_app.cloud_mode:
            return current_app.asymmetric_key['public']
            # if current_app.local_mode:
            #     return current_app.asymmetric_key['public']

            # public_key = base64.b64decode(os.getenv("DG_RSA_PUBLIC_KEY"))

            # if not public_key:
            #     LOGGER.error("Error: No RSA public key provided!")

            # return public_key

        return self.settings_reader.get_value('asymmetric_key', 'security')['public']


    def get_private_key(self):
        """TODO: document"""
        if current_app.cloud_mode:
            return current_app.asymmetric_key['private']
            # if current_app.local_mode:
            #     return current_app.asymmetric_key['private']

            # private_key = base64.b64decode(os.getenv("DG_RSA_PRIVATE_KEY"))

            # if not private_key:
            #     LOGGER.error("Error: No RSA private key provided!")

            # return private_key

        return self.settings_reader.get_value('asymmetric_key', 'security')['private']

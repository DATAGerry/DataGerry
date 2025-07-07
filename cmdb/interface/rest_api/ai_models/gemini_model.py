# DataGerry - OpenSource Enterprise CMDB
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
Gemini model initialisation
"""
import logging
import os
import google.generativeai as genai
from dotenv import load_dotenv
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #

load_dotenv()

# LOGGER.debug(f"GOOGLE-API-KEY: {os.getenv('GOOGLE_API_KEY')}")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model once
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

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
Implementation of IsmsImportType enumeration
"""
from enum import Enum
# -------------------------------------------------------------------------------------------------------------------- #

class IsmsImportType(str, Enum):
    """
    Available IsmsImportTypes
    """
    RISK = 'risk'
    CONTROL_MEASURE = 'control_measure'
    THREAT = 'threat'
    VULNERABILITY = 'vulnerability'


    @classmethod
    def is_valid(cls, value: str) -> bool:
        """
        Checks if a given string is a valid IsmsImportType

        Args:
            value (str): The string to check

        Returns:
            bool: True if the string matches an existing IsmsImportType, False otherwise
        """
        return value in cls._value2member_map_

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
Implementation of FileMetaData
"""
import logging
from typing import Optional

# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 FileMetadata - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class FileMetadata:
    """
    A class representing metadata for a file or folder

    Attributes:
        author_id (str): The ID of the author of the file/folder
        permissions (Optional[str]): The permissions associated with the file/folder
        reference (Optional[str]): A reference to another object
        reference_type (Optional[str]): The type of reference (if any)
        folder (bool): Whether the object represents a folder
        parent (Optional[int]): The ID of the parent folder or object
        mime_type (str): The MIME type of the file, default is "application/json"
    """

    #pylint: disable=R0917
    def __init__(
            self,
            author_id,
            permissions = None,
            reference = None,
            reference_type = None,
            folder: bool = False,
            parent: int = None,
            mime_type = "application/json"):
        """
        Initialize the FileMetadata

        Args:
            author_id (str): The ID of the author
            permissions (Optional[str]): The permissions for the file/folder
            reference (Optional[str]): The reference associated with the file/folder
            reference_type (Optional[str]): The type of reference (if any)
            folder (bool): A flag indicating if it's a folder
            parent (Optional[int]): The ID of the parent folder
            mime_type (str): The MIME type for the file
        """
        self.reference = reference
        self.reference_type = reference_type
        self.mime_type = mime_type
        self.author_id = author_id
        self.folder = folder
        self.parent = parent
        self.permission = permissions


    def get_ref_to(self) -> Optional[str]:
        """
        Get the reference associated with this file/folder

        Returns:
            Optional[str]: The reference, or None if not set
        """
        return self.reference


    def get_ref_to_type(self) -> str:
        """
        Get the reference type associated with this file/folder

        Returns:
            str: The reference type, or an empty string if not set
        """
        return self.reference_type or ""


    def get_mime_type(self) -> str:
        """
        Get the MIME type associated with this file/folder

        Returns:
            str: The MIME type, default is "application/json"
        """
        return self.mime_type or "application/json"


    def get_permission(self) -> Optional[str]:
        """
        Get the permissions associated with this file/folder

        Returns:
            Optional[str]: The permissions, or None if not set
        """
        return self.permission


    @classmethod
    def to_json(cls, instance: "FileMetadata") -> dict:
        """
        Convert a FileMetadata instance to a JSON-compatible dictionary

        Args:
            instance (FileMetadata): The FileMetadata to convert

        Returns:
            dict: A dictionary representation of the FileMetadata
        """
        return {
            'reference': instance.get_ref_to(),
            'reference_type': instance.get_ref_to_type(),
            'mime_type': instance.get_mime_type(),
            'author_id': instance.author_id,
            'folder': instance.folder,
            'parent': instance.parent,
            'permission': instance.permission,
        }

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
Implementation of the DocApiRenderer in DataGerry
"""
import logging
from io import BytesIO

from cmdb.manager import (
    ObjectsManager,
    DocapiTemplatesManager,
)

from cmdb.models.object_model import CmdbObject
from cmdb.framework.rendering.cmdb_render import CmdbRender
from cmdb.models.docapi_model.object_document_generator import ObjectDocumentGenerator
from cmdb.models.docapi_model.pdf_document_type import PdfDocumentType
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                DocApiRenderer - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class DocApiRenderer:
    """
     A renderer for generating documents from CmdbObjects using predefined templates
    """
    #TODO: INIT-FIX (refactor the initalisation)
    def __init__(self, objects_manager: ObjectsManager, docapi_manager: DocapiTemplatesManager):
        """
        Initializes the DocApiRenderer

        Args:
            objects_manager (ObjectsManager): The manager responsible for CmdbObjects
            docapi_manager (DocapiTemplatesManager): The manager handling DocapiTemplates
        """
        self.docapi_manager = docapi_manager
        self.objects_manager = objects_manager


    def render_object_template(self, doctpl_id: int, object_id: int) -> BytesIO:
        """
        Renders a document by applying the provided DocapiTemplate to a CmdbObject

        This method retrieves the DocapiTemplate and the CmdbObject using their respective IDs,
        then generates a PDF document by rendering the DocapiTemplate with the CmdbObject's data.

        Steps involved:
            1. Fetch the template using the template ID (`doctpl_id`)
            2. Retrieve the CMDB object using the object ID (`object_id`)
            3. Fetch the object type information for the CMDB object
            4. Create a `CmdbRender` object to prepare the data
            5. Use `ObjectDocumentGenerator` to generate a PDF document
            6. Return the generated PDF as a BytesIO object

        Args:
            doctpl_id (int): The public_id of the DocapiTemplate to be used
            object_id (int): The public_id of the CmdbObject to be rendered in the DocapiTemplate

        Returns:
            BytesIO: A file-like object containing the generated PDF document
        """
        template = self.docapi_manager.get_template(doctpl_id)
        cmdb_object = self.objects_manager.get_object(object_id)
        cmdb_object = CmdbObject.from_data(cmdb_object)
        type_instance = self.objects_manager.get_object_type(cmdb_object.get_type_id())

        cmdb_render_object = CmdbRender(cmdb_object,
                                        type_instance,
                                        None,
                                        False,
                                        self.objects_manager.dbm)

        generator = ObjectDocumentGenerator(template,
                                            cmdb_render_object.result(),
                                            PdfDocumentType(),
                                            self.objects_manager)

        return generator.generate_doc()

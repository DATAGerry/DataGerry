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
Represents an ObjectDocumentGenerator in DataGerry
"""
import logging
from io import BytesIO

from cmdb.manager import ObjectsManager

from cmdb.framework.docapi.docapi_template.docapi_template import DocapiTemplate
from cmdb.models.docapi_model.template_engine import TemplateEngine
from cmdb.models.docapi_model.pdf_document_type import PdfDocumentType
from cmdb.framework.docapi.object_template_data import ObjectTemplateData
from cmdb.framework.rendering.render_result import RenderResult
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                            ObjectDocumentGenerator - CLASS                                           #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectDocumentGenerator:
    """
    A generator for creating document files from templates
    """
    # Default CSS to ensure consistent document styling in TinyMCE and the final PDF
    default_css = """
        img {
            zoom: 70%;
        }

        td {
            padding: 1px;
        }
    """

    def __init__(
            self,
            template: DocapiTemplate,
            cmdb_object: RenderResult,
            doctype: PdfDocumentType,
            objects_manager: ObjectsManager):
        """
        Initializes the ObjectDocumentGenerator

        Args:
            template (DocapiTemplate): The template object containing structure and styling
            cmdb_object (RenderResult): The CmdbObject RenderResult
            doctype (PdfDocumentType): The document type that determines the final output format
            objects_manager (ObjectsManager): The manager responsible for CmdbObject operations
        """
        self.template = template
        self.cmdb_object = cmdb_object
        self.doctype = doctype
        self.objects_manager = objects_manager


    def generate_doc(self) -> BytesIO:
        """
        Generates a document by rendering the template with CmdbObject data

        The method fetches relevant data, applies it to the template,
        constructs an HTML document, and then generates the final document

        Returns:
            BytesIO: A file-like object containing the generated PDF document
        """
        template_data = ObjectTemplateData(self.cmdb_object, self.objects_manager).get_template_data()

        rendered_template = TemplateEngine().render_template_string(self.template.get_template_data(), template_data)

        # Construct the full HTML document
        html = (
            f"<html><head>"
            f'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
            f'<meta charset="UTF-8" />'
            f'<title>{self.template.get_label()}</title>'
            f'<style>{self.default_css}{self.template.get_template_style()}</style>'
            f"</head><body>{rendered_template}</body></html>"
        )

        # Generate and return the final document
        return self.doctype.create_doc(html)

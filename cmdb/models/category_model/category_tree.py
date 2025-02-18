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
"""document"""
#TODO: DOCUMENT-FIX
import logging

from cmdb.models.type_model import CmdbType
from cmdb.models.category_model.cmdb_category import CmdbCategory
from cmdb.models.category_model.category_node import CategoryNode
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 CategoryTree - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class CategoryTree:
    """document"""
    #TODO: DOCUMENT-FIX
    MODEL = 'CategoryTree'

    def __init__(self, categories: list[CmdbCategory], types: list[CmdbType] = None):
        """document"""
        #TODO: DOCUMENT-FIX
        self._categories: list[CmdbCategory] = categories
        self._types: list[CmdbType] = types
        self._tree: list[CategoryNode] = sorted(self.__create_tree(self._categories, types=self._types),
                                                             key=lambda node: (
                                                             node.get_order() is None, node.get_order()))


    def __len__(self) -> int:
        """Get length of tree - this means the number of root categories"""
        return len(self._tree)


    def flat(self) -> list[CmdbCategory]:
        """Returns a flatted tree with tree like category order"""
        flatted = []
        for node in self.tree:
            flatted += node.flatten()
        return flatted


    @property
    def tree(self) -> list[CategoryNode]:
        """Get the tree"""
        if not self._tree:
            self._tree = CategoryTree.__create_tree(self._categories, types=self._types)
        return self._tree


    @classmethod
    def __create_tree(cls, categories, parent: int = None, types: list[CmdbType] = None) -> list[CategoryNode]:
        """
        Generate the category tree from list structure
        Args:
            categories: list of root/child categories
            parent: the parent id of the current subset, None if root list
            types: list of all possible types
        """
        return list(
            CategoryNode(
                category,
                cls.__create_tree(categories, category.get_public_id(), types),
                types
            )
            for category in categories if category.get_parent() == parent
        )


    @classmethod
    def from_data(cls, raw_categories: list[dict]) -> "CategoryTree":
        """Create the category list from raw data"""
        categories: list[CmdbCategory] = [CmdbCategory.from_data(category) for category in raw_categories]
        return cls(categories=categories)


    @classmethod
    def to_json(cls, instance: "CategoryTree"):
        """Get the complete category tree as json"""
        return [CategoryNode.to_json(node) for node in instance.tree]

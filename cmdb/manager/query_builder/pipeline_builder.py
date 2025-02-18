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

from cmdb.manager.query_builder.builder import Builder # TODO: REFACTOR-FIX
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                PipelineBuilder - CLASS                                               #
# -------------------------------------------------------------------------------------------------------------------- #
class PipelineBuilder(Builder):
    """Pipeline query builder for database aggregation search"""

    def __init__(self, pipeline: list[dict] = None):
        """Init constructor
        Args:
            pipeline: preset a for defined pipeline
        """
        self._pipeline = pipeline if pipeline is not None else []


    def __len__(self) -> int:
        """Get the number of aggregate pipes inside the pipeline
        Returns (int): number of pipes
        """
        return len(self.pipeline)


    def clear(self):
        """Clear the pipeline"""
        self.pipeline = []


    @property
    def pipeline(self) -> list[dict]:
        """document"""
        #TODO: DOCUMENT-FIX
        return self._pipeline


    @pipeline.setter
    def pipeline(self, pipes: list[dict]):
        self._pipeline = pipes


    def add_pipe(self, pipe: dict):
        """Add a pipe to the pipeline"""
        self._pipeline.append(pipe)


    def remove_pipe(self, pipe: dict):
        """Remove a pipe to the pipeline"""
        self._pipeline.remove(pipe)


    def build(self, *args, **kwargs) -> list[dict]:
        """document"""
        #TODO: DOCUMENT-FIX
        raise NotImplementedError

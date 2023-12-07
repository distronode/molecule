"""Distronode Galaxy dependencies for lists of collections."""
import logging
import os

from molecule import util
from molecule.dependency.distronode_galaxy.base import DistronodeGalaxyBase

LOG = logging.getLogger(__name__)


class Collections(DistronodeGalaxyBase):
    """Collection-specific Distronode Galaxy dependency handling."""

    FILTER_OPTS = ("role-file",)  # type: ignore
    COMMANDS = ("collection", "install")

    @property
    def default_options(self):
        general = super().default_options
        specific = util.merge_dicts(
            general,
            {
                "requirements-file": os.path.join(
                    self._config.scenario.directory,
                    "collections.yml",
                ),
            },
        )

        return specific

    @property
    def default_env(self):
        return super().default_env

    @property
    def requirements_file(self):
        return self.options["requirements-file"]

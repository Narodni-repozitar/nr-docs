# Copyright (c) 2022 Miroslav Bauer
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from docs_app import config as config
from invenio_base.utils import obj_or_import_string
import re


class DocsAppExtension:
    def __init__(self, app=None):
        if app:
            self.init_config(app)
            self.init_app(app)
            self.init_resource(app)

    def init_app(self, app):
        app.extensions["docs_app"] = self

    def init_resource(self, app):
        """Initialize vocabulary resources."""
        self.resource = obj_or_import_string(app.config["DOCS_APP_RESOURCE"])(
            config=obj_or_import_string(app.config["DOCS_APP_RESOURCE_CONFIG"])(),
        )

    def init_config(self, app):
        """Initialize configuration."""
        for identifier in dir(config):
            if re.match("^[A-Z_]*$", identifier) and not identifier.startswith("_"):
                app.config.setdefault(identifier, getattr(config, identifier))

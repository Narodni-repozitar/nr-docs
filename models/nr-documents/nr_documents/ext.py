import re
from functools import cached_property

from nr_documents import config as config


class NrDocumentsExt:
    """nr_documents extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        self.resource = None
        self.service = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""

        self.init_config(app)
        if not self.is_inherited():
            self.init_resource(app)
            self.register_flask_extension(app)

    def register_flask_extension(self, app):
        app.extensions["nr_documents"] = self

    def init_resource(self, app):
        """Initialize vocabulary resources."""
        self.service = app.config["NR_DOCUMENTS_SERVICE_CLASS_NR_DOCUMENTS"](
            config=app.config["NR_DOCUMENTS_SERVICE_CONFIG_NR_DOCUMENTS"](),
        )
        self.resource = app.config["NR_DOCUMENTS_RESOURCE_CLASS_NR_DOCUMENTS"](
            service=self.service,
            config=app.config["NR_DOCUMENTS_RESOURCE_CONFIG_NR_DOCUMENTS"](),
        )

    def init_config(self, app):
        """Initialize configuration."""
        for identifier in dir(config):
            if re.match("^[A-Z_0-9]*$", identifier) and not identifier.startswith("_"):
                app.config.setdefault(identifier, getattr(config, identifier))

    def is_inherited(self):
        from importlib_metadata import entry_points

        ext_class = type(self)
        for ep in entry_points(group="invenio_base.apps"):
            loaded = ep.load()
            if loaded is not ext_class and issubclass(ext_class, loaded):
                return True
        for ep in entry_points(group="invenio_base.api_apps"):
            loaded = ep.load()
            if loaded is not ext_class and issubclass(ext_class, loaded):
                return True
        return False


class Nr_documentsExt:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""

        self.init_config(app)
        if not self.is_inherited():
            self.register_flask_extension(app)

    def register_flask_extension(self, app):
        app.extensions["nr_documents"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for identifier in dir(config):
            if re.match("^[A-Z_0-9]*$", identifier) and not identifier.startswith("_"):
                app.config.setdefault(identifier, getattr(config, identifier))

    def is_inherited(self):
        from importlib_metadata import entry_points

        ext_class = type(self)
        for ep in entry_points(group="invenio_base.apps"):
            loaded = ep.load()
            if loaded is not ext_class and issubclass(ext_class, loaded):
                return True
        for ep in entry_points(group="invenio_base.api_apps"):
            loaded = ep.load()
            if loaded is not ext_class and issubclass(ext_class, loaded):
                return True
        return False

    @cached_property
    def service_records(self):
        return config.NR_DOCUMENTS_RECORD_SERVICE_CLASS(
            config=config.NR_DOCUMENTS_RECORD_SERVICE_CONFIG(),
        )

    @cached_property
    def resource_records(self):
        return config.NR_DOCUMENTS_RECORD_RESOURCE_CLASS(
            service=self.service_records,
            config=config.NR_DOCUMENTS_RECORD_RESOURCE_CONFIG(),
        )

import re
from functools import cached_property

from invenio_rdm_records.services.pids import PIDManager, PIDsService
from oarepo_requests.proxies import current_oarepo_requests_service
from oarepo_requests.resources.draft.config import DraftRecordRequestsResourceConfig
from oarepo_requests.resources.draft.types.config import DraftRequestTypesResourceConfig
from oarepo_runtime.config import build_config

from documents import config


class DocumentsExt:

    def __init__(self, app=None):

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.app = app

        self.init_config(app)
        if not self.is_inherited():
            self.register_flask_extension(app)

        for method in dir(self):
            if method.startswith("init_app_callback_"):
                getattr(self, method)(app)

    def register_flask_extension(self, app):

        app.extensions["documents"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for identifier in dir(config):
            if re.match("^[A-Z_0-9]*$", identifier) and not identifier.startswith("_"):
                if isinstance(app.config.get(identifier), list):
                    app.config[identifier] += getattr(config, identifier)
                elif isinstance(app.config.get(identifier), dict):
                    for k, v in getattr(config, identifier).items():
                        if k not in app.config[identifier]:
                            app.config[identifier][k] = v
                else:
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

    def load_action_permissions(self, sender, identity):
        # TODO: need to have a deeper look at this
        from flask_principal import ActionNeed
        from invenio_access.models import ActionUsers

        user_id = identity.id
        if user_id is None:
            return

        for au in ActionUsers.query.filter_by(user_id=user_id, exclude=False).all():
            identity.provides.add(ActionNeed(au.action))

    def init_app_callback_identity_loaded(self, app):
        """Load action permissions into the identity when it is loaded."""

        from flask_principal import identity_loaded

        identity_loaded.connect_via(app)(self.load_action_permissions)

    def init_app_callback_facets_i18n(self, app):
        """Patch i18n in facets"""
        from invenio_i18n import lazy_gettext as _
        from invenio_rdm_records.records.systemfields.access.field.record import (
            AccessStatusEnum,
        )

        from documents.services.records.facets import access_status

        access_status._value_labels = {
            AccessStatusEnum.OPEN.value: _("access.status.open"),
            AccessStatusEnum.EMBARGOED.value: _("access.status.embargoed"),
            AccessStatusEnum.RESTRICTED.value: _("access.status.restricted"),
            AccessStatusEnum.METADATA_ONLY.value: _("access.status.metadata-only"),
        }

    @cached_property
    def service_records(self):
        service_config = build_config(config.DOCUMENTS_RECORD_SERVICE_CONFIG, self.app)

        service_kwargs = {
            "pids_service": PIDsService(service_config, PIDManager),
            "config": service_config,
        }
        return config.DOCUMENTS_RECORD_SERVICE_CLASS(
            **service_kwargs,
            files_service=self.service_files,
            draft_files_service=self.service_draft_files,
        )

    @cached_property
    def resource_records(self):
        return config.DOCUMENTS_RECORD_RESOURCE_CLASS(
            service=self.service_records,
            config=build_config(config.DOCUMENTS_RECORD_RESOURCE_CONFIG, self.app),
        )

    @cached_property
    def service_record_requests(self):
        return config.DOCUMENTS_REQUESTS_SERVICE_CLASS(
            record_service=self.service_records,
            oarepo_requests_service=current_oarepo_requests_service,
        )

    @cached_property
    def resource_record_requests(self):
        return config.DOCUMENTS_REQUESTS_RESOURCE_CLASS(
            service=self.service_record_requests,
            config=build_config(config.DOCUMENTS_RECORD_RESOURCE_CONFIG, self.app),
            record_requests_config=DraftRecordRequestsResourceConfig(),
        )

    @cached_property
    def service_record_request_types(self):
        return config.DOCUMENTS_REQUEST_TYPES_SERVICE_CLASS(
            record_service=self.service_records,
            oarepo_requests_service=current_oarepo_requests_service,
        )

    @cached_property
    def resource_record_request_types(self):
        return config.DOCUMENTS_REQUEST_TYPES_RESOURCE_CLASS(
            service=self.service_record_request_types,
            config=build_config(config.DOCUMENTS_RECORD_RESOURCE_CONFIG, self.app),
            record_requests_config=DraftRequestTypesResourceConfig(),
        )

    def init_app_callback_rdm_models(self, app):

        app.config.setdefault("GLOBAL_SEARCH_MODELS", [])
        for cfg in app.config["GLOBAL_SEARCH_MODELS"]:
            if cfg["model_service"] == RDM_MODEL_CONFIG["model_service"]:
                break
        else:
            app.config["GLOBAL_SEARCH_MODELS"].append(RDM_MODEL_CONFIG)

        app.config.setdefault("RDM_MODELS", [])
        for cfg in app.config["RDM_MODELS"]:
            if cfg["model_service"] == RDM_MODEL_CONFIG["model_service"]:
                break
        else:
            app.config["RDM_MODELS"].append(RDM_MODEL_CONFIG)

    @cached_property
    def service_files(self):
        service_config = build_config(config.DOCUMENTS_FILES_SERVICE_CONFIG, self.app)

        service_kwargs = {"config": service_config}
        return config.DOCUMENTS_FILES_SERVICE_CLASS(
            **service_kwargs,
        )

    @cached_property
    def resource_files(self):
        return config.DOCUMENTS_FILES_RESOURCE_CLASS(
            service=self.service_files,
            config=build_config(config.DOCUMENTS_FILES_RESOURCE_CONFIG, self.app),
        )

    @cached_property
    def service_draft_files(self):
        service_config = build_config(
            config.DOCUMENTS_DRAFT_FILES_SERVICE_CONFIG, self.app
        )

        service_kwargs = {"config": service_config}
        return config.DOCUMENTS_DRAFT_FILES_SERVICE_CLASS(
            **service_kwargs,
        )

    @cached_property
    def resource_draft_files(self):
        return config.DOCUMENTS_DRAFT_FILES_RESOURCE_CLASS(
            service=self.service_draft_files,
            config=build_config(config.DOCUMENTS_DRAFT_FILES_RESOURCE_CONFIG, self.app),
        )


RDM_MODEL_CONFIG = {  # allows merging stuff from other builders
    "service_id": "documents",
    # deprecated
    "model_service": "documents.services.records.service.DocumentsService",
    # deprecated
    "service_config": "documents.services.records.config.DocumentsServiceConfig",
    "api_service": "documents.services.records.service.DocumentsService",
    "api_service_config": "documents.services.records.config.DocumentsServiceConfig",
    "api_resource": "documents.resources.records.resource.DocumentsResource",
    "api_resource_config": "documents.resources.records.config.DocumentsResourceConfig",
    "ui_resource_config": "ui.documents.DocumentsUIResourceConfig",
    "record_cls": "documents.records.api.DocumentsRecord",
    "pid_type": "dcmnts",
    "draft_cls": "documents.records.api.DocumentsDraft",
}

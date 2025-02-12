import importlib_metadata
from flask_resources import HTTPJSONException, ResponseHandler, create_error_handler
from invenio_records_resources.resources import FileResourceConfig

from common.services.files.allowed_document_extensions import (
    InvalidFileExtensionException,
)
from documents.resources.files.ui import (
    DocumentsFileDraftUIJSONSerializer,
    DocumentsFileUIJSONSerializer,
)


class DocumentsFileResourceConfig(FileResourceConfig):
    """DocumentsFile resource config."""

    blueprint_name = "documents_file"
    url_prefix = "/docs/<pid_value>"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.documents.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                DocumentsFileUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

    @property
    def error_handlers(self):
        entrypoint_error_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.documents_files.error_handlers"
        ):
            entrypoint_error_handlers.update(x.load())
        return {**super().error_handlers, **entrypoint_error_handlers}


class DocumentsFileDraftResourceConfig(FileResourceConfig):
    """DocumentsFileDraft resource config."""

    blueprint_name = "documents_file_draft"
    url_prefix = "/docs/<pid_value>/draft"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.documents.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                DocumentsFileDraftUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

    @property
    def error_handlers(self):
        entrypoint_error_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.documents_draft_files.error_handlers"
        ):
            entrypoint_error_handlers.update(x.load())
        return {**super().error_handlers, **entrypoint_error_handlers}

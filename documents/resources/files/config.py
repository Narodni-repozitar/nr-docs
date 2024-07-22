import importlib_metadata
from documents.resources.files.ui import (
    DocumentsFileDraftUIJSONSerializer,
    DocumentsFileUIJSONSerializer,
)
from flask_resources import ResponseHandler
from invenio_records_resources.resources import FileResourceConfig


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

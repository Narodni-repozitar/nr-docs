import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import FileResourceConfig

from nr_documents.resources.files.ui import (
    NrDocumentsFileDraftUIJSONSerializer,
    NrDocumentsFileUIJSONSerializer,
)


class NrDocumentsFileResourceConfig(FileResourceConfig):
    """NrDocumentsFile resource config."""

    blueprint_name = "nr_documents_file"
    url_prefix = "/nr-documents/<pid_value>"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.nr_documents.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                NrDocumentsFileUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }


class NrDocumentsFileDraftResourceConfig(FileResourceConfig):
    """NrDocumentsFileDraft resource config."""

    blueprint_name = "nr_documents_file_draft"
    url_prefix = "/nr-documents/<pid_value>/draft"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.nr_documents.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                NrDocumentsFileDraftUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

import importlib_metadata
from documents.resources.records.ui import DocumentsUIJSONSerializer
from flask_resources import ResponseHandler
from invenio_drafts_resources.resources import RecordResourceConfig


class DocumentsResourceConfig(RecordResourceConfig):
    """DocumentsRecord resource config."""

    blueprint_name = "documents"
    url_prefix = "/docs/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.documents.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                DocumentsUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

import importlib_metadata
from flask_resources import ResponseHandler
from invenio_drafts_resources.resources import RecordResourceConfig
from invenio_records_resources.resources import RecordResourceConfig

from nr_documents.resources.records.ui import NrDocumentsUIJSONSerializer


class NrDocumentsResourceConfig(RecordResourceConfig):
    """NrDocumentsRecord resource config."""

    blueprint_name = "NrDocuments"
    url_prefix = "/nr-documents/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.nr_documents.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                NrDocumentsUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

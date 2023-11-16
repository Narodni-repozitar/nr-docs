import importlib_metadata
from flask_resources import ResponseHandler
from oarepo_communities.resources.community_records.config import (
    CommunityRecordsResourceConfig,
)

from nr_documents.resources.community_records.ui import (
    NrDocumentsCommunityRecordUIJSONSerializer,
)


class NrDocumentsCommunityRecordResourceConfig(CommunityRecordsResourceConfig):
    """NrDocumentsRecord resource config."""

    blueprint_name = "nr_documents_community_record"
    url_prefix = "/communities/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.nr_documents.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                NrDocumentsCommunityRecordUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

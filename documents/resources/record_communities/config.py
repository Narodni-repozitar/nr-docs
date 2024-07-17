import importlib_metadata
from documents.resources.record_communities.ui import (
    DocumentsRecordCommunitiesUIJSONSerializer,
)
from flask_resources import ResponseHandler
from oarepo_communities.resources.record_communities.config import (
    RecordCommunitiesResourceConfig,
)


class DocumentsRecordCommunitiesResourceConfig(RecordCommunitiesResourceConfig):
    """DocumentsRecord resource config."""

    blueprint_name = "documents_record_communities"
    url_prefix = "/documents/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.documents.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                DocumentsRecordCommunitiesUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

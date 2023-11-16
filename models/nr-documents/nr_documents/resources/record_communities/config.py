import importlib_metadata
from flask_resources import ResponseHandler
from oarepo_communities.resources.record_communities.config import (
    RecordCommunitiesResourceConfig,
)

from nr_documents.resources.record_communities.ui import (
    NrDocumentsRecordCommunitiesUIJSONSerializer,
)


class NrDocumentsRecordCommunitiesResourceConfig(RecordCommunitiesResourceConfig):
    """NrDocumentsRecord resource config."""

    blueprint_name = "nr_documents_record_communities"
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
                NrDocumentsRecordCommunitiesUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

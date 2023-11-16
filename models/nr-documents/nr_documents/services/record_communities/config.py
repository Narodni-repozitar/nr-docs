from oarepo_communities.services.record_communities.config import (
    RecordCommunitiesServiceConfig,
)
from oarepo_communities.services.record_communities.schema import (
    RecordCommunitiesSchema,
)

from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord


class NrDocumentsRecordCommunitiesServiceConfig(RecordCommunitiesServiceConfig):
    draft_cls = NrDocumentsDraft
    """NrDocumentsRecord service config."""
    PERMISSIONS_PRESETS = ["community", "record-communities-community"]

    url_prefix = "/nr-documents/"

    schema = RecordCommunitiesSchema

    record_cls = NrDocumentsRecord

    service_id = "nr_documents_record_communities"

    components = [*RecordCommunitiesServiceConfig.components]

    model = "nr_documents"

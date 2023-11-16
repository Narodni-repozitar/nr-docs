from oarepo_communities.services.community_records.config import (
    CommunityRecordsServiceConfig,
)

from nr_documents.records.api import NrDocumentsRecord
from nr_documents.services.records.schema import NrDocumentsSchema
from nr_documents.services.records.search import NrDocumentsSearchOptions


class NrDocumentsCommunityRecordServiceConfig(CommunityRecordsServiceConfig):
    """NrDocumentsRecord service config."""

    PERMISSIONS_PRESETS = ["community", "community-records-community"]

    url_prefix = "/communities/"

    schema = NrDocumentsSchema

    search = NrDocumentsSearchOptions

    record_cls = NrDocumentsRecord

    service_id = "nr_documents_community_record"

    components = [*CommunityRecordsServiceConfig.components]

    model = "nr_documents"

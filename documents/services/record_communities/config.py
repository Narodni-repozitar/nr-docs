from documents.records.api import DocumentsDraft, DocumentsRecord
from documents.services.records.search import DocumentsSearchOptions
from oarepo_communities.services.record_communities.config import (
    RecordCommunitiesServiceConfig,
)
from oarepo_communities.services.record_communities.schema import (
    RecordCommunitiesSchema,
)
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin


class DocumentsRecordCommunitiesServiceConfig(
    PermissionsPresetsConfigMixin, RecordCommunitiesServiceConfig
):
    """DocumentsRecord service config."""

    PERMISSIONS_PRESETS = ["workflow"]

    url_prefix = "/documents/"

    schema = RecordCommunitiesSchema

    record_cls = DocumentsRecord

    service_id = "documents_record_communities"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *RecordCommunitiesServiceConfig.components,
    ]

    model = "documents"
    draft_cls = DocumentsDraft
    search_drafts = DocumentsSearchOptions

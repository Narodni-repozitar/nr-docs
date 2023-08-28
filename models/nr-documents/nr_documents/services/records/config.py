from invenio_drafts_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services import RecordLink
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin

from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord
from nr_documents.services.records.permissions import NrDocumentsPermissionPolicy
from nr_documents.services.records.schema import NrDocumentsSchema
from nr_documents.services.records.search import NrDocumentsSearchOptions


class NrDocumentsServiceConfig(
    PermissionsPresetsConfigMixin, InvenioRecordServiceConfig
):
    """NrDocumentsRecord service config."""

    PERMISSIONS_PRESETS = ["read_only"]

    url_prefix = "/nr-documents/"

    base_permission_policy_cls = NrDocumentsPermissionPolicy

    schema = NrDocumentsSchema

    search = NrDocumentsSearchOptions

    record_cls = NrDocumentsRecord

    service_id = "nr_documents"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
        DataComponent,
    ]

    model = "nr_documents"
    draft_cls = NrDocumentsDraft

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")
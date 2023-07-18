from invenio_drafts_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import (
    RecordLink,
    RecordServiceConfig,
    pagination_links,
)
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.relations.components import CachingRelationsComponent

from nr_documents.records.api import NrDocumentsRecord
from nr_documents.services.records.permissions import NrDocumentsPermissionPolicy
from nr_documents.services.records.schema import NrDocumentsSchema
from nr_documents.services.records.search import NrDocumentsSearchOptions


class NrDocumentsServiceConfig(PermissionsPresetsConfigMixin, RecordServiceConfig):
    """NrDocumentsRecord service config."""

    url_prefix = "/nr-documents/"

    PERMISSIONS_PRESETS = ["read_only"]

    schema = NrDocumentsSchema

    search = NrDocumentsSearchOptions

    record_cls = NrDocumentsRecord
    service_id = "nr_documents"

    components = [
        *RecordServiceConfig.components,
        CachingRelationsComponent,
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
        DataComponent,
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
    ]

    model = "nr_documents"

    base_permission_policy_cls = NrDocumentsPermissionPolicy

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")

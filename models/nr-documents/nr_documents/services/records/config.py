from invenio_drafts_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_drafts_resources.services.records.config import is_record
from invenio_records_resources.services import ConditionalLink, RecordLink
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin

from nr_documents.records.api import NrDocumentsRecord
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

    @property
    def links_item(self):
        return {
            "draft": RecordLink("{+api}/{self.url_prefix}{id}/draft"),
            "latest": RecordLink("{+api}/{self.url_prefix}{id}/versions/latest"),
            "latest_html": RecordLink("{+ui}/{self.url_prefix}{id}/latest"),
            "publish": RecordLink("{+api}/{self.url_prefix}{id}/draft/actions/publish"),
            "record": RecordLink("{+api}/{self.url_prefix}{id}"),
            "self": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+api}{self.url_prefix}{id}"),
                else_=RecordLink("{+api}{self.url_prefix}{id}/draft"),
            ),
            "self_html": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+ui}{self.url_prefix}{id}"),
                else_=RecordLink("{+ui}/uploads/{id}"),
            ),
            "versions": RecordLink("{+api}/{self.url_prefix}{id}/versions"),
        }

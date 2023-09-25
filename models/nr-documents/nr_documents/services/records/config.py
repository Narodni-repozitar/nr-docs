from invenio_drafts_resources.services import (
    RecordServiceConfig as InvenioRecordDraftsServiceConfig,
)
from invenio_drafts_resources.services.records.config import is_record
from invenio_records_resources.services import ConditionalLink, RecordLink
from invenio_records_resources.services.records.components import DataComponent
from oarepo_requests.components.requests import PublishDraftComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin

from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord
from nr_documents.services.records.permissions import NrDocumentsPermissionPolicy
from nr_documents.services.records.schema import NrDocumentsSchema
from nr_documents.services.records.search import NrDocumentsSearchOptions


class NrDocumentsServiceConfig(
    PermissionsPresetsConfigMixin, InvenioRecordDraftsServiceConfig
):
    """NrDocumentsRecord service config."""

    PERMISSIONS_PRESETS = ["authenticated"]

    url_prefix = "/nr-documents/"

    base_permission_policy_cls = NrDocumentsPermissionPolicy

    schema = NrDocumentsSchema

    search = NrDocumentsSearchOptions

    record_cls = NrDocumentsRecord

    service_id = "nr_documents"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordDraftsServiceConfig.components,
        PublishDraftComponent("publish_draft", "delete_record"),
        DataComponent,
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordDraftsServiceConfig.components,
    ]

    model = "nr_documents"
    draft_cls = NrDocumentsDraft
    search_drafts = NrDocumentsSearchOptions

    @property
    def links_item(self):
        return {
            "draft": RecordLink("{+api}/nr-documents/{id}/draft"),
            "latest": RecordLink("{+api}/nr-documents/{id}/versions/latest"),
            "latest_html": RecordLink("{+ui}/docs/{id}/latest"),
            "publish": RecordLink("{+api}/nr-documents/{id}/draft/actions/publish"),
            "record": RecordLink("{+api}/nr-documents/{id}"),
            "self": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+api}/nr-documents/{id}"),
                else_=RecordLink("{+api}/nr-documents/{id}/draft"),
            ),
            "self_html": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+ui}/docs/{id}"),
                else_=RecordLink("{+ui}/uploads/{id}"),
            ),
            "versions": RecordLink("{+api}/nr-documents/{id}/versions"),
        }

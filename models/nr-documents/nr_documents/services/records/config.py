from invenio_drafts_resources.services import (
    RecordServiceConfig as InvenioRecordDraftsServiceConfig,
)

from invenio_records_resources.services import pagination_links
from invenio_records_resources.services import RecordLink, ConditionalLink
from invenio_records_resources.services.records.components import DataComponent
from oarepo_requests.components.requests import PublishDraftComponent
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin

from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord
from nr_documents.services.records.permissions import NrDocumentsPermissionPolicy
from nr_documents.services.records.schema import NrDocumentsSchema
from nr_documents.services.records.search import NrDocumentsSearchOptions


def is_draft(record, ctx):
    """Shortcut for links to determine if record is a draft."""
    return record.is_draft


def is_record(record, ctx):
    """Shortcut for links to determine if record is a record."""
    return not record.is_draft


class NrDocumentsServiceConfig(
    PermissionsPresetsConfigMixin, InvenioRecordDraftsServiceConfig
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
        *InvenioRecordDraftsServiceConfig.components,
        PublishDraftComponent("publish_draft", "delete_record"),
        DataComponent,
    ]

    model = "nr_documents"
    draft_cls = NrDocumentsDraft

    @property
    def links_item(self):
        return {
            "self": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+api}/nr-documents/{id}"),
                else_=RecordLink("{+api}/nr-documents/{id}/draft"),
            ),
            "self_html": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+ui}/docs/{id}"),
                else_=RecordLink("{+ui}/docs/{id}/edit"),
            ),
            "latest": RecordLink("{+api}/nr-documents/{id}/versions/latest"),
            # TODO: "latest_html": RecordLink("{+ui}/docs/{id}/latest"),
            "draft": RecordLink("{+api}/nr-documents/{id}/draft", when=is_record),
            "record": RecordLink("{+api}/nr-documents/{id}", when=is_draft),
            "publish": RecordLink(
                "{+api}/nr-documents/{id}/draft/actions/publish", when=is_draft
            ),
            "versions": RecordLink("{+api}/nr-documents/{id}/versions"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")

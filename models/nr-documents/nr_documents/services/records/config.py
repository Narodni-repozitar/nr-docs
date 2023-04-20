from invenio_drafts_resources.services import RecordServiceConfig
from invenio_drafts_resources.services.records.config import is_draft, is_record
from invenio_records_resources.services import (
    ConditionalLink,
    RecordLink,
    pagination_links,
)
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.relations.components import CachingRelationsComponent

from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord
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

    components = [*RecordServiceConfig.components, CachingRelationsComponent]

    model = "nr_documents"
    draft_cls = NrDocumentsDraft

    @property
    def links_item(self):
        return {
            "self": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+api}{self.url_prefix}{id}"),
                else_=RecordLink("{+api}{self.url_prefix}{id}/draft"),
            ),
            "self_html": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+ui}{self.url_prefix}{id}"),
                else_=RecordLink("{+ui}{self.url_prefix}{id}/draft"),
            ),
            "latest": RecordLink("{+api}{self.url_prefix}{id}/versions/latest"),
            "latest_html": RecordLink("{+ui}{self.url_prefix}{id}/latest"),
            "draft": RecordLink("{+api}{self.url_prefix}{id}/draft", when=is_record),
            "record": RecordLink("{+api}{self.url_prefix}{id}", when=is_draft),
            "publish": RecordLink(
                "{+api}{self.url_prefix}{id}/draft/actions/publish", when=is_draft
            ),
            "versions": RecordLink("{+api}{self.url_prefix}{id}/versions"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")

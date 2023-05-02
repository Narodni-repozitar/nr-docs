from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import RecordServiceConfig
from invenio_records_resources.services import pagination_links
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.relations.components import CachingRelationsComponent

from nr_documents.records.api import NrDocumentsRecord
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

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")

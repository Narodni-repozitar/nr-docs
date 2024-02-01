from documents.records.api import DocumentsDraft, DocumentsRecord
from documents.services.records.permissions import DocumentsPermissionPolicy
from documents.services.records.schema import DocumentsSchema
from documents.services.records.search import DocumentsSearchOptions
from invenio_drafts_resources.services.records.components import DraftFilesComponent
from invenio_drafts_resources.services.records.config import is_record
from invenio_records_resources.services import ConditionalLink, RecordLink
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.files import FilesComponent
from oarepo_runtime.services.results import RecordList

from common.services.config import FilteredResultServiceConfig


class DocumentsServiceConfig(
    PermissionsPresetsConfigMixin, FilteredResultServiceConfig
):
    """DocumentsRecord service config."""

    result_list_cls = RecordList

    PERMISSIONS_PRESETS = ["authenticated"]

    url_prefix = "/docs/"

    base_permission_policy_cls = DocumentsPermissionPolicy

    schema = DocumentsSchema

    search = DocumentsSearchOptions

    record_cls = DocumentsRecord

    service_id = "documents"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *FilteredResultServiceConfig.components,
        FilesComponent,
        DataComponent,
        DraftFilesComponent,
    ]

    model = "documents"
    draft_cls = DocumentsDraft
    search_drafts = DocumentsSearchOptions

    @property
    def links_item(self):
        return {
            "draft": RecordLink("{+api}/docs/{id}/draft"),
            "files": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+api}/docs/{id}/files"),
                else_=RecordLink("{+api}/docs/{id}/draft/files"),
            ),
            "latest": RecordLink("{+api}/docs/{id}/versions/latest"),
            "latest_html": RecordLink("{+ui}/docs/{id}/latest"),
            "publish": RecordLink("{+api}/docs/{id}/draft/actions/publish"),
            "record": RecordLink("{+api}/docs/{id}"),
            "self": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+api}/docs/{id}"),
                else_=RecordLink("{+api}/docs/{id}/draft"),
            ),
            "self_html": ConditionalLink(
                cond=is_record,
                if_=RecordLink("{+ui}/docs/{id}"),
                else_=RecordLink("{+ui}/docs/{id}/edit"),
            ),
            "versions": RecordLink("{+api}/docs/{id}/versions"),
        }

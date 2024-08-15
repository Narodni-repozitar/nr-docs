from invenio_drafts_resources.services.records.components import DraftFilesComponent
from invenio_records_resources.services import (
    ConditionalLink,
    RecordLink,
    pagination_links,
)
from invenio_records_resources.services.records.components import DataComponent
from oarepo_communities.services.components.default_workflow import CommunityDefaultWorkflowComponent
from oarepo_communities.services.components.include import CommunityInclusionComponent
from oarepo_runtime.records import has_draft, is_published_record
from oarepo_runtime.services.components import DateIssuedComponent, OwnersComponent
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.files import FilesComponent
from oarepo_vocabularies.authorities.components import AuthorityComponent
from oarepo_workflows.services.components.workflow import WorkflowComponent

from common.services.config import FilteredResultServiceConfig
from documents.records.api import DocumentsDraft, DocumentsRecord
from documents.services.records.permissions import DocumentsPermissionPolicy
from documents.services.records.results import DocumentsRecordItem, DocumentsRecordList
from documents.services.records.schema import DocumentsSchema
from documents.services.records.search import DocumentsSearchOptions


class DocumentsServiceConfig(
    PermissionsPresetsConfigMixin, FilteredResultServiceConfig
):
    """DocumentsRecord service config."""

    result_item_cls = DocumentsRecordItem

    result_list_cls = DocumentsRecordList

    PERMISSIONS_PRESETS = ["docs"]

    url_prefix = "/docs/"

    base_permission_policy_cls = DocumentsPermissionPolicy

    schema = DocumentsSchema

    search = DocumentsSearchOptions

    record_cls = DocumentsRecord

    service_id = "documents"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *FilteredResultServiceConfig.components,
        AuthorityComponent,
        DateIssuedComponent,
        CommunityDefaultWorkflowComponent,
        CommunityInclusionComponent,
        OwnersComponent,
        FilesComponent,
        DraftFilesComponent,
        DataComponent,
        WorkflowComponent,
    ]

    model = "documents"
    draft_cls = DocumentsDraft
    search_drafts = DocumentsSearchOptions

    @property
    def links_item(self):
        return {
            "draft": RecordLink("{+api}/docs/{id}/draft"),
            "edit_html": RecordLink("{+ui}/docs/{id}/edit", when=has_draft),
            "files": ConditionalLink(
                cond=is_published_record,
                if_=RecordLink("{+api}/docs/{id}/files"),
                else_=RecordLink("{+api}/docs/{id}/draft/files"),
            ),
            "latest": RecordLink("{+api}/docs/{id}/versions/latest"),
            "latest_html": RecordLink("{+ui}/docs/{id}/latest"),
            "publish": RecordLink("{+api}/docs/{id}/draft/actions/publish"),
            "record": RecordLink("{+api}/docs/{id}"),
            "requests": ConditionalLink(
                cond=is_published_record,
                if_=RecordLink("{+api}/docs/{id}/requests"),
                else_=RecordLink("{+api}/docs/{id}/draft/requests"),
            ),
            "self": ConditionalLink(
                cond=is_published_record,
                if_=RecordLink("{+api}/docs/{id}"),
                else_=RecordLink("{+api}/docs/{id}/draft"),
            ),
            "self_html": ConditionalLink(
                cond=is_published_record,
                if_=RecordLink("{+ui}/docs/{id}"),
                else_=RecordLink("{+ui}/docs/{id}/preview"),
            ),
            "versions": RecordLink("{+api}/docs/{id}/versions"),
        }

    @property
    def links_search(self):
        return {
            **pagination_links("{+api}/docs/{?args*}"),
        }

    @property
    def links_search_drafts(self):
        return {
            **pagination_links("{+api}/user/docs/{?args*}"),
        }

    @property
    def links_search_versions(self):
        return {
            **pagination_links("{+api}/docs/{id}/versions{?args*}"),
        }

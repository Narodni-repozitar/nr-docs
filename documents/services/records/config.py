from invenio_rdm_records.services.config import RDMRecordServiceConfig
from invenio_records_resources.services import (
    ConditionalLink,
    LinksTemplate,
    RecordLink,
    pagination_links,
)
from oarepo_communities.services.components.default_workflow import (
    CommunityDefaultWorkflowComponent,
)
from oarepo_communities.services.components.include import CommunityInclusionComponent
from oarepo_communities.services.links import CommunitiesLinks
from oarepo_doi.services.components import DoiComponent
from oarepo_oaipmh_harvester.components import OaiSectionComponent
from oarepo_runtime.services.components import (
    CustomFieldsComponent,
    DateIssuedComponent,
    OwnersComponent,
    process_service_configs,
)
from oarepo_runtime.services.config import (
    has_draft,
    has_file_permission,
    has_permission,
    has_published_record,
    is_published_record,
)
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.records import pagination_links_html
from oarepo_vocabularies.authorities.components import AuthorityComponent
from oarepo_workflows.services.components.workflow import WorkflowComponent

from documents.records.api import DocumentsDraft, DocumentsRecord
from documents.services.records.permissions import DocumentsPermissionPolicy
from documents.services.records.results import DocumentsRecordItem, DocumentsRecordList
from documents.services.records.schema import DocumentsSchema
from documents.services.records.search import DocumentsSearchOptions
from invenio_rdm_records.services.components.access import AccessComponent


class DocumentsServiceConfig(PermissionsPresetsConfigMixin, RDMRecordServiceConfig):
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

    search_item_links_template = LinksTemplate
    draft_cls = DocumentsDraft
    search_drafts = DocumentsSearchOptions

    @property
    def components(self):
        return process_service_configs(self) + [
            AuthorityComponent,
            DateIssuedComponent,
            DoiComponent,
            OaiSectionComponent,
            CommunityDefaultWorkflowComponent,
            CommunityInclusionComponent,
            OwnersComponent,
            CustomFieldsComponent,
            WorkflowComponent,
            AccessComponent,
        ]

    model = "documents"

    @property
    def links_item(self):
        return {
            "applicable-requests": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+api}/docs/{id}/requests/applicable"),
                else_=RecordLink("{+api}/docs/{id}/draft/requests/applicable"),
            ),
            "communities": CommunitiesLinks(
                {
                    "self": "{+api}/communities/{id}",
                    "self_html": "{+ui}/communities/{slug}/records",
                }
            ),
            "draft": RecordLink(
                "{+api}/docs/{id}/draft",
                when=has_draft() & has_permission("read_draft"),
            ),
            "edit_html": RecordLink(
                "{+ui}/docs/{id}/edit", when=has_draft() & has_permission("update")
            ),
            "files": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink(
                    "{+api}/docs/{id}/files", when=has_file_permission("list_files")
                ),
                else_=RecordLink(
                    "{+api}/docs/{id}/draft/files",
                    when=has_file_permission("list_files"),
                ),
            ),
            "latest": RecordLink(
                "{+api}/docs/{id}/versions/latest", when=has_permission("read")
            ),
            "latest_html": RecordLink(
                "{+ui}/docs/{id}/latest", when=has_permission("read")
            ),
            "publish": RecordLink(
                "{+api}/docs/{id}/draft/actions/publish", when=has_permission("publish")
            ),
            "record": RecordLink(
                "{+api}/docs/{id}", when=has_published_record() & has_permission("read")
            ),
            "requests": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+api}/docs/{id}/requests"),
                else_=RecordLink("{+api}/docs/{id}/draft/requests"),
            ),
            "self": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+api}/docs/{id}", when=has_permission("read")),
                else_=RecordLink(
                    "{+api}/docs/{id}/draft", when=has_permission("read_draft")
                ),
            ),
            "self_html": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+ui}/docs/{id}", when=has_permission("read")),
                else_=RecordLink(
                    "{+ui}/docs/{id}/preview", when=has_permission("read_draft")
                ),
            ),
            "versions": RecordLink(
                "{+api}/docs/{id}/versions", when=has_permission("search_versions")
            ),
        }

    @property
    def links_search_item(self):
        return {
            "self": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+api}/docs/{id}", when=has_permission("read")),
                else_=RecordLink(
                    "{+api}/docs/{id}/draft", when=has_permission("read_draft")
                ),
            ),
            "self_html": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+ui}/docs/{id}", when=has_permission("read")),
                else_=RecordLink(
                    "{+ui}/docs/{id}/preview", when=has_permission("read_draft")
                ),
            ),
        }

    @property
    def links_search(self):
        return {
            **pagination_links("{+api}/docs/{?args*}"),
            **pagination_links_html("{+ui}/docs/{?args*}"),
        }

    @property
    def links_search_drafts(self):
        return {
            **pagination_links("{+api}/user/docs/{?args*}"),
            **pagination_links_html("{+ui}/user/docs/{?args*}"),
        }

    @property
    def links_search_versions(self):
        return {
            **pagination_links("{+api}/docs/{id}/versions{?args*}"),
        }

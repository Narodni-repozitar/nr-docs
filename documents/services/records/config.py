from invenio_rdm_records.services.config import _groups_enabled
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
from oarepo_requests.services.components.autorequest import AutorequestComponent
from oarepo_runtime.services.components import (
    CustomFieldsComponent,
    DateIssuedComponent,
    process_service_configs,
)
from oarepo_runtime.services.config import (
    has_draft_permission,
    has_file_permission,
    has_permission,
    DraftLink,
    has_published_record,
    is_published_record,
)
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.records import pagination_links_html
from oarepo_vocabularies.authorities.components import AuthorityComponent
from oarepo_workflows.services.components.workflow import WorkflowComponent

from common.services.config import FilteredResultServiceConfig
from documents.records.api import DocumentsDraft, DocumentsRecord
from documents.services.records.permissions import DocumentsPermissionPolicy
from documents.services.records.results import DocumentsRecordItem, DocumentsRecordList
from documents.services.records.schema import DocumentsSchema
from documents.services.records.search import (
    DocumentsDraftSearchOptions,
    DocumentsSearchOptions,
)
from invenio_rdm_records.services.customizations import FromConfigPIDsProviders, FromConfigRequiredPIDs

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
    indexer_queue_name = "documents"

    search_item_links_template = LinksTemplate
    draft_cls = DocumentsDraft
    search_drafts = DocumentsDraftSearchOptions

    # PIDs configuration
    pids_providers = FromConfigPIDsProviders()
    pids_required = FromConfigRequiredPIDs()

    @property
    def components(self):
        return process_service_configs(
            self,
            AuthorityComponent,
            DateIssuedComponent,
            DoiComponent,
            OaiSectionComponent,
            CommunityDefaultWorkflowComponent,
            CommunityInclusionComponent,
            CustomFieldsComponent,
            AutorequestComponent,
            WorkflowComponent,
        )

    model = "documents"

    @property
    def links_item(self):
        try:
            supercls_links = super().links_item
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            "access_grants": RecordLink("{+api}/records/{id}/access/grants"),
            "access_groups": RecordLink(
                "{+api}/records/{id}/access/groups", when=_groups_enabled
            ),
            "access_links": RecordLink("{+api}/records/{id}/access/links"),
            "access_users": RecordLink("{+api}/records/{id}/access/users"),
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
            # TODO: changed manually, fix model builder to generate this
            "draft": DraftLink(
                "{+api}/docs/{id}/draft", when=has_draft_permission("read_draft")
            ),
            # TODO: changed manually, fix model builder to generate this
            "edit_html": DraftLink(
                "{+ui}/docs/{id}/edit", when=has_draft_permission("update_draft")
            ),
            "files": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink(
                    "{+api}/docs/{id}/files", when=has_file_permission("read_files")
                ),
                else_=RecordLink(
                    "{+api}/docs/{id}/draft/files",
                    when=has_file_permission("read_files"),
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
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search_item(self):
        try:
            supercls_links = super().links_search_item
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
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
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search(self):
        try:
            supercls_links = super().links_search
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            **pagination_links("{+api}/docs/{?args*}"),
            **pagination_links_html("{+ui}/docs/{?args*}"),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search_drafts(self):
        try:
            supercls_links = super().links_search_drafts
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            **pagination_links("{+api}/user/docs/{?args*}"),
            **pagination_links_html("{+ui}/user/docs/{?args*}"),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search_versions(self):
        try:
            supercls_links = super().links_search_versions
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            **pagination_links("{+api}/docs/{id}/versions{?args*}"),
        }
        return {k: v for k, v in links.items() if v is not None}

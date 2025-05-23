from invenio_records_resources.services import (
    FileLink,
    FileServiceConfig,
    LinksTemplate,
    RecordLink,
)
from oarepo_runtime.services.components import (
    CustomFieldsComponent,
    process_service_configs,
)
from oarepo_runtime.services.config import (
    has_file_permission,
    has_permission_file_service,
)
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin

from common.services.files.allowed_document_extensions import (
    AllowedDocumentExtensionsComponent,
)
from documents.records.api import DocumentsDraft, DocumentsRecord
from documents.services.files.schema import DocumentsFileSchema
from documents.services.records.permissions import DocumentsPermissionPolicy


class DocumentsFileServiceConfig(PermissionsPresetsConfigMixin, FileServiceConfig):
    """DocumentsRecord service config."""

    PERMISSIONS_PRESETS = ["docs"]

    url_prefix = "/docs/<pid_value>"

    base_permission_policy_cls = DocumentsPermissionPolicy

    schema = DocumentsFileSchema

    record_cls = DocumentsRecord

    service_id = "documents_file"
    indexer_queue_name = "documents_file"

    search_item_links_template = LinksTemplate
    allowed_mimetypes = []
    allowed_extensions = []
    allow_upload = False

    @property
    def components(self):
        return process_service_configs(
            self, AllowedDocumentExtensionsComponent, CustomFieldsComponent
        )

    model = "documents"

    @property
    def file_links_list(self):
        try:
            supercls_links = super().file_links_list
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            "self": RecordLink(
                "{+api}/docs/{id}/files", when=has_permission_file_service("list_files")
            ),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def file_links_item(self):
        try:
            supercls_links = super().file_links_item
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            "commit": FileLink(
                "{+api}/docs/{id}/files/{key}/commit",
                when=has_permission_file_service("commit_files"),
            ),
            "content": FileLink(
                "{+api}/docs/{id}/files/{key}/content",
                when=has_permission_file_service("get_content_files"),
            ),
            "preview": FileLink("{+ui}/docs/{id}/files/{key}/preview"),
            "self": FileLink(
                "{+api}/docs/{id}/files/{key}",
                when=has_permission_file_service("read_files"),
            ),
        }
        return {k: v for k, v in links.items() if v is not None}


class DocumentsFileDraftServiceConfig(PermissionsPresetsConfigMixin, FileServiceConfig):
    """DocumentsDraft service config."""

    PERMISSIONS_PRESETS = ["docs"]

    url_prefix = "/docs/<pid_value>/draft"

    schema = DocumentsFileSchema

    record_cls = DocumentsDraft

    service_id = "documents_file_draft"
    indexer_queue_name = "documents_file_draft"

    search_item_links_template = LinksTemplate
    permission_action_prefix = "draft_"

    @property
    def components(self):
        return process_service_configs(
            self, AllowedDocumentExtensionsComponent, CustomFieldsComponent
        )

    model = "documents"

    @property
    def file_links_list(self):
        try:
            supercls_links = super().file_links_list
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            "self": RecordLink(
                "{+api}/docs/{id}/draft/files", when=has_file_permission("read_files")
            ),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def file_links_item(self):
        try:
            supercls_links = super().file_links_item
        except AttributeError:  # if they aren't defined in the superclass
            supercls_links = {}
        links = {
            **supercls_links,
            "commit": FileLink(
                "{+api}/docs/{id}/draft/files/{key}/commit",
                when=has_file_permission("commit_files"),
            ),
            "content": FileLink(
                "{+api}/docs/{id}/draft/files/{key}/content",
                when=has_file_permission("get_content_files"),
            ),
            "preview": FileLink("{+ui}/docs/{id}/preview/files/{key}/preview"),
            "self": FileLink(
                "{+api}/docs/{id}/draft/files/{key}",
                when=has_file_permission("read_files"),
            ),
        }
        return {k: v for k, v in links.items() if v is not None}

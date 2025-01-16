from flask_resources import HTTPJSONException, create_error_handler
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
    InvalidFileExtensionException,
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

    search_item_links_template = LinksTemplate
    allowed_mimetypes = []
    allowed_extensions = []
    allow_upload = False

    @property
    def components(self):
        return process_service_configs(self) + [
            CustomFieldsComponent,
            AllowedDocumentExtensionsComponent,
        ]

    model = "documents"

    @property
    def file_links_list(self):
        return {
            "self": RecordLink(
                "{+api}/docs/{id}/files", when=has_permission_file_service("list_files")
            ),
        }

    @property
    def file_links_item(self):
        return {
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


class DocumentsFileDraftServiceConfig(PermissionsPresetsConfigMixin, FileServiceConfig):
    """DocumentsDraft service config."""

    PERMISSIONS_PRESETS = ["docs"]

    url_prefix = "/docs/<pid_value>/draft"

    schema = DocumentsFileSchema

    record_cls = DocumentsDraft

    service_id = "documents_file_draft"

    search_item_links_template = LinksTemplate

    @property
    def components(self):
        return process_service_configs(self) + [
            CustomFieldsComponent,
            AllowedDocumentExtensionsComponent,
        ]

    model = "documents"

    @property
    def file_links_list(self):
        return {
            "self": RecordLink(
                "{+api}/docs/{id}/draft/files", when=has_file_permission("list_files")
            ),
        }

    @property
    def file_links_item(self):
        return {
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

from invenio_records_resources.services import FileLink, FileServiceConfig, RecordLink
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.results import RecordList

from documents.records.api import DocumentsDraft, DocumentsRecord
from documents.services.files.permissions import DocumentsFileDraftPermissionPolicy
from documents.services.files.schema import DocumentsFileSchema
from documents.services.records.permissions import DocumentsPermissionPolicy


class DocumentsFileServiceConfig(PermissionsPresetsConfigMixin, FileServiceConfig):
    """DocumentsRecord service config."""

    result_list_cls = RecordList

    PERMISSIONS_PRESETS = ["everyone"]

    url_prefix = "/docs/<pid_value>"

    base_permission_policy_cls = DocumentsPermissionPolicy

    schema = DocumentsFileSchema

    record_cls = DocumentsRecord

    service_id = "documents_file"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *FileServiceConfig.components,
        DataComponent,
    ]

    model = "documents"
    allow_upload = False

    @property
    def file_links_list(self):
        return {
            "self": RecordLink("{+api}/docs/{id}/files"),
        }

    @property
    def file_links_item(self):
        return {
            "commit": FileLink("{+api}/docs/{id}/files/{key}/commit"),
            "content": FileLink("{+api}/docs/{id}/files/{key}/content"),
            "self": FileLink("{+api}/docs/{id}/files/{key}"),
        }


class DocumentsFileDraftServiceConfig(PermissionsPresetsConfigMixin, FileServiceConfig):
    """DocumentsDraft service config."""

    result_list_cls = RecordList

    PERMISSIONS_PRESETS = ["everyone"]

    url_prefix = "/docs/<pid_value>/draft"

    base_permission_policy_cls = DocumentsFileDraftPermissionPolicy

    schema = DocumentsFileSchema

    record_cls = DocumentsDraft

    service_id = "documents_file_draft"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *FileServiceConfig.components,
        DataComponent,
    ]

    model = "documents"

    @property
    def file_links_list(self):
        return {
            "self": RecordLink("{+api}/docs/{id}/draft/files"),
        }

    @property
    def file_links_item(self):
        return {
            "commit": FileLink("{+api}/docs/{id}/draft/files/{key}/commit"),
            "content": FileLink("{+api}/docs/{id}/draft/files/{key}/content"),
            "self": FileLink("{+api}/docs/{id}/draft/files/{key}"),
        }

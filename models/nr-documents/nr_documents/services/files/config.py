from invenio_records_resources.services import FileLink, FileServiceConfig, RecordLink
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.results import RecordList

from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord
from nr_documents.services.files.permissions import NrDocumentsFileDraftPermissionPolicy
from nr_documents.services.files.schema import NrDocumentsFileSchema
from nr_documents.services.records.permissions import NrDocumentsPermissionPolicy


class NrDocumentsFileServiceConfig(PermissionsPresetsConfigMixin, FileServiceConfig):
    """NrDocumentsRecord service config."""

    result_list_cls = RecordList

    PERMISSIONS_PRESETS = ["everyone"]

    url_prefix = "/nr-documents/<pid_value>"

    base_permission_policy_cls = NrDocumentsPermissionPolicy

    schema = NrDocumentsFileSchema

    record_cls = NrDocumentsRecord

    service_id = "nr_documents_file"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *FileServiceConfig.components,
        DataComponent,
    ]

    model = "nr_documents"
    allow_upload = False

    @property
    def file_links_list(self):
        return {
            "self": RecordLink("{+api}/nr-documents/{id}/files"),
        }

    @property
    def file_links_item(self):
        return {
            "commit": FileLink("{+api}/nr-documents/{id}/files/{key}/commit"),
            "content": FileLink("{+api}/nr-documents/{id}/files/{key}/content"),
            "self": FileLink("{+api}/nr-documents/{id}/files/{key}"),
        }


class NrDocumentsFileDraftServiceConfig(
    PermissionsPresetsConfigMixin, FileServiceConfig
):
    """NrDocumentsDraft service config."""

    result_list_cls = RecordList

    PERMISSIONS_PRESETS = ["everyone"]

    url_prefix = "/nr-documents/<pid_value>/draft"

    base_permission_policy_cls = NrDocumentsFileDraftPermissionPolicy

    schema = NrDocumentsFileSchema

    record_cls = NrDocumentsDraft

    service_id = "nr_documents_file_draft"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *FileServiceConfig.components,
        DataComponent,
    ]

    model = "nr_documents"

    @property
    def file_links_list(self):
        return {
            "self": RecordLink("{+api}/nr-documents/{id}/draft/files"),
        }

    @property
    def file_links_item(self):
        return {
            "commit": FileLink("{+api}/nr-documents/{id}/draft/files/{key}/commit"),
            "content": FileLink("{+api}/nr-documents/{id}/draft/files/{key}/content"),
            "self": FileLink("{+api}/nr-documents/{id}/draft/files/{key}"),
        }

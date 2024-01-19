from documents.files.models import DocumentsFileDraftMetadata, DocumentsFileMetadata
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records_resources.records.api import FileRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext


class DocumentsFileIdProvider(RecordIdProviderV2):
    pid_type = "dcmsfl"


class DocumentsFile(FileRecord):

    model_cls = DocumentsFileMetadata

    index = IndexField("documents_file-documents_file-1.0.0")

    pid = PIDField(
        provider=DocumentsFileIdProvider, context_cls=PIDFieldContext, create=True
    )
    record_cls = None  # is defined inside the parent record


class DocumentsFileDraft(FileRecord):

    model_cls = DocumentsFileDraftMetadata

    index = IndexField("documents_file_draft-documents_file_draft-1.0.0")

    pid = PIDField(
        provider=DocumentsFileIdProvider, context_cls=PIDFieldContext, create=True
    )
    record_cls = None  # is defined inside the parent record

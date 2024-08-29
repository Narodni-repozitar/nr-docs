from documents.files.models import DocumentsFileDraftMetadata, DocumentsFileMetadata
from invenio_records_resources.records.api import FileRecord
from invenio_records_resources.records.systemfields import IndexField


class DocumentsFile(FileRecord):

    model_cls = DocumentsFileMetadata

    index = IndexField(
        "documents_file-documents_file-1.0.0",
    )
    record_cls = None  # is defined inside the parent record


class DocumentsFileDraft(FileRecord):

    model_cls = DocumentsFileDraftMetadata

    index = IndexField(
        "documents_file_draft-documents_file_draft-1.0.0",
    )
    record_cls = None  # is defined inside the parent record

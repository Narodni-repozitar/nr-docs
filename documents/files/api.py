from invenio_records_resources.records.api import FileRecord
from invenio_records_resources.records.systemfields import IndexField

from documents.files.models import DocumentsFileDraftMetadata, DocumentsFileMetadata


class DocumentsFile(FileRecord):

    model_cls = DocumentsFileMetadata

    index = IndexField(
        "documents_file-documents_file-1.0.0", search_alias="documents_file"
    )
    record_cls = None  # is defined inside the parent record


class DocumentsFileDraft(FileRecord):

    model_cls = DocumentsFileDraftMetadata

    index = IndexField(
        "documents_file_draft-documents_file_draft-1.0.0",
        search_alias="documents_file_draft",
    )
    record_cls = None  # is defined inside the parent record

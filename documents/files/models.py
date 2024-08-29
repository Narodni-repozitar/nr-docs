from documents.records.models import DocumentsDraftMetadata, DocumentsMetadata
from invenio_db import db
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records import FileRecordModelMixin


class DocumentsFileMetadata(db.Model, RecordMetadataBase, FileRecordModelMixin):
    """Model for DocumentsFile metadata."""

    __tablename__ = "documents_file_metadata"
    __record_model_cls__ = DocumentsMetadata


class DocumentsFileDraftMetadata(db.Model, RecordMetadataBase, FileRecordModelMixin):
    """Model for DocumentsFileDraft metadata."""

    __tablename__ = "documents_file_draft_metadata"
    __record_model_cls__ = DocumentsDraftMetadata

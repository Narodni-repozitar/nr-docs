from invenio_db import db
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records import FileRecordModelMixin

from nr_documents.records.models import NrDocumentsDraftMetadata, NrDocumentsMetadata


class NrDocumentsFileMetadata(db.Model, RecordMetadataBase, FileRecordModelMixin):
    """Model for NrDocumentsFile metadata."""

    __tablename__ = "nr_documents_file_metadata"
    __record_model_cls__ = NrDocumentsMetadata


class NrDocumentsFileDraftMetadata(db.Model, RecordMetadataBase, FileRecordModelMixin):
    """Model for NrDocumentsFileDraft metadata."""

    __tablename__ = "nr_documents_file_draft_metadata"
    __record_model_cls__ = NrDocumentsDraftMetadata

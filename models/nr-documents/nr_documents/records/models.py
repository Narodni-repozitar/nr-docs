from invenio_db import db
from invenio_drafts_resources.records import ParentRecordMixin
from invenio_records.models import RecordMetadataBase


class DraftParentMetadata(db.Model, RecordMetadataBase):
    __tablename__ = "nr_documents_parent_metadata"


class NrDocumentsMetadata(db.Model, RecordMetadataBase, ParentRecordMixin):
    """Model for NrDocumentsRecord metadata."""

    __tablename__ = "nrdocuments_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

    __parent_record_model__ = DraftParentMetadata

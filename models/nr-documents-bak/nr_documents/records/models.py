from invenio_db import db
from invenio_drafts_resources.records import (
    DraftMetadataBase,
    ParentRecordMixin,
    ParentRecordStateMixin,
)
from invenio_records.models import RecordMetadataBase


class NrDocumentsParentRecordMetadata(db.Model, RecordMetadataBase):
    __tablename__ = "nr_documents_parent_metadata"


class NrDocumentsMetadata(db.Model, RecordMetadataBase, ParentRecordMixin):
    """Model for NrDocumentsRecord metadata."""

    __tablename__ = "nrdocuments_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
    __parent_record_model__ = NrDocumentsParentRecordMetadata


class NrDocumentsDraftMetadata(db.Model, DraftMetadataBase, ParentRecordMixin):
    """Model for NrDocumentsDraft metadata."""

    __tablename__ = "nrdocuments_metadata_draft"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
    __parent_record_model__ = NrDocumentsParentRecordMetadata


class ParentState(db.Model, ParentRecordStateMixin):
    __parent_record_model__ = NrDocumentsParentRecordMetadata
    __record_model__ = NrDocumentsDraftMetadata
    __draft_model__ = NrDocumentsDraftMetadata

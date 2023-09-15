from invenio_db import db
from invenio_drafts_resources.records import (
    DraftMetadataBase,
    ParentRecordMixin,
    ParentRecordStateMixin,
)
from invenio_records.models import RecordMetadataBase


class NrDocumentsParentMetadata(db.Model, RecordMetadataBase):
    __tablename__ = "nr_documents_parent_record_metadata"


class NrDocumentsMetadata(db.Model, RecordMetadataBase, ParentRecordMixin):
    """Model for NrDocumentsRecord metadata."""

    __tablename__ = "nr_documents_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

    __parent_record_model__ = NrDocumentsParentMetadata


class NrDocumentsDraftMetadata(db.Model, DraftMetadataBase, ParentRecordMixin):
    """Model for NrDocumentsDraft metadata."""

    __tablename__ = "nr_documents_draft_metadata"

    __parent_record_model__ = NrDocumentsParentMetadata


class NrDocumentsParentState(db.Model, ParentRecordStateMixin):
    table_name = "nr_documents_parent_state_metadata"

    __parent_record_model__ = NrDocumentsParentMetadata
    __record_model__ = NrDocumentsMetadata
    __draft_model__ = NrDocumentsDraftMetadata

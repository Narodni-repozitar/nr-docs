from invenio_db import db
from invenio_drafts_resources.records import (
    DraftMetadataBase,
    ParentRecordMixin,
    ParentRecordStateMixin,
)
from invenio_records.models import RecordMetadataBase


class NrDocumentsMetadata(db.Model, RecordMetadataBase):
    """Model for NrDocumentsRecord metadata."""

    __tablename__ = "nrdocuments_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

    __parent_record_model__ = DraftParentMetadata


class DraftParentMetadata(db.Model, RecordMetadataBase):
    __tablename__ = "nr_documents_parent_metadata"


class NrDocumentsDraftMetadata(db.Model, DraftMetadataBase, ParentRecordMixin):
    """Model for NrDocumentsDraft metadata."""

    __tablename__ = "nrdocumentsdraft_metadata"

    __parent_record_model__ = DraftParentMetadata


class ParentState(db.Model, ParentRecordStateMixin):
    table_name = "parent_state_metadata"

    __parent_record_model__ = DraftParentMetadata
    __record_model__ = NrDocumentsMetadata
    __draft_model__ = NrDocumentsDraftMetadata

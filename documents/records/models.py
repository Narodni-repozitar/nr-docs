from invenio_db import db
from invenio_drafts_resources.records import (
    DraftMetadataBase,
    ParentRecordMixin,
    ParentRecordStateMixin,
)
from invenio_files_rest.models import Bucket
from invenio_records.models import RecordMetadataBase
from sqlalchemy_utils import UUIDType


class DocumentsParentMetadata(db.Model, RecordMetadataBase):

    __tablename__ = "documents_parent_record_metadata"


class DocumentsMetadata(db.Model, RecordMetadataBase, ParentRecordMixin):
    """Model for DocumentsRecord metadata."""

    __tablename__ = "documents_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

    __parent_record_model__ = DocumentsParentMetadata
    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class DocumentsDraftMetadata(db.Model, DraftMetadataBase, ParentRecordMixin):
    """Model for DocumentsDraft metadata."""

    __tablename__ = "documents_draft_metadata"

    __parent_record_model__ = DocumentsParentMetadata
    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class DocumentsParentState(db.Model, ParentRecordStateMixin):
    table_name = "documents_parent_state_metadata"

    __parent_record_model__ = DocumentsParentMetadata
    __record_model__ = DocumentsMetadata
    __draft_model__ = DocumentsDraftMetadata

from invenio_db import db
from invenio_drafts_resources.records import (
    DraftMetadataBase,
    ParentRecordMixin,
    ParentRecordStateMixin,
)
from invenio_files_rest.models import Bucket
from invenio_records.models import RecordMetadataBase
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types import ChoiceType
from invenio_rdm_records.records.systemfields.deletion_status import RecordDeletionStatusEnum
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

    # The deletion status is stored in the model so that we can use it in SQL queries
    deletion_status = db.Column(
        ChoiceType(RecordDeletionStatusEnum, impl=db.String(1)),
        nullable=False,
        default=RecordDeletionStatusEnum.PUBLISHED.value,
    )

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


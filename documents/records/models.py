from invenio_communities.records.records.models import CommunityRelationMixin
from invenio_db import db
from invenio_drafts_resources.records import (
    DraftMetadataBase,
    ParentRecordMixin,
    ParentRecordStateMixin,
)
from invenio_files_rest.models import Bucket
from invenio_rdm_records.records.systemfields.deletion_status import (
    RecordDeletionStatusEnum,
)
from invenio_records.models import RecordMetadataBase
from oarepo_workflows.records.models import RecordWorkflowParentModelMixin
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types import ChoiceType, UUIDType


class DocumentsParentMetadata(
    RecordWorkflowParentModelMixin, db.Model, RecordMetadataBase
):

    __tablename__ = "documents_parent_record_metadata"


class DocumentsMetadata(db.Model, RecordMetadataBase, ParentRecordMixin):
    """Model for DocumentsRecord metadata."""

    __tablename__ = "documents_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

    __parent_record_model__ = DocumentsParentMetadata

    deletion_status = db.Column(
        ChoiceType(RecordDeletionStatusEnum, impl=db.String(1)),
        nullable=False,
        default=RecordDeletionStatusEnum.PUBLISHED.value,
    )

    media_bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id), index=True)
    media_bucket = db.relationship(Bucket, foreign_keys=[media_bucket_id])
    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket, foreign_keys=[bucket_id])


class DocumentsDraftMetadata(db.Model, DraftMetadataBase, ParentRecordMixin):
    """Model for DocumentsDraft metadata."""

    __tablename__ = "documents_draft_metadata"

    __parent_record_model__ = DocumentsParentMetadata

    deletion_status = db.Column(
        ChoiceType(RecordDeletionStatusEnum, impl=db.String(1)),
        nullable=False,
        default=RecordDeletionStatusEnum.PUBLISHED.value,
    )

    media_bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id), index=True)
    media_bucket = db.relationship(Bucket, foreign_keys=[media_bucket_id])
    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket, foreign_keys=[bucket_id])


class DocumentsCommunitiesMetadata(db.Model, CommunityRelationMixin):
    __tablename__ = "documents_communities_metadata"
    __record_model__ = DocumentsParentMetadata


class DocumentsParentState(db.Model, ParentRecordStateMixin):
    table_name = "documents_parent_state_metadata"

    __parent_record_model__ = DocumentsParentMetadata
    __record_model__ = DocumentsMetadata
    __draft_model__ = DocumentsDraftMetadata

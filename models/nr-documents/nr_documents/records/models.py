from invenio_db import db
from invenio_records.models import RecordMetadataBase


class NrDocumentsMetadata(db.Model, RecordMetadataBase):
    """Model for NrDocumentsRecord metadata."""

    __tablename__ = "nrdocuments_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}

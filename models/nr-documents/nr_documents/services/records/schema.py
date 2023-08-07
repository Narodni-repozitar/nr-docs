import marshmallow as ma
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from marshmallow import fields as ma_fields
from nr_metadata.documents.services.records.schema import (
    NRDocumentMetadataSchema,
)


class NrDocumentsSchema(InvenioBaseRecordSchema):
    """NrDocumentsSchema schema."""

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataSchema())

    class Meta:
        unknown = ma.RAISE

    metadata = ma.fields.Nested(lambda: NrDocumentsMetadataSchema())


class NrDocumentsMetadataSchema(NRDocumentMetadataSchema):
    class Meta:
        unknown = ma.RAISE

import marshmallow as ma
from nr_metadata.documents.services.records.schema import (
    NRDocumentMetadataSchema,
    NRDocumentRecordSchema,
)
from oarepo_runtime.marshmallow import BaseRecordSchema


class NrDocumentsSchema(NRDocumentRecordSchema, BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma.fields.Nested(lambda: NrDocumentsMetadataSchema())


class NrDocumentsMetadataSchema(NRDocumentMetadataSchema):
    class Meta:
        unknown = ma.RAISE

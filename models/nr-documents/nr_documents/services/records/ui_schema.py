import marshmallow as ma
from nr_metadata.documents.services.records.ui_schema import (
    NRDocumentMetadataUISchema,
    NRDocumentRecordUISchema,
)
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class NrDocumentsUISchema(NRDocumentRecordUISchema, InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma.fields.Nested(lambda: NrDocumentsMetadataUISchema())


class NrDocumentsMetadataUISchema(NRDocumentMetadataUISchema):
    class Meta:
        unknown = ma.RAISE

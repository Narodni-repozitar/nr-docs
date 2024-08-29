import marshmallow as ma
from marshmallow import fields as ma_fields
from nr_metadata.documents.services.records.ui_schema import (
    NRDocumentMetadataUISchema,
    NRDocumentRecordUISchema,
    NRDocumentSyntheticFieldsUISchema,
)
from oarepo_requests.services.ui_schema import UIRequestsSerializationMixin
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema


class DocumentsUISchema(UIRequestsSerializationMixin, NRDocumentRecordUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataUISchema())

    oai = ma_fields.Nested(lambda: OaiUISchema())

    state = ma_fields.String(dump_only=True)

    syntheticFields = ma_fields.Nested(lambda: NRDocumentSyntheticFieldsUISchema())


class OaiUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestUISchema())


class HarvestUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()

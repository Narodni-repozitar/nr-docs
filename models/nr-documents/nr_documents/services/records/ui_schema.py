import marshmallow as ma
from marshmallow import ValidationError
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from nr_metadata.documents.services.records.ui_schema import (
    NRDocumentMetadataUISchema, NRDocumentRecordUISchema)
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class NrDocumentsUISchema(InvenioUISchema):
    """NrDocumentsUISchema schema."""

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataUISchema())

    class Meta:
        unknown = ma.RAISE

    metadata = ma.fields.Nested(lambda: NrDocumentsMetadataUISchema())


class NrDocumentsMetadataUISchema(NRDocumentMetadataUISchema):
    class Meta:
        unknown = ma.RAISE

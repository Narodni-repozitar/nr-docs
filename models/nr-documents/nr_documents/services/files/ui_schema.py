import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.services.schema.ui import InvenioUISchema


class NrDocumentsFileUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    caption = ma_fields.String()


class NrDocumentsFileDraftUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

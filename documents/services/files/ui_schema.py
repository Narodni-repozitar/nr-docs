import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.services.schema.ui import InvenioUISchema


class DocumentsFileUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    caption = ma_fields.String()


# TODO this failed to generate? - there are probably multiple things wrong in the files builder due to automatic inheritance of the new requests builders; imo it should be scrapped
class DocumentsFileDraftUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

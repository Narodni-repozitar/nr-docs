import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_requests.services.ui_schema import UIRequestsSerializationMixin
from oarepo_runtime.services.schema.ui import InvenioUISchema

# TODO generally what to do with this?
class DocumentsFileUISchema(InvenioUISchema, UIRequestsSerializationMixin):
    class Meta:
        unknown = ma.RAISE

# TODO Draft file missing
class DocumentsFileDraftUISchema(InvenioUISchema, UIRequestsSerializationMixin):
    class Meta:
        unknown = ma.RAISE





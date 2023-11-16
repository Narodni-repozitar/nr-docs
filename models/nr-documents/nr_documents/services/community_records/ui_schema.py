import marshmallow as ma
from oarepo_runtime.services.schema.ui import InvenioUISchema


class NrDocumentsCommunityRecordUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

import marshmallow as ma
from oarepo_runtime.services.schema.ui import InvenioUISchema


class NrDocumentsRecordCommunitiesUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

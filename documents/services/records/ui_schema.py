import marshmallow as ma
from marshmallow import fields as ma_fields
from nr_metadata.documents.services.records.ui_schema import (
    NRDocumentMetadataUISchema,
    NRDocumentRecordUISchema,
    NRDocumentSyntheticFieldsUISchema,
)
from oarepo_requests.services.ui_schema import UIRequestsSerializationMixin
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_runtime.services.schema.ui import LocalizedDateTime
from common.services.schema import LocalizedStateField
from invenio_rdm_records.services.schemas.access import AccessSchema, EmbargoSchema
from marshmallow_utils.fields import NestedAttribute

from marshmallow import validates, ValidationError
from flask_babel import gettext as _


class AccessUISchema(DictOnlySchema):
    """UI schema for Access."""

    class Meta:
        unknown = ma.RAISE  # Prevents unknown fields

    record = ma_fields.String(required=True)
    files = ma_fields.String(required=True)
    embargo = ma_fields.Nested(lambda: EmbargoSchema())  # Assuming you need this
    status = ma_fields.String()

    def validate_protection_value(self, value, field_name):
        """Check that the protection value is valid."""
        if value not in ["public", "restricted"]:
            raise ValidationError(
                _("'{field_name}' must be either 'public' or 'restricted'").format(
                    field_name=field_name
                ),
                field_name,
            )

    @validates("record")
    def validate_record_protection(self, value):
        """Validate the record protection value."""
        self.validate_protection_value(value, "record")

    @validates("files")
    def validate_files_protection(self, value):
        """Validate the files protection value."""
        self.validate_protection_value(value, "files")


class DocumentsUISchema(UIRequestsSerializationMixin, NRDocumentRecordUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataUISchema())

    oai = ma_fields.Nested(lambda: OaiUISchema())

    # TODO: model builder seems to ignore field-class during merging of schemas,
    # need to investigate why !!!
    state = LocalizedStateField(dump_only=True)

    state_timestamp = LocalizedDateTime(dump_only=True)

    syntheticFields = ma_fields.Nested(lambda: NRDocumentSyntheticFieldsUISchema())

    access = ma_fields.Nested(lambda: AccessUISchema())


class OaiUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestUISchema())


class HarvestUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()

from marshmallow import INCLUDE, Schema, fields


class DataciteSchema(Schema):
    """Schema for Datacite in json."""

    class Meta:
        unknown = INCLUDE

    metadata = fields.Raw()
    id = fields.Str()

import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow.utils import get_value
from marshmallow_utils.fields import SanitizedUnicode
from nr_metadata.documents.services.records.schema import (
    NRDocumentMetadataSchema,
    NRDocumentRecordSchema,
    NRDocumentSyntheticFieldsSchema,
)
from oarepo_communities.schemas.parent import CommunitiesParentSchema
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_workflows.services.records.schema import WorkflowParentSchema


class GeneratedParentSchema(WorkflowParentSchema):
    """"""

    owners = ma.fields.List(ma.fields.Dict(), load_only=True)

    communities = ma_fields.Nested(CommunitiesParentSchema)


class DocumentsSchema(NRDocumentRecordSchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataSchema())

    oai = ma_fields.Nested(lambda: OaiSchema())

    syntheticFields = ma_fields.Nested(lambda: NRDocumentSyntheticFieldsSchema())
    parent = ma.fields.Nested(GeneratedParentSchema)
    files = ma.fields.Nested(
        lambda: FilesOptionsSchema(), load_default={"enabled": True}
    )

    # todo this needs to be generated for [default preview] to work
    def get_attribute(self, obj, attr, default):
        """Override how attributes are retrieved when dumping.

        NOTE: We have to access by attribute because although we are loading
              from an external pure dict, but we are dumping from a data-layer
              object whose fields should be accessed by attributes and not
              keys. Access by key runs into FilesManager key access protection
              and raises.
        """
        if attr == "files":
            return getattr(obj, attr, default)
        else:
            return get_value(obj, attr, default)


class OaiSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestSchema())


class HarvestSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()


class FilesOptionsSchema(ma.Schema):
    """Basic files options schema class."""

    enabled = ma.fields.Bool(missing=True)
    # allow unsetting
    default_preview = SanitizedUnicode(allow_none=True)

    def get_attribute(self, obj, attr, default):
        """Override how attributes are retrieved when dumping.

        NOTE: We have to access by attribute because although we are loading
              from an external pure dict, but we are dumping from a data-layer
              object whose fields should be accessed by attributes and not
              keys. Access by key runs into FilesManager key access protection
              and raises.
        """
        value = getattr(obj, attr, default)

        if attr == "default_preview" and not value:
            return default

        return value

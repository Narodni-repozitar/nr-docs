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
from oarepo_runtime.services.schema.rdm import RDMRecordMixin
from oarepo_runtime.services.schema.validation import validate_datetime
from oarepo_workflows.services.records.schema import WorkflowParentSchema
from nr_metadata.common.services.records.schema_datatypes import (
    NRLanguageVocabularySchema,
)


class GeneratedParentSchema(WorkflowParentSchema):
    """"""

    owners = ma.fields.List(ma.fields.Dict(), load_only=True)

    communities = ma_fields.Nested(CommunitiesParentSchema)


# TODO: fix model builder to include required languages. Until then
# please keep the overriden code here
class LocalNRDocumentMetadataSchema(NRDocumentMetadataSchema):
    languages = ma_fields.List(
        ma_fields.Nested(lambda: NRLanguageVocabularySchema()),
        required=True,
        validate=[ma.validate.Length(min=1)],
    )


class DocumentsSchema(NRDocumentRecordSchema, RDMRecordMixin):
    class Meta:
        unknown = ma.RAISE

    # TODO: fix model builder to include required languages. Until then
    # please keep the overriden code here
    metadata = ma_fields.Nested(lambda: LocalNRDocumentMetadataSchema())
    oai = ma_fields.Nested(lambda: OaiSchema())

    state = ma_fields.String(dump_only=True)
    is_published = ma_fields.Boolean(dump_only=True)
    state_timestamp = ma_fields.String(dump_only=True, validate=[validate_datetime])

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

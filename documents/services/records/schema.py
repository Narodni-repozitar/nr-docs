import marshmallow as ma
from invenio_drafts_resources.services.records.schema import (
    ParentSchema as InvenioParentSchema,
)
from invenio_vocabularies.services.schema import i18n_strings
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from marshmallow.utils import get_value
from marshmallow_utils.fields import SanitizedUnicode
from nr_metadata.common.services.records.schema_common import (
    AdditionalTitlesSchema,
    NRContributorSchema,
    NRCreatorSchema,
)
from nr_metadata.common.services.records.schema_datatypes import (
    NRAccessRightsVocabularySchema,
    NRAffiliationVocabularySchema,
    NRAuthorityRoleVocabularySchema,
    NRCountryVocabularySchema,
    NREventSchema,
    NRExternalLocationSchema,
    NRFunderVocabularySchema,
    NRFundingReferenceSchema,
    NRGeoLocationPointSchema,
    NRGeoLocationSchema,
    NRItemRelationTypeVocabularySchema,
    NRLanguageVocabularySchema,
    NRLicenseVocabularySchema,
    NRLocationSchema,
    NRRelatedItemContributorSchema,
    NRRelatedItemCreatorSchema,
    NRRelatedItemSchema,
    NRResourceTypeVocabularySchema,
    NRSeriesSchema,
    NRSubjectCategoryVocabularySchema,
    NRSubjectSchema,
)
from nr_metadata.documents.services.records.schema import (
    NRDegreeGrantorSchema,
    NRDocumentMetadataSchema,
    NRDocumentRecordSchema,
    NRDocumentSyntheticFieldsSchema,
    NRThesisSchema,
)
from nr_metadata.schema.identifiers import (
    NRAuthorityIdentifierSchema,
    NRObjectIdentifierSchema,
    NRSystemIdentifierSchema,
)
from oarepo_requests.services.schemas import NoneReceiverGenericRequestSchema
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_vocabularies.services.schema import HierarchySchema


class GeneratedParentSchema(InvenioParentSchema):
    """"""

    delete_record = ma.fields.Nested(NoneReceiverGenericRequestSchema)
    publish_draft = ma.fields.Nested(NoneReceiverGenericRequestSchema)

    @ma.pre_load
    def clean(self, data, **kwargs):
        """Removes dump_only fields.

        Why: We want to allow the output of a Schema dump, to be a valid input
             to a Schema load without causing strange issues.
        """
        for name, field in self.fields.items():
            if field.dump_only:
                data.pop(name, None)
        return data

    @ma.pre_load
    def clean_delete_record(self, data, **kwargs):
        """Clear review if None."""
        # draft.parent.review returns None when not set, causing the serializer
        # to dump {'review': None}. As a workaround we pop it if it's none
        # here.
        if data.get("delete_record", None) is None:
            data.pop("delete_record", None)
        return data

    @ma.post_dump()
    def pop_delete_record_if_none(self, data, many, **kwargs):
        """Clear review if None."""
        if data.get("delete_record", None) is None:
            data.pop("delete_record", None)
        return data

    @ma.pre_load
    def clean_publish_draft(self, data, **kwargs):
        """Clear review if None."""
        # draft.parent.review returns None when not set, causing the serializer
        # to dump {'review': None}. As a workaround we pop it if it's none
        # here.
        if data.get("publish_draft", None) is None:
            data.pop("publish_draft", None)
        return data

    @ma.post_dump()
    def pop_publish_draft_if_none(self, data, many, **kwargs):
        """Clear review if None."""
        if data.get("publish_draft", None) is None:
            data.pop("publish_draft", None)
        return data


class DocumentsSchema(NRDocumentRecordSchema):
    class Meta:
        unknown = ma.RAISE

    oai = ma_fields.Nested(lambda: OaiSchema())

    syntheticFields = ma_fields.Nested(lambda: SyntheticFieldsSchema())
    parent = ma.fields.Nested(GeneratedParentSchema)
    files = ma.fields.Nested(
        lambda: FilesOptionsSchema(), load_default={"enabled": True}
    )
    metadata = ma_fields.Nested(lambda: DocumentsMetadataSchema())


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


class DocumentsMetadataSchema(NRDocumentMetadataSchema):
    class Meta:
        unknown = ma.RAISE

    additionalTitles = ma_fields.List(
        ma_fields.Nested(lambda: AdditionalTitlesItemSchema())
    )

    contributors = ma_fields.List(ma_fields.Nested(lambda: ContributorsItemSchema()))

    creators = ma_fields.List(
        ma_fields.Nested(lambda: CreatorsItemSchema()),
        required=True,
        validate=[ma.validate.Length(min=1)],
    )

    thesis = ma_fields.Nested(lambda: ThesisSchema())


class GeoLocationsItemSchema(NRGeoLocationSchema):
    class Meta:
        unknown = ma.RAISE

    geoLocationPoint = ma_fields.Nested(lambda: GeoLocationPointSchema())


class OaiSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestSchema())


class RelatedItemsItemSchema(NRRelatedItemSchema):
    class Meta:
        unknown = ma.RAISE

    itemContributors = ma_fields.List(
        ma_fields.Nested(lambda: ItemContributorsItemSchema())
    )

    itemCreators = ma_fields.List(ma_fields.Nested(lambda: ItemCreatorsItemSchema()))


class AccessRightsSchema(NRAccessRightsVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class AdditionalTitlesItemSchema(AdditionalTitlesSchema):
    class Meta:
        unknown = ma.RAISE


class AffiliationsItemSchema(NRAffiliationVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    hierarchy = ma_fields.Nested(lambda: HierarchySchema())

    title = i18n_strings


class AuthorityIdentifiersItemSchema(NRAuthorityIdentifierSchema):
    class Meta:
        unknown = ma.RAISE


class ContributorsItemSchema(NRContributorSchema):
    class Meta:
        unknown = ma.RAISE


class CountrySchema(NRCountryVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class CreatorsItemSchema(NRCreatorSchema):
    class Meta:
        unknown = ma.RAISE


class DegreeGrantorsItemSchema(NRDegreeGrantorSchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    hierarchy = ma_fields.Nested(lambda: HierarchySchema())

    title = i18n_strings


class EventLocationSchema(NRLocationSchema):
    class Meta:
        unknown = ma.RAISE


class EventsItemSchema(NREventSchema):
    class Meta:
        unknown = ma.RAISE


class ExternalLocationSchema(NRExternalLocationSchema):
    class Meta:
        unknown = ma.RAISE


class FunderSchema(NRFunderVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class FundingReferencesItemSchema(NRFundingReferenceSchema):
    class Meta:
        unknown = ma.RAISE


class GeoLocationPointSchema(NRGeoLocationPointSchema):
    class Meta:
        unknown = ma.RAISE


class HarvestSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()


class InstitutionsSchema(DictOnlySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    hierarchy = ma_fields.Nested(lambda: HierarchySchema())

    title = i18n_strings


class ItemContributorsItemSchema(NRRelatedItemContributorSchema):
    class Meta:
        unknown = ma.RAISE


class ItemCreatorsItemSchema(NRRelatedItemCreatorSchema):
    class Meta:
        unknown = ma.RAISE


class ItemRelationTypeSchema(NRItemRelationTypeVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class ItemResourceTypeSchema(NRResourceTypeVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class LanguagesItemSchema(NRLanguageVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class ObjectIdentifiersItemSchema(NRObjectIdentifierSchema):
    class Meta:
        unknown = ma.RAISE


class RightsSchema(NRLicenseVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class RoleSchema(NRAuthorityRoleVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class SeriesItemSchema(NRSeriesSchema):
    class Meta:
        unknown = ma.RAISE


class SubjectCategoriesItemSchema(NRSubjectCategoryVocabularySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class SubjectsItemSchema(NRSubjectSchema):
    class Meta:
        unknown = ma.RAISE


class SyntheticFieldsSchema(NRDocumentSyntheticFieldsSchema):
    class Meta:
        unknown = ma.RAISE


class SystemIdentifiersItemSchema(NRSystemIdentifierSchema):
    class Meta:
        unknown = ma.RAISE


class ThesisSchema(NRThesisSchema):
    class Meta:
        unknown = ma.RAISE


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

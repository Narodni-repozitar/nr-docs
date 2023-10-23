import marshmallow as ma
import nr_metadata.common.services.records.schema_common
import nr_metadata.common.services.records.schema_datatypes
import nr_metadata.documents.services.records.schema
import nr_metadata.schema.identifiers
from invenio_drafts_resources.services.records.schema import (
    ParentSchema as InvenioParentSchema,
)
from invenio_vocabularies.services.schema import i18n_strings
from oarepo_requests.schemas.marshmallow import NoneReceiverGenericRequestSchema
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


class GeoLocationsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRGeoLocationSchema
):
    class Meta:
        unknown = ma.RAISE

    geoLocationPoint = ma.fields.Nested(lambda: GeoLocationPointSchema())


class NrDocumentsMetadataSchema(
    nr_metadata.documents.services.records.schema.NRDocumentMetadataSchema
):
    class Meta:
        unknown = ma.RAISE

    additionalTitles = ma.fields.List(
        ma.fields.Nested(lambda: AdditionalTitlesItemSchema())
    )

    contributors = ma.fields.List(ma.fields.Nested(lambda: ContributorsItemSchema()))

    creators = ma.fields.List(
        ma.fields.Nested(lambda: CreatorsItemSchema()),
        required=True,
        validate=[ma.validate.Length(min=1)],
    )

    thesis = ma.fields.Nested(lambda: ThesisSchema())


class NrDocumentsSchema(
    nr_metadata.documents.services.records.schema.NRDocumentRecordSchema
):
    class Meta:
        unknown = ma.RAISE

    syntheticFields = ma.fields.Nested(lambda: SyntheticFieldsSchema())
    parent = ma.fields.Nested(GeneratedParentSchema)


class RelatedItemsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRRelatedItemSchema
):
    class Meta:
        unknown = ma.RAISE

    itemContributors = ma.fields.List(
        ma.fields.Nested(lambda: ItemContributorsItemSchema())
    )

    itemCreators = ma.fields.List(ma.fields.Nested(lambda: ItemCreatorsItemSchema()))


class AccessRightsSchema(
    nr_metadata.common.services.records.schema_datatypes.NRAccessRightsVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class AdditionalTitlesItemSchema(
    nr_metadata.common.services.records.schema_common.AdditionalTitlesSchema
):
    class Meta:
        unknown = ma.RAISE


class AffiliationsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRAffiliationVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    hierarchy = ma.fields.Nested(lambda: HierarchySchema())

    title = i18n_strings


class AuthorityIdentifiersItemSchema(
    nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema
):
    class Meta:
        unknown = ma.RAISE


class ContributorsItemSchema(
    nr_metadata.common.services.records.schema_common.NRContributorSchema
):
    class Meta:
        unknown = ma.RAISE


class CountrySchema(
    nr_metadata.common.services.records.schema_datatypes.NRCountryVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class CreatorsItemSchema(
    nr_metadata.common.services.records.schema_common.NRCreatorSchema
):
    class Meta:
        unknown = ma.RAISE


class DegreeGrantorsItemSchema(
    nr_metadata.documents.services.records.schema.NRDegreeGrantorSchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    hierarchy = ma.fields.Nested(lambda: HierarchySchema())

    title = i18n_strings


class EventLocationSchema(
    nr_metadata.common.services.records.schema_datatypes.NRLocationSchema
):
    class Meta:
        unknown = ma.RAISE


class EventsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NREventSchema
):
    class Meta:
        unknown = ma.RAISE


class ExternalLocationSchema(
    nr_metadata.common.services.records.schema_datatypes.NRExternalLocationSchema
):
    class Meta:
        unknown = ma.RAISE


class FunderSchema(
    nr_metadata.common.services.records.schema_datatypes.NRFunderVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class FundingReferencesItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRFundingReferenceSchema
):
    class Meta:
        unknown = ma.RAISE


class GeoLocationPointSchema(
    nr_metadata.common.services.records.schema_datatypes.NRGeoLocationPointSchema
):
    class Meta:
        unknown = ma.RAISE


class ItemContributorsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRRelatedItemContributorSchema
):
    class Meta:
        unknown = ma.RAISE


class ItemCreatorsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRRelatedItemCreatorSchema
):
    class Meta:
        unknown = ma.RAISE


class ItemRelationTypeSchema(
    nr_metadata.common.services.records.schema_datatypes.NRItemRelationTypeVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class ItemResourceTypeSchema(
    nr_metadata.common.services.records.schema_datatypes.NRResourceTypeVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class LanguagesItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRLanguageVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class ObjectIdentifiersItemSchema(
    nr_metadata.schema.identifiers.NRObjectIdentifierSchema
):
    class Meta:
        unknown = ma.RAISE


class RightsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRLicenseVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class RoleSchema(
    nr_metadata.common.services.records.schema_datatypes.NRAuthorityRoleVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class SeriesItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRSeriesSchema
):
    class Meta:
        unknown = ma.RAISE


class SubjectCategoriesItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRSubjectCategoryVocabularySchema
):
    class Meta:
        unknown = ma.INCLUDE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class SubjectsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRSubjectSchema
):
    class Meta:
        unknown = ma.RAISE


class SyntheticFieldsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE


class SystemIdentifiersItemSchema(
    nr_metadata.schema.identifiers.NRSystemIdentifierSchema
):
    class Meta:
        unknown = ma.RAISE


class ThesisSchema(nr_metadata.documents.services.records.schema.NRThesisSchema):
    class Meta:
        unknown = ma.RAISE

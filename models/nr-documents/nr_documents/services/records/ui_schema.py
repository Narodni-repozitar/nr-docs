import marshmallow as ma
from invenio_drafts_resources.services.records.schema import (
    ParentSchema as InvenioParentSchema,
)
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from nr_metadata.common.services.records.ui_schema_common import (
    AdditionalTitlesUISchema,
    NRContributorUISchema,
    NRCreatorUISchema,
)
from nr_metadata.common.services.records.ui_schema_datatypes import (
    NRAccessRightsVocabularyUISchema,
    NRAffiliationVocabularyUISchema,
    NRAuthorityRoleVocabularyUISchema,
    NRCountryVocabularyUISchema,
    NREventUISchema,
    NRExternalLocationUISchema,
    NRFunderVocabularyUISchema,
    NRFundingReferenceUISchema,
    NRGeoLocationPointUISchema,
    NRGeoLocationUISchema,
    NRItemRelationTypeVocabularyUISchema,
    NRLanguageVocabularyUISchema,
    NRLicenseVocabularyUISchema,
    NRLocationUISchema,
    NRRelatedItemContributorUISchema,
    NRRelatedItemCreatorUISchema,
    NRRelatedItemUISchema,
    NRResourceTypeVocabularyUISchema,
    NRSeriesUISchema,
    NRSubjectCategoryVocabularyUISchema,
    NRSubjectUISchema,
)
from nr_metadata.documents.services.records.ui_schema import (
    NRDegreeGrantorUISchema,
    NRDocumentMetadataUISchema,
    NRDocumentRecordUISchema,
    NRThesisUISchema,
)
from nr_metadata.ui_schema.identifiers import (
    NRAuthorityIdentifierUISchema,
    NRObjectIdentifierUISchema,
    NRSystemIdentifierUISchema,
)
from oarepo_vocabularies.services.ui_schema import (
    HierarchyUISchema,
    VocabularyI18nStrUIField,
)

from oarepo_requests.schemas.marshmallow import NoneReceiverGenericRequestSchema


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


class GeoLocationsItemUISchema(NRGeoLocationUISchema):
    class Meta:
        unknown = ma.RAISE

    geoLocationPoint = ma_fields.Nested(lambda: GeoLocationPointUISchema())


class NrDocumentsMetadataUISchema(NRDocumentMetadataUISchema):
    class Meta:
        unknown = ma.RAISE

    additionalTitles = ma_fields.List(
        ma_fields.Nested(lambda: AdditionalTitlesItemUISchema())
    )

    contributors = ma_fields.List(ma_fields.Nested(lambda: ContributorsItemUISchema()))

    creators = ma_fields.List(
        ma_fields.Nested(lambda: CreatorsItemUISchema()), required=True
    )

    thesis = ma_fields.Nested(lambda: ThesisUISchema())


class NrDocumentsUISchema(NRDocumentRecordUISchema):
    class Meta:
        unknown = ma.RAISE

    syntheticFields = ma_fields.Nested(lambda: SyntheticFieldsUISchema())
    parent = ma.fields.Nested(GeneratedParentSchema)


class RelatedItemsItemUISchema(NRRelatedItemUISchema):
    class Meta:
        unknown = ma.RAISE

    itemContributors = ma_fields.List(
        ma_fields.Nested(lambda: ItemContributorsItemUISchema())
    )

    itemCreators = ma_fields.List(ma_fields.Nested(lambda: ItemCreatorsItemUISchema()))


class AccessRightsUISchema(NRAccessRightsVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class AdditionalTitlesItemUISchema(AdditionalTitlesUISchema):
    class Meta:
        unknown = ma.RAISE


class AffiliationsItemUISchema(NRAffiliationVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    hierarchy = ma_fields.Nested(lambda: HierarchyUISchema())

    title = VocabularyI18nStrUIField()


class AuthorityIdentifiersItemUISchema(NRAuthorityIdentifierUISchema):
    class Meta:
        unknown = ma.RAISE


class ContributorsItemUISchema(NRContributorUISchema):
    class Meta:
        unknown = ma.RAISE


class CountryUISchema(NRCountryVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class CreatorsItemUISchema(NRCreatorUISchema):
    class Meta:
        unknown = ma.RAISE


class DegreeGrantorsItemUISchema(NRDegreeGrantorUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    hierarchy = ma_fields.Nested(lambda: HierarchyUISchema())

    title = VocabularyI18nStrUIField()


class EventLocationUISchema(NRLocationUISchema):
    class Meta:
        unknown = ma.RAISE


class EventsItemUISchema(NREventUISchema):
    class Meta:
        unknown = ma.RAISE


class ExternalLocationUISchema(NRExternalLocationUISchema):
    class Meta:
        unknown = ma.RAISE


class FunderUISchema(NRFunderVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class FundingReferencesItemUISchema(NRFundingReferenceUISchema):
    class Meta:
        unknown = ma.RAISE


class GeoLocationPointUISchema(NRGeoLocationPointUISchema):
    class Meta:
        unknown = ma.RAISE


class ItemContributorsItemUISchema(NRRelatedItemContributorUISchema):
    class Meta:
        unknown = ma.RAISE


class ItemCreatorsItemUISchema(NRRelatedItemCreatorUISchema):
    class Meta:
        unknown = ma.RAISE


class ItemRelationTypeUISchema(NRItemRelationTypeVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class ItemResourceTypeUISchema(NRResourceTypeVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class LanguagesItemUISchema(NRLanguageVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class ObjectIdentifiersItemUISchema(NRObjectIdentifierUISchema):
    class Meta:
        unknown = ma.RAISE


class RightsItemUISchema(NRLicenseVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class RoleUISchema(NRAuthorityRoleVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class SeriesItemUISchema(NRSeriesUISchema):
    class Meta:
        unknown = ma.RAISE


class SubjectCategoriesItemUISchema(NRSubjectCategoryVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class SubjectsItemUISchema(NRSubjectUISchema):
    class Meta:
        unknown = ma.RAISE


class SyntheticFieldsUISchema(Schema):
    class Meta:
        unknown = ma.RAISE


class SystemIdentifiersItemUISchema(NRSystemIdentifierUISchema):
    class Meta:
        unknown = ma.RAISE


class ThesisUISchema(NRThesisUISchema):
    class Meta:
        unknown = ma.RAISE

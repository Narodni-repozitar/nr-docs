import marshmallow as ma
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
    NRDocumentSyntheticFieldsUISchema,
    NRThesisUISchema,
)
from nr_metadata.ui_schema.identifiers import (
    NRAuthorityIdentifierUISchema,
    NRObjectIdentifierUISchema,
    NRSystemIdentifierUISchema,
)
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_vocabularies.services.ui_schema import (
    HierarchyUISchema,
    VocabularyI18nStrUIField,
)


class DocumentsUISchema(NRDocumentRecordUISchema):
    class Meta:
        unknown = ma.RAISE

    oai = ma_fields.Nested(lambda: OaiUISchema())

    syntheticFields = ma_fields.Nested(lambda: SyntheticFieldsUISchema())

    metadata = ma_fields.Nested(lambda: DocumentsMetadataUISchema())


class DocumentsMetadataUISchema(NRDocumentMetadataUISchema):
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
    
    


class GeoLocationsItemUISchema(NRGeoLocationUISchema):
    class Meta:
        unknown = ma.RAISE

    geoLocationPoint = ma_fields.Nested(lambda: GeoLocationPointUISchema())


class OaiUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestUISchema())


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


class HarvestUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()


class InstitutionsUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    hierarchy = ma_fields.Nested(lambda: HierarchyUISchema())

    title = VocabularyI18nStrUIField()


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


class RightsUISchema(NRLicenseVocabularyUISchema):
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


class SyntheticFieldsUISchema(NRDocumentSyntheticFieldsUISchema):
    class Meta:
        unknown = ma.RAISE


class SystemIdentifiersItemUISchema(NRSystemIdentifierUISchema):
    class Meta:
        unknown = ma.RAISE


class ThesisUISchema(NRThesisUISchema):
    class Meta:
        unknown = ma.RAISE

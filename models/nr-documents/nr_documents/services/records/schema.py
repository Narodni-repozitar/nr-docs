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
from oarepo_runtime.marshmallow import BaseRecordSchema
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


class NrDocumentsSchema(
    nr_metadata.documents.services.records.schema.NRDocumentRecordSchema,
    BaseRecordSchema,
):
    class Meta:
        unknown = ma.RAISE

    metadata = ma.fields.Nested(lambda: NrDocumentsMetadataSchema())

    syntheticFields = ma.fields.Nested(lambda: SyntheticFieldsSchema())
    parent = ma.fields.Nested(GeneratedParentSchema)


class NrDocumentsMetadataSchema(
    nr_metadata.documents.services.records.schema.NRDocumentMetadataSchema,
    nr_metadata.common.services.records.schema_common.NRCommonMetadataSchema,
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

    events = ma.fields.List(ma.fields.Nested(lambda: EventsItemSchema()))

    externalLocation = ma.fields.Nested(lambda: ExternalLocationSchema())

    fundingReferences = ma.fields.List(
        ma.fields.Nested(lambda: FundingReferencesItemSchema())
    )

    geoLocations = ma.fields.List(ma.fields.Nested(lambda: GeoLocationsItemSchema()))

    objectIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: ObjectIdentifiersItemSchema())
    )

    relatedItems = ma.fields.List(ma.fields.Nested(lambda: RelatedItemsItemSchema()))

    series = ma.fields.List(ma.fields.Nested(lambda: SeriesItemSchema()))

    subjects = ma.fields.List(ma.fields.Nested(lambda: SubjectsItemSchema()))

    systemIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: SystemIdentifiersItemSchema())
    )

    thesis = ma.fields.Nested(lambda: ThesisSchema())


class RelatedItemsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRRelatedItemSchema
):
    class Meta:
        unknown = ma.RAISE

    itemContributors = ma.fields.List(
        ma.fields.Nested(lambda: ItemContributorsItemSchema())
    )

    itemCreators = ma.fields.List(ma.fields.Nested(lambda: ItemCreatorsItemSchema()))

    itemPIDs = ma.fields.List(ma.fields.Nested(lambda: ObjectIdentifiersItemSchema()))


class ContributorsItemSchema(
    nr_metadata.common.services.records.schema_common.NRContributorSchema
):
    class Meta:
        unknown = ma.RAISE

    authorityIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: AuthorityIdentifiersItemSchema())
    )


class CreatorsItemSchema(
    nr_metadata.common.services.records.schema_common.NRCreatorSchema
):
    class Meta:
        unknown = ma.RAISE

    authorityIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: AuthorityIdentifiersItemSchema())
    )


class EventsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NREventSchema
):
    class Meta:
        unknown = ma.RAISE

    eventLocation = ma.fields.Nested(lambda: EventLocationSchema(), required=True)


class GeoLocationsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRGeoLocationSchema
):
    class Meta:
        unknown = ma.RAISE

    geoLocationPoint = ma.fields.Nested(lambda: GeoLocationPointSchema())


class ItemContributorsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRRelatedItemContributorSchema
):
    class Meta:
        unknown = ma.RAISE

    authorityIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: AuthorityIdentifiersItemSchema())
    )


class ItemCreatorsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRRelatedItemCreatorSchema
):
    class Meta:
        unknown = ma.RAISE

    authorityIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: AuthorityIdentifiersItemSchema())
    )


class AccessRightsSchema(
    nr_metadata.common.services.records.schema_datatypes.NRAccessRightsVocabularySchema
):
    class Meta:
        unknown = ma.RAISE

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
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    hierarchy = ma.fields.Nested(lambda: HierarchySchema())

    title = i18n_strings


class AuthorityIdentifiersItemSchema(
    nr_metadata.schema.identifiers.NRAuthorityIdentifierSchema
):
    class Meta:
        unknown = ma.RAISE


class CountrySchema(
    nr_metadata.common.services.records.schema_datatypes.NRCountryVocabularySchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class DegreeGrantorsItemSchema(
    nr_metadata.documents.services.records.schema.NRDegreeGrantorSchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    hierarchy = ma.fields.Nested(lambda: HierarchySchema())

    title = i18n_strings


class EventLocationSchema(
    nr_metadata.common.services.records.schema_datatypes.NRLocationSchema
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
        unknown = ma.RAISE

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


class ItemRelationTypeSchema(
    nr_metadata.common.services.records.schema_datatypes.NRItemRelationTypeVocabularySchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class ItemResourceTypeSchema(
    nr_metadata.common.services.records.schema_datatypes.NRResourceTypeVocabularySchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class LanguagesItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRLanguageVocabularySchema
):
    class Meta:
        unknown = ma.RAISE

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
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class RoleSchema(
    nr_metadata.common.services.records.schema_datatypes.NRAuthorityRoleVocabularySchema
):
    class Meta:
        unknown = ma.RAISE

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
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = i18n_strings


class SubjectsItemSchema(
    nr_metadata.common.services.records.schema_datatypes.NRSubjectSchema
):
    class Meta:
        unknown = ma.RAISE


class SyntheticFieldsSchema(
    nr_metadata.documents.services.records.schema.NRDocumentSyntheticFieldsSchema
):
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

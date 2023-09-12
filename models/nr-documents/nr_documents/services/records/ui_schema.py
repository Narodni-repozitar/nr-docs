import marshmallow as ma
import nr_metadata.common.services.records.ui_schema_common
import nr_metadata.common.services.records.ui_schema_datatypes
import nr_metadata.documents.services.records.ui_schema
import nr_metadata.ui_schema.identifiers
from invenio_drafts_resources.services.records.schema import (
    ParentSchema as InvenioParentSchema,
)
from nr_metadata.ui_schema.subjects import NRSubjectListField
from oarepo_requests.schemas.marshmallow import NoneReceiverGenericRequestSchema
from oarepo_runtime.ui.marshmallow import InvenioUISchema
from oarepo_vocabularies.services.ui_schema import (
    HierarchyUISchema,
    VocabularyI18nStrUIField,
)

from nr_documents.services.records.schema import GeneratedParentSchema


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


class NrDocumentsUISchema(
    nr_metadata.documents.services.records.ui_schema.NRDocumentRecordUISchema,
    InvenioUISchema,
):
    class Meta:
        unknown = ma.RAISE

    metadata = ma.fields.Nested(lambda: NrDocumentsMetadataUISchema())

    syntheticFields = ma.fields.Nested(lambda: SyntheticFieldsUISchema())
    parent = ma.fields.Nested(GeneratedParentSchema)


class NrDocumentsMetadataUISchema(
    nr_metadata.documents.services.records.ui_schema.NRDocumentMetadataUISchema,
    nr_metadata.common.services.records.ui_schema_common.NRCommonMetadataUISchema,
):
    class Meta:
        unknown = ma.RAISE

    additionalTitles = ma.fields.List(
        ma.fields.Nested(lambda: AdditionalTitlesItemUISchema())
    )

    contributors = ma.fields.List(ma.fields.Nested(lambda: ContributorsItemUISchema()))

    creators = ma.fields.List(
        ma.fields.Nested(lambda: CreatorsItemUISchema()), required=True
    )

    events = ma.fields.List(ma.fields.Nested(lambda: EventsItemUISchema()))

    externalLocation = ma.fields.Nested(lambda: ExternalLocationUISchema())

    fundingReferences = ma.fields.List(
        ma.fields.Nested(lambda: FundingReferencesItemUISchema())
    )

    geoLocations = ma.fields.List(ma.fields.Nested(lambda: GeoLocationsItemUISchema()))

    objectIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: ObjectIdentifiersItemUISchema())
    )

    relatedItems = ma.fields.List(ma.fields.Nested(lambda: RelatedItemsItemUISchema()))

    series = ma.fields.List(ma.fields.Nested(lambda: SeriesItemUISchema()))

    subjects = NRSubjectListField(ma.fields.Nested(lambda: SubjectsItemUISchema()))

    systemIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: SystemIdentifiersItemUISchema())
    )

    thesis = ma.fields.Nested(lambda: ThesisUISchema())


class RelatedItemsItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRRelatedItemUISchema
):
    class Meta:
        unknown = ma.RAISE

    itemContributors = ma.fields.List(
        ma.fields.Nested(lambda: ItemContributorsItemUISchema())
    )

    itemCreators = ma.fields.List(ma.fields.Nested(lambda: ItemCreatorsItemUISchema()))

    itemPIDs = ma.fields.List(ma.fields.Nested(lambda: ObjectIdentifiersItemUISchema()))


class ContributorsItemUISchema(
    nr_metadata.common.services.records.ui_schema_common.NRContributorUISchema
):
    class Meta:
        unknown = ma.RAISE

    authorityIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: AuthorityIdentifiersItemUISchema())
    )


class CreatorsItemUISchema(
    nr_metadata.common.services.records.ui_schema_common.NRCreatorUISchema
):
    class Meta:
        unknown = ma.RAISE

    authorityIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: AuthorityIdentifiersItemUISchema())
    )


class EventsItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NREventUISchema
):
    class Meta:
        unknown = ma.RAISE

    eventLocation = ma.fields.Nested(lambda: EventLocationUISchema(), required=True)


class GeoLocationsItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRGeoLocationUISchema
):
    class Meta:
        unknown = ma.RAISE

    geoLocationPoint = ma.fields.Nested(lambda: GeoLocationPointUISchema())


class ItemContributorsItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRRelatedItemContributorUISchema
):
    class Meta:
        unknown = ma.RAISE

    authorityIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: AuthorityIdentifiersItemUISchema())
    )


class ItemCreatorsItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRRelatedItemCreatorUISchema
):
    class Meta:
        unknown = ma.RAISE

    authorityIdentifiers = ma.fields.List(
        ma.fields.Nested(lambda: AuthorityIdentifiersItemUISchema())
    )


class AccessRightsUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRAccessRightsVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class AdditionalTitlesItemUISchema(
    nr_metadata.common.services.records.ui_schema_common.AdditionalTitlesUISchema
):
    class Meta:
        unknown = ma.RAISE


class AffiliationsItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRAffiliationVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    hierarchy = ma.fields.Nested(lambda: HierarchyUISchema())

    title = VocabularyI18nStrUIField()


class AuthorityIdentifiersItemUISchema(
    nr_metadata.ui_schema.identifiers.NRAuthorityIdentifierUISchema
):
    class Meta:
        unknown = ma.RAISE


class CountryUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRCountryVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class DegreeGrantorsItemUISchema(
    nr_metadata.documents.services.records.ui_schema.NRDegreeGrantorUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    hierarchy = ma.fields.Nested(lambda: HierarchyUISchema())

    title = VocabularyI18nStrUIField()


class EventLocationUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRLocationUISchema
):
    class Meta:
        unknown = ma.RAISE


class ExternalLocationUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRExternalLocationUISchema
):
    class Meta:
        unknown = ma.RAISE


class FunderUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRFunderVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class FundingReferencesItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRFundingReferenceUISchema
):
    class Meta:
        unknown = ma.RAISE


class GeoLocationPointUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRGeoLocationPointUISchema
):
    class Meta:
        unknown = ma.RAISE


class ItemRelationTypeUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRItemRelationTypeVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class ItemResourceTypeUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRResourceTypeVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class LanguagesItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRLanguageVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class ObjectIdentifiersItemUISchema(
    nr_metadata.ui_schema.identifiers.NRObjectIdentifierUISchema
):
    class Meta:
        unknown = ma.RAISE


class RightsItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRLicenseVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class RoleUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRAuthorityRoleVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class SeriesItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRSeriesUISchema
):
    class Meta:
        unknown = ma.RAISE


class SubjectCategoriesItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRSubjectCategoryVocabularyUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class SubjectsItemUISchema(
    nr_metadata.common.services.records.ui_schema_datatypes.NRSubjectUISchema
):
    class Meta:
        unknown = ma.RAISE


class SyntheticFieldsUISchema(
    nr_metadata.documents.services.records.ui_schema.NRDocumentSyntheticFieldsUISchema
):
    class Meta:
        unknown = ma.RAISE


class SystemIdentifiersItemUISchema(
    nr_metadata.ui_schema.identifiers.NRSystemIdentifierUISchema
):
    class Meta:
        unknown = ma.RAISE


class ThesisUISchema(nr_metadata.documents.services.records.ui_schema.NRThesisUISchema):
    class Meta:
        unknown = ma.RAISE


class NrDocumentsDraftUISchema(InvenioUISchema):
    parent = ma.fields.Nested(GeneratedParentSchema)

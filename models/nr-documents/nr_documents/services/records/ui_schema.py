import marshmallow as ma
import nr_metadata.documents.services.records.ui_schema
from invenio_drafts_resources.services.records.schema import (
    ParentSchema as InvenioParentSchema,
)
from oarepo_requests.schemas.marshmallow import NoneReceiverGenericRequestSchema
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


class NrDocumentsMetadataUISchema(
    nr_metadata.documents.services.records.ui_schema.NRDocumentMetadataUISchema
):
    class Meta:
        unknown = ma.RAISE

    thesis = ma.fields.Nested(lambda: ThesisUISchema())

    title = ma.fields.String()


class NrDocumentsUISchema(
    nr_metadata.documents.services.records.ui_schema.NRDocumentRecordUISchema
):
    class Meta:
        unknown = ma.RAISE

    syntheticFields = ma.fields.Nested(lambda: SyntheticFieldsUISchema())
    parent = ma.fields.Nested(GeneratedParentSchema)


class DegreeGrantorsItemUISchema(
    nr_metadata.documents.services.records.ui_schema.NRDegreeGrantorUISchema
):
    class Meta:
        unknown = ma.RAISE

    _id = ma.fields.String(data_key="id", attribute="id")

    _version = ma.fields.String(data_key="@v", attribute="@v")

    hierarchy = ma.fields.Nested(lambda: HierarchyUISchema())

    title = VocabularyI18nStrUIField()


class SyntheticFieldsUISchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE


class ThesisUISchema(nr_metadata.documents.services.records.ui_schema.NRThesisUISchema):
    class Meta:
        unknown = ma.RAISE


class NrDocumentsDraftUISchema(InvenioUISchema):
    parent = ma.fields.Nested(GeneratedParentSchema)

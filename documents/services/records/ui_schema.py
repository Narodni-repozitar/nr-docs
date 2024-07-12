import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from nr_metadata.documents.services.records.ui_schema import (
    NRDocumentMetadataUISchema,
    NRDocumentRecordUISchema,
    NRDocumentSyntheticFieldsUISchema,
)
from oarepo_requests.services.ui_schema import UIRequestsSerializationMixin
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_vocabularies.services.ui_schema import (
    HierarchyUISchema,
    VocabularyI18nStrUIField,
)


class DocumentsUISchema(UIRequestsSerializationMixin, NRDocumentRecordUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataUISchema())

    oai = ma_fields.Nested(lambda: OaiUISchema())

    syntheticFields = ma_fields.Nested(lambda: SyntheticFieldsUISchema())


class OaiUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestUISchema())


class SyntheticFieldsUISchema(NRDocumentSyntheticFieldsUISchema):
    class Meta:
        unknown = ma.RAISE

    keywords = ma_fields.Nested(lambda: KeywordsUISchema())


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


class KeywordsUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    cs = ma_fields.List(ma_fields.String())

    en = ma_fields.List(ma_fields.String())

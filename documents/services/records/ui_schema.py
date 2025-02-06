import marshmallow as ma
from marshmallow import fields as ma_fields
from nr_metadata.documents.services.records.ui_schema import (
    NRDocumentMetadataUISchema,
    NRDocumentRecordUISchema,
    NRDocumentSyntheticFieldsUISchema,
)
from oarepo_requests.services.ui_schema import UIRequestsSerializationMixin
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_runtime.services.schema.ui import LocalizedDateTime
from common.services.schema import LocalizedStateField
from invenio_i18n.ext import current_i18n

from marshmallow import fields
from oarepo_vocabularies.proxies import current_ui_vocabulary_cache
from babel_edtf import format_edtf


class AccessStatusField(fields.Field):
    """Record access status."""

    def get_access_rights_vocabulary_id(
        self, access: dict, has_files: bool
    ) -> str | None:
        """Derives metadata_access_rights from access dictionary and file presence."""

        embargo_active = access.get("embargo", {}).get("active", False)
        record_access = access.get("record")
        files_access = access.get("files")
        vocabulary_id = "c_16ec"

        if embargo_active:
            vocabulary_id = "c_f1cf"
        elif record_access == "public" and not has_files:
            vocabulary_id = "c_14cb"
        elif record_access == files_access == "public":
            vocabulary_id = "c_abf2"

        return vocabulary_id

    def _serialize(self, value, attr, obj, **kwargs) -> dict | None:
        """Serialise access status."""
        record_access_dict = obj.get("access")
        _files = obj.get("files", {})
        has_files = _files is not None and _files.get("enabled", False)
        access_rights_vocabulary_id = self.get_access_rights_vocabulary_id(
            record_access_dict, has_files
        )
        access_rights_vocabulary = current_ui_vocabulary_cache.get(
            ["access-rights"]
        ).get("access-rights", None)
        embargoed_until = record_access_dict.get("embargo").get("until")
        if access_rights_vocabulary_id and access_rights_vocabulary:
            return {
                "id": access_rights_vocabulary_id,
                "title": access_rights_vocabulary.get(access_rights_vocabulary_id).get(
                    "text", ""
                ),
                "embargoedUntil": format_edtf(
                    embargoed_until, locale=current_i18n.locale
                )
                if embargoed_until
                else None,
            }


class DocumentsUISchema(UIRequestsSerializationMixin, NRDocumentRecordUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataUISchema())

    oai = ma_fields.Nested(lambda: OaiUISchema())

    # TODO: model builder seems to ignore field-class during merging of schemas,
    # need to investigate why !!!
    state = LocalizedStateField(dump_only=True)

    state_timestamp = LocalizedDateTime(dump_only=True)

    syntheticFields = ma_fields.Nested(lambda: NRDocumentSyntheticFieldsUISchema())

    access_status = AccessStatusField(attribute="access")


class OaiUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestUISchema())


class HarvestUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()

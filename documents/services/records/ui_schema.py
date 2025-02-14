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
from invenio_rdm_records.resources.serializers.ui.fields import (
    UIObjectAccessStatus as InvenioUIObjectAccessStatus,
)
from invenio_rdm_records.records.systemfields.access.field.record import (
    AccessStatusEnum,
)
from oarepo_runtime.i18n import lazy_gettext as _


# seems not possible to avoid, as they have this hardcoded in their object,
# and translation keys are i.e. open, which gets translated to otevret
class UIObjectAccessStatus(InvenioUIObjectAccessStatus):
    @property
    def title(self):
        """Access status title."""
        return {
            AccessStatusEnum.OPEN: _("access.status.open"),
            AccessStatusEnum.EMBARGOED: _("access.status.embargoed"),
            AccessStatusEnum.RESTRICTED: _("access.status.restricted"),
            AccessStatusEnum.METADATA_ONLY: _("access.status.metadata-only"),
        }.get(self.access_status)


class AccessStatusField(ma_fields.Field):
    """Record access status."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialise access status."""
        record_access_dict = obj.get("access")
        _files = obj.get("files", {})
        has_files = _files is not None and _files.get("enabled", False)
        if record_access_dict:
            record_access_status_ui = UIObjectAccessStatus(
                record_access_dict, has_files
            )
            return {
                "id": record_access_status_ui.id,
                "title_l10n": record_access_status_ui.title,
                "description_l10n": record_access_status_ui.description,
                "icon": record_access_status_ui.icon,
                "embargo_date_l10n": record_access_status_ui.embargo_date,
                "message_class": record_access_status_ui.message_class,
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

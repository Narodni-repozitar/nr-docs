from marshmallow import fields as ma_fields
from oarepo_runtime.i18n import gettext as _

class LocalizedStateField(ma_fields.String):
    def _serialize(self, value, attr, obj, **kwargs):
        ret = super()._serialize(value, attr, obj, **kwargs)
        return _(f'state:{ret}')

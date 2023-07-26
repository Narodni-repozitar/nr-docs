import marshmallow as ma
from invenio_records_resources.services.custom_fields import BaseCF
from invenio_vocabularies.services.schema import i18n_strings

"""
class HasDraftCF(BaseCF):
    @property
    def mapping(self):
        return {"type": "boolean"}

    @property
    def field(self):
        class PermissiveSchema(ma.Schema):
            class Meta:
                unknown = ma.INCLUDE

        return ma.fields.Nested(PermissiveSchema())
"""
class RelatedURICF(BaseCF):
    @property
    def mapping(self):
        """Return the mapping."""
        return {"type": "object", "dynamic": True}

    @property
    def field(self):
        """Marshmallow field for custom fields."""

        class PermissiveSchema(ma.Schema):
            class Meta:
                unknown = ma.INCLUDE

        return ma.fields.Nested(PermissiveSchema())


class NonPreferredLabelsCF(BaseCF):
    @property
    def mapping(self):
        """Return the mapping."""
        return {"type": "object", "dynamic": True}

    @property
    def field(self):
        """Marshmallow field for custom fields."""
        return ma.fields.List(i18n_strings)


class HintCF(BaseCF):
    @property
    def mapping(self):
        """Return the mapping."""
        return {"type": "object", "dynamic": True}

    @property
    def field(self):
        """Marshmallow field for custom fields."""
        return i18n_strings

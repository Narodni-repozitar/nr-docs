from flask import g
from flask_resources import BaseListSchema
from flask_resources.serializers import JSONSerializer

from oarepo_runtime.resources import (
    FilteredUIJSONSerializer,
)
from documents.services.records.ui_schema import DocumentsUISchema


class DocumentsUIJSONSerializer(FilteredUIJSONSerializer):
    """UI JSON serializer."""

    def __init__(self, **kwargs):
        base_schema_context = {"object_key": "ui", "service": "documents"}
        schema_context = (
            base_schema_context | kwargs["schema_context"]
            if "schema_context" in kwargs
            else base_schema_context
        )
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=DocumentsUISchema,
            list_schema_cls=BaseListSchema,
            schema_context=schema_context,
        )

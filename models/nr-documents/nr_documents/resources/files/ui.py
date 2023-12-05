from flask_resources import BaseListSchema
from flask_resources.serializers import JSONSerializer
from oarepo_runtime.resources import LocalizedUIJSONSerializer

from nr_documents.services.files.ui_schema import (
    NrDocumentsFileDraftUISchema,
    NrDocumentsFileUISchema,
)


class NrDocumentsFileUIJSONSerializer(LocalizedUIJSONSerializer):
    """UI JSON serializer."""

    def __init__(self):
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=NrDocumentsFileUISchema,
            list_schema_cls=BaseListSchema,
            schema_context={"object_key": "ui"},
        )


class NrDocumentsFileDraftUIJSONSerializer(LocalizedUIJSONSerializer):
    """UI JSON serializer."""

    def __init__(self):
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=NrDocumentsFileDraftUISchema,
            list_schema_cls=BaseListSchema,
            schema_context={"object_key": "ui"},
        )

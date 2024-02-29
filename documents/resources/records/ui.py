from flask import g
from flask_resources import BaseListSchema
from flask_resources.serializers import JSONSerializer
from nr_metadata.documents.services.records.ui_schema import NRDocumentRecordUISchema

from common.services.filtered_json_ui_serializer import FilteredUIJSONSerializer


class DocumentsUIJSONSerializer(FilteredUIJSONSerializer):
    """UI JSON serializer."""

    def __init__(self):
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=NRDocumentRecordUISchema,
            list_schema_cls=BaseListSchema,
            schema_context={"object_key": "ui", "identity": g.identity},
        )

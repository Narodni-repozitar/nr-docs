from flask_resources.serializers import JSONSerializer
from nr_docs_extensions.services.filtered_json_ui_serializer import FilteredUIJSONSerializer

from nr_documents.services.records.ui_schema import NrDocumentsUISchema


class NrDocumentsUIJSONSerializer(FilteredUIJSONSerializer):
    """UI JSON serializer."""

    def __init__(self):
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=NrDocumentsUISchema,
        )


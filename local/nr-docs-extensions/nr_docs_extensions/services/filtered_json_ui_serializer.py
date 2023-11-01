from flask_resources import MarshmallowSerializer
from nr_docs_extensions.services.filtered_ui_schema import FilteredUIListSchema
from oarepo_runtime.resources import LocalizedUIJSONSerializer


class FilteredUIJSONSerializer(LocalizedUIJSONSerializer):
    """UI JSON serializer."""

    def __init__(self, **kwargs):
        """Initialise Serializer."""
        super().__init__(
            **{
                **kwargs,
                'list_schema_cls': FilteredUIListSchema,
                'schema_context': {"object_key": "ui", "service": "nr_documents"},
             }
        )


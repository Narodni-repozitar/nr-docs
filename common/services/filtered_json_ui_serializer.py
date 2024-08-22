from oarepo_runtime.resources import LocalizedUIJSONSerializer

from common.services.filtered_ui_schema import FilteredUIListSchema


class FilteredUIJSONSerializer(LocalizedUIJSONSerializer):
    """UI JSON serializer."""

    def __init__(self, **kwargs):
        """Initialise Serializer."""
        base_schema_context = {"object_key": "ui", "service": "documents"}
        schema_context = (
            base_schema_context | kwargs["schema_context"]
            if "schema_context" in kwargs
            else base_schema_context
        )
        super().__init__(
            **{
                **kwargs,
                "list_schema_cls": FilteredUIListSchema,
                "schema_context": schema_context,
            }
        )

from flask import g
from flask_resources import BaseListSchema
from flask_resources.serializers import JSONSerializer
from oarepo_communities.services.record_communities.schema import (
    RecordCommunitiesSchema,
)
from oarepo_runtime.resources import LocalizedUIJSONSerializer


class DocumentsRecordCommunitiesUIJSONSerializer(LocalizedUIJSONSerializer):
    """UI JSON serializer."""

    def __init__(self):
        """Initialise Serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=RecordCommunitiesSchema,
            list_schema_cls=BaseListSchema,
            schema_context={"object_key": "ui", "identity": g.identity},
        )

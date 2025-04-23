from flask_resources import BaseListSchema, MarshmallowSerializer
from flask_resources.serializers import SimpleSerializer

from .datacite import generate_datacite
from .schema import DataciteSchema


class DataciteSerializer(MarshmallowSerializer):
    """Marshmallow based GeoJSON serializer for records."""

    def __init__(self, **options):
        """Constructor."""
        super().__init__(
            format_serializer_cls=SimpleSerializer,
            object_schema_cls=DataciteSchema,
            list_schema_cls=BaseListSchema,
            schema_kwargs={},
            encoder=generate_datacite,
        )

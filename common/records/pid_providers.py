from invenio_pidstore.providers.base import BaseProvider
from invenio_pidstore.models import PIDStatus

class ReuseNUSLMixin:
    @classmethod
    def create(cls, object_type=None, object_uuid=None, record=None, data=None, **kwargs):
        if data:
            nusl_id = cls._extract_nusl_id_from_data(data)
            if nusl_id:
                return BaseProvider.create(
                    pid_type=cls.pid_type,
                    pid_value=nusl_id,
                    object_type=object_type,
                    object_uuid=object_uuid,
                    status=PIDStatus.REGISTERED
                )
    
        return super().create(
            object_type=object_type,
            object_uuid=object_uuid,
            record=record,
            **kwargs
        )
    
    @classmethod
    def _extract_nusl_id_from_data(cls, data):
        """Extract NUSL ID from the data."""
        metadata = data.get('metadata', {})
        if not metadata:
            raise ValueError("Missing metadata.")
        
        system_identifiers = metadata.get('systemIdentifiers', [])
        for identifier in system_identifiers:
            if isinstance(identifier, dict) and identifier.get('scheme') == 'nusl':
                nusl_identifier = identifier.get('identifier')
                formatted_nusl_identifier = nusl_identifier.split("/")[-1]
                return formatted_nusl_identifier

        return None
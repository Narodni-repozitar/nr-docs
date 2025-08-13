"""
Service component that sets NUSL id as PID.
"""

from invenio_records_resources.services.records.components import ServiceComponent
from invenio_pidstore.models import PersistentIdentifier, PIDStatus

class NUSLPIDComponent(ServiceComponent):
    """
    Component that creates an additional NUSL PID alongside the existing PID.
    """
    def create(self, identity, data=None, record=None, **kwargs):
        nusl_id = self._extract_nusl_id_from_data(data)
        
        if nusl_id:
            nusl_pid = PersistentIdentifier.create(
                pid_type="nusl",
                pid_value=nusl_id,
                status=PIDStatus.REGISTERED
            )
            
            main_pid = record.pid
            nusl_pid.redirect(pid=main_pid)
    
    def _extract_nusl_id_from_data(self, data):
        """Extract NUSL ID from the data."""
        if not data:
            return None
            
        metadata = data.get('metadata', {})
        system_identifiers = metadata.get('systemIdentifiers', [])
        
        for identifier in system_identifiers:
            if isinstance(identifier, dict) and identifier.get('scheme') == 'nusl':
                nusl_url = identifier.get('identifier')
                if nusl_url and 'nusl-' in nusl_url:
                    return nusl_url.split('nusl-')[-1]
                    
        return None
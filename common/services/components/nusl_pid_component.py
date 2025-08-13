"""
Service component that sets NUSL id as PID.
"""

from invenio_records_resources.services.records.components import ServiceComponent

class NUSLPIDComponent(ServiceComponent):
    """
    NUSL PID registration component.
    """
    
    def create(self, identity, data=None, record=None, **kwargs):
        self.service.record_cls.pid.field._provider.create(record, data=data)
    
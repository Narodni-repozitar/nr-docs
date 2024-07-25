from invenio_access.permissions import system_identity
from oarepo_runtime.datastreams.types import StreamBatch
from oarepo_runtime.datastreams.writers import BaseWriter
from oarepo_runtime.datastreams.writers.service import ServiceWriter
from oarepo_runtime.datastreams.writers.attachments_service import AttachmentsServiceWriter

class CompositeWriter(BaseWriter):
    def __init__(self, *, service, identity=None):
        identity = identity or system_identity
        
        self.service = ServiceWriter(service=service, identity=identity)
        self.attachment_service = AttachmentsServiceWriter(service=service, identity=identity)
        
    def write(self, batch: StreamBatch) -> StreamBatch:
        self.service.write(batch)
        self.attachment_service.write(batch)
        return batch

from invenio_access.permissions import system_identity
from oarepo_runtime.datastreams.types import StreamBatch
from oarepo_runtime.datastreams.writers import BaseWriter

class TimestampUpdateWriter(BaseWriter):
    def __init__(self, *, service, identity=None):
        identity = identity or system_identity
        self.service = service

    def write(self, batch: StreamBatch) -> StreamBatch:
        for entry in batch.entries:
            print()
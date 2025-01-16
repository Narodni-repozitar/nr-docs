from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.uow import UnitOfWork
from sqlalchemy import Table, update

from invenio_records_resources.services.uow import RecordIndexOp
from oarepo_runtime.datastreams.types import StreamBatch, StreamEntry
from oarepo_runtime.datastreams.writers import BaseWriter
from oarepo_runtime.datastreams.writers.utils import record_invenio_exceptions 

class TimestampUpdateWriter(BaseWriter):
    def __init__(self, *, service, identity=None):
        if isinstance(service, str):
            service = current_service_registry.get(service)

        self._service = service
        self._identity = identity or system_identity

    def write(self, batch: StreamBatch) -> StreamBatch:
        with UnitOfWork() as uow:
            for entry in batch.ok_entries:
                if entry.deleted:
                    continue

                with record_invenio_exceptions(entry):
                    self._write_entry(entry, uow)

            uow.commit()
        
        db.session.commit()
        db.session.expunge_all()

    def _write_entry(self, entry: StreamEntry, uow: UnitOfWork):
        record = self._service.read(system_identity, entry.id)

        model = record._record.model
        table = Table(model.__tablename__, model.metadata)
        stmt = (
            update(table)
            .where(table.c.id == model.id)
            .values(
                updated=entry.context["oai"]["datestamp"],
                created=entry.context["oai"]["datestamp"],
            )
        )
        db.session.execute(stmt)

        record1 = self._service.read(system_identity, entry.id)

        uow.register(RecordIndexOp(record1._record, indexer=self._service.indexer, index_refresh=True))
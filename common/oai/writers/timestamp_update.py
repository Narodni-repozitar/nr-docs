from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_records_resources.proxies import current_service_registry
from sqlalchemy import Table, update

from oarepo_runtime.datastreams.types import StreamBatch
from oarepo_runtime.datastreams.writers import BaseWriter


class TimestampUpdateWriter(BaseWriter):
    def __init__(self, *, service, identity=None):
        if isinstance(service, str):
            service = current_service_registry.get(service)

        self._service = service
        self._identity = identity or system_identity

    def write(self, batch: StreamBatch) -> StreamBatch:
        for entry in batch.ok_entries:
            if entry.deleted:
                continue

            read_entry = self._service.read(system_identity, entry.id)

            model = read_entry._record.model
            table = Table(model.__tablename__, model.metadata, autoload_with=db.engine)
            stmt = (
                update(table)
                .where(table.c.id == model.id)
                .values(
                    updated=entry.context["oai"]["datestamp"],
                    created=entry.context["oai"]["datestamp"],
                )
            )
            db.session.execute(stmt)
            db.session.commit()

        db.session.expunge_all()
        self._service.reindex(
            system_identity,
            {"query": {"ids": {"values": [entry.id for entry in batch.ok_entries]}}},
        )
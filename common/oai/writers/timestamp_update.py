from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.uow import UnitOfWork
from pathlib import Path
from sqlalchemy import Table, update

from invenio_records_resources.services.uow import RecordIndexOp
from oarepo_runtime.datastreams.types import StreamBatch, StreamEntry
from oarepo_runtime.datastreams.writers import BaseWriter
from oarepo_runtime.datastreams.writers.utils import record_invenio_exceptions

class TimestampUpdateWriter(BaseWriter):
    def __init__(self, *, service, date_created_csv_path, identity=None):
        if isinstance(service, str):
            service = current_service_registry.get(service)

        self._service = service
        self._identity = identity or system_identity

        self._dates = self._try_load_dates(date_created_csv_path)

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
        datestamp = self._get_created_timestamp(entry)

        record = self._service.read(system_identity, entry.id)

        model = record._record.model
        table = Table(model.__tablename__, model.metadata)
        stmt = (
            update(table)
            .where(table.c.id == model.id)
            .values(
                updated=datestamp,
                created=datestamp,
            )
        )
        db.session.execute(stmt)

        record1 = self._service.read(system_identity, entry.id)

        uow.register(RecordIndexOp(record1._record, indexer=self._service.indexer, index_refresh=True))

    def _get_created_timestamp(self, entry: StreamEntry) -> str:
        def get_nusl_id(entry: StreamEntry) -> str:
                system_identifiers = entry.entry['metadata']['systemIdentifiers']
                nusl_id = None
                for sys_idf in system_identifiers:
                    if sys_idf["scheme"] == "nusl":
                        nusl_id = sys_idf["identifier"].split("-")[1]
                        break
                    elif sys_idf["scheme"] == "nuslOAI":
                        nusl_id = sys_idf["identifier"].split(":")[1]
                        break

                if nusl_id is None:
                    raise ValueError(f"NUSL identifier does not exist.")

                return nusl_id

        nusl_id = get_nusl_id(entry)
        if nusl_id not in self._dates:
            raise KeyError(f"Date not found for identifier {nusl_id}")
        return self._dates[nusl_id]
    
    def _try_load_dates(self, path) -> None:
        csv_path = Path(path)
        if not csv_path.exists():
            raise ValueError(f"CSV file not found at: '{csv_path}'")
        if not csv_path.is_file():
            raise ValueError(f"Path exists but is not a file: '{csv_path}'")

        dates = {}
        try:
            with csv_path.open('r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        line = line.strip()
                        if not line:
                            continue
                        if ',' not in line:
                            raise ValueError(f"Invalid CSV format at line {line_num}: missing comma separator")
                        
                        identifier, date = line.split(',', 1)
                        identifier = identifier.strip()
                        date = date.strip()
                        
                        if not identifier or not date:
                            raise ValueError(f"Invalid CSV format at line {line_num}: empty identifier or date")
                        
                        dates[identifier] = f"{date}T00:00:00+00:00"
                        
                    except ValueError as e:
                        raise ValueError(f"Error processing CSV at line {line_num}: {str(e)}")
                    
        except (IOError, UnicodeDecodeError) as e:
            raise RuntimeError(f"Failed to read CSV file: {str(e)}")
        
        return dates
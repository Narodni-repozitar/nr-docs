import csv
from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.uow import UnitOfWork
import requests
from sqlalchemy import Table, update
from typing import Dict

from invenio_records_resources.services.uow import RecordIndexOp
from oarepo_runtime.datastreams.types import StreamBatch, StreamEntry
from oarepo_runtime.datastreams.writers import BaseWriter
from oarepo_runtime.datastreams.writers.utils import record_invenio_exceptions
from io import StringIO

class TimestampUpdateWriter(BaseWriter):
    def __init__(self, *, service, date_created_csv_url, identity=None):
        if isinstance(service, str):
            service = current_service_registry.get(service)

        self._service = service
        self._identity = identity or system_identity

        self._dates = self._load_dates(date_created_csv_url)

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
    
    def _load_dates(self, url: str) -> Dict[str, str]:
        """Load dates from a GitHub raw content URL"""
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL provided: {url}. Please provide a full URL starting with http:// or https://")
        
        dates = {}
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            csv_content = StringIO(response.text)
            reader = csv.reader(csv_content)
            
            for line_num, row in enumerate(reader, 1):
                if len(row) >= 2:
                    identifier, date = row[0], row[1]
                    if identifier and date:
                        dates[identifier.strip()] = f"{date.strip()}T00:00:00+00:00"
                        
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch CSV from URL {url}: {str(e)}")
        except csv.Error as e:
            raise ValueError(f"Error processing CSV at line {line_num}: {str(e)}")
        
        if not dates:
            raise ValueError(f"No valid date entries found in CSV from {url}")
        
        return dates
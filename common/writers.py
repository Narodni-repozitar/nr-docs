import functools
from typing import Union

from invenio_db import db
from invenio_records_resources.proxies import current_service_registry
from invenio_vocabularies.contrib.awards.models import AwardsMetadata
from invenio_vocabularies.contrib.funders.models import FundersMetadata
from invenio_vocabularies.contrib.names.models import NamesMetadata
from oarepo_runtime.datastreams.types import StreamBatch
from oarepo_runtime.datastreams.writers import BaseWriter


class AwardsWriter(BaseWriter):
    """Optimized writer for awards."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def write(self, batch: StreamBatch) -> Union[StreamBatch, None]:
        """Writes the input entry to the target output.
        :returns: nothing
                  Raises WriterException in case of errors.
        """
        awards_service = current_service_registry.get("awards")

        uuids = []
        for entry in batch.ok_entries:
            payload = entry.entry
            stored = AwardsMetadata.query.filter_by(pid=payload["id"]).first()
            if stored:
                entry.id = payload["id"]
                uuids.append(stored.id)
                continue

            pid = payload.pop("id")
            if "funder" in payload:
                funder_id = payload["funder"].get("id")
                payload["funder"]["name"] = self.lookup_funder_name(funder_id)
            award = AwardsMetadata(pid=pid, json=payload)
            db.session.add(award)
            entry.id = award.pid

            uuids.append(award.id)

        db.session.commit()
        awards_service.indexer.bulk_index(uuids)

        return batch

    def finish(self):
        pass

    @functools.lru_cache(maxsize=1024)
    def lookup_funder_name(self, funder_id):
        """Lookup funder name by id."""
        funder = FundersMetadata.query.filter_by(pid=funder_id).one()
        return funder.json["name"]


class NamesWriter(BaseWriter):
    """Optimized writer for names."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def write(self, batch: StreamBatch) -> Union[StreamBatch, None]:
        """Writes the input entry to the target output.
        :returns: nothing
                  Raises WriterException in case of errors.
        """
        names_service = current_service_registry.get("names")

        uuids = []
        for entry in batch.ok_entries:
            payload = entry.entry
            if "affiliations" in payload:
                raise Exception("Affiliations are not supported in this writer")
            stored = NamesMetadata.query.filter_by(pid=payload["id"]).first()
            if stored:
                entry.id = payload["id"]
                uuids.append(stored.id)
                continue

            pid = payload.pop("id")
            name = NamesMetadata(pid=pid, json=payload)
            db.session.add(name)
            entry.id = name.pid
            uuids.append(name.id)

        db.session.commit()
        names_service.indexer.bulk_index(uuids)

        return batch

    def finish(self):
        pass

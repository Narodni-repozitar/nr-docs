from invenio_access.permissions import system_identity
from invenio_communities.communities.records.models import CommunityMetadata
from invenio_communities.members.records.models import MemberModel
from invenio_db import db
from invenio_records_resources.proxies import current_service_registry
from oarepo_runtime.datastreams.types import StreamBatch, StreamEntry
from oarepo_runtime.datastreams.writers import BaseWriter
from oarepo_runtime.datastreams.writers.utils import record_invenio_exceptions
from sqlalchemy import Table, and_, select, update


class OwnershipWriter(BaseWriter):
    def __init__(self, *, service, identity=None):
        if isinstance(service, str):
            service = current_service_registry.get(service)

        self._service = service
        self._identity = identity or system_identity

    def write(self, batch: StreamBatch) -> StreamBatch:
        for entry in batch.ok_entries:
            if entry.deleted:
                continue

            with record_invenio_exceptions(entry):
                self._write_entry(entry)

    def _write_entry(self, entry: StreamEntry):
        record = self._service.read(system_identity, entry.id)
        record_communities = self._find_record_communities(record)
        communities_owners = [
            self._find_community_owner(community[0]) for community in record_communities
        ]
        self._add_owners(record, communities_owners)

    def _find_record_communities(self, record):
        communities_ids = record._record.parent.communities.ids
        stmt = select(CommunityMetadata).where(
            CommunityMetadata.id.in_(communities_ids)
        )
        record_communities_result = db.session.execute(stmt)
        return record_communities_result.fetchall()

    def _find_community_owner(self, community):
        stmt = select(MemberModel).where(
            and_(MemberModel.community_id == community.id, MemberModel.role == "owner")
        )
        community_members_result = db.session.execute(stmt)
        return community_members_result.fetchone()

    def _add_owners(self, record, owners):
        parent_model = record._record.parent.model
        table = Table(parent_model.__tablename__, parent_model.metadata)
        
        result = db.session.execute(
            select(table.c.json).where(table.c.id == parent_model.id)
        ).scalar_one()
        
        owned_by = None
        if owners and len(owners) > 0:
            owned_by = owners[0].user_id
        current_json = dict(result) if result else {}
        if 'access' not in current_json:
            current_json['access'] = {}
        current_json['access']['owned_by'] = owned_by
        
        stmt = (
            update(table)
            .where(table.c.id == parent_model.id)
            .values(json=current_json)
        )
        
        db.session.execute(stmt)
        db.session.commit()

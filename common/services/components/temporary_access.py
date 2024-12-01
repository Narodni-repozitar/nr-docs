"""
Temporary implementation of RDM access field.
"""

from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_rdm_records.records.systemfields.access.field.record import RecordAccess


class TemporaryAccessComponent(ServiceComponent):
    def create(self, identity, **kwargs):
        self._set_access(identity, **kwargs)

    def update(self, identity, **kwargs):
        self._set_access(identity, **kwargs)

    def update_draft(self, identity, **kwargs):
        self._set_access(identity, **kwargs)

    def _set_access(self, identity, *, data, record, **kwargs):
        metadata_access_rights = (
            data.get("metadata", {}).get("accessRights", {}).get("id", None)
        )
        if not metadata_access_rights:
            return
        access: RecordAccess = record.access
        print("metadata access rights", metadata_access_rights)
        match metadata_access_rights:
            case "c_abf2":  # open access
                access.embargo.active = False
                access.protection.record = "public"
                access.protection.files = "public"
            case "c_f1cf":  # embargo
                access.embargo.active = True
                access.protection.record = "public"
                access.protection.files = "restricted"
            case "c_16ec":  # restricted access
                access.embargo.active = False
                access.protection.record = "restricted"
                access.protection.files = "restricted"
            case "c_14cb":  # metadata only
                access.embargo.active = False
                access.protection.record = "public"
                access.protection.files = "restricted"

        print("Access", access.protection.record, access.protection.files)

    def publish(self, identity, draft=None, record=None):
        record.access.protection.record = draft.access.protection.record
        record.access.protection.files = draft.access.protection.files
        record.access.embargo.active = draft.access.embargo.active

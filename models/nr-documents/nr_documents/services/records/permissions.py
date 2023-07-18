from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess


class NrDocumentsPermissionPolicy(RecordPermissionPolicy):
    """nr_documents.records.api.NrDocumentsRecord permissions."""

    """nr_documents.records.api.NrDocumentsRecord permissions.
        Values in this class will override permission presets.
    """

    can_search = [SystemProcess(), AnyUser()]
    can_read = [SystemProcess(), AnyUser()]
    can_create = [SystemProcess()]
    can_update = [SystemProcess()]
    can_delete = [SystemProcess()]
    can_manage = [SystemProcess()]

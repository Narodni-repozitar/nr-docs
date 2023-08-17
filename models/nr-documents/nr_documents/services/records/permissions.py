from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess


class NrDocumentsPermissionPolicy(RecordPermissionPolicy):
    """nr_documents.records.api.NrDocumentsRecord permissions."""

    can_search = [SystemProcess(), AnyUser()]
    can_read = [SystemProcess(), AnyUser()]
    can_create = [SystemProcess(), AnyUser()]
    can_update = [SystemProcess(), AnyUser()]
    can_delete = [SystemProcess(), AnyUser()]
    can_manage = [SystemProcess(), AnyUser()]

from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    SystemProcess,
)
from oarepo_runtime.services.generators import RecordOwners


class NRDocsPermissionPolicy(RecordPermissionPolicy):
    """record policy for read only repository"""

    can_search = [SystemProcess(), AuthenticatedUser()]
    can_read = [SystemProcess(), AuthenticatedUser()]
    can_create = [SystemProcess(), AuthenticatedUser()]
    can_update = [SystemProcess()]
    can_delete = [SystemProcess()]
    can_manage = [SystemProcess()]

    can_create_files = [SystemProcess()]
    can_set_content_files = [SystemProcess()]
    can_get_content_files = [SystemProcess(), AuthenticatedUser()]
    can_commit_files = [SystemProcess()]
    can_read_files = [SystemProcess(), AuthenticatedUser()]
    can_update_files = [SystemProcess()]
    can_delete_files = [SystemProcess()]

    can_edit = [SystemProcess(), RecordOwners()]
    can_new_version = [SystemProcess(), RecordOwners()]
    can_search_drafts = [SystemProcess(), RecordOwners()]
    can_read_draft = [SystemProcess(), RecordOwners()]
    can_update_draft = [SystemProcess(), RecordOwners()]
    can_delete_draft = [SystemProcess(), RecordOwners()]
    can_publish = [SystemProcess(), RecordOwners()]
    can_draft_create_files = [SystemProcess(), RecordOwners()]
    can_draft_set_content_files = [SystemProcess(), RecordOwners()]
    can_draft_get_content_files = [SystemProcess(), RecordOwners()]
    can_draft_commit_files = [SystemProcess(), RecordOwners()]
    can_draft_read_files = [SystemProcess(), RecordOwners()]
    can_draft_update_files = [SystemProcess(), RecordOwners()]

    can_add_community = [SystemProcess(), AuthenticatedUser()]
    can_remove_community = [SystemProcess(), AuthenticatedUser()]
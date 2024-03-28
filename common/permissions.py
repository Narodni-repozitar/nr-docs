from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    SystemProcess,
)
from oarepo_runtime.services.generators import RecordOwners


class NRDocsPermissionPolicy(RecordPermissionPolicy):
    """record policy for read only repository"""

    can_search = [AuthenticatedUser()]
    can_read = [AnyUser()]
    can_create = [AuthenticatedUser()]
    can_update = [AuthenticatedUser()]
    can_delete = [AuthenticatedUser()]
    can_manage = [AuthenticatedUser()]

    can_create_files = [AuthenticatedUser()]
    can_set_content_files = [AuthenticatedUser()]
    can_get_content_files = [AnyUser()]
    can_commit_files = [AuthenticatedUser()]
    can_read_files = [AnyUser()]
    can_update_files = [AuthenticatedUser()]
    can_delete_files = [AuthenticatedUser()]

    can_edit = [RecordOwners()]
    can_new_version = [RecordOwners()]
    can_search_drafts = [AuthenticatedUser()]
    can_read_draft = [RecordOwners()]
    can_update_draft = [RecordOwners()]
    can_delete_draft = [RecordOwners()]
    can_publish = [RecordOwners()]
    can_draft_create_files = [RecordOwners()]
    can_draft_set_content_files = [RecordOwners()]
    can_draft_get_content_files = [RecordOwners()]
    can_draft_commit_files = [RecordOwners()]
    can_draft_read_files = [RecordOwners()]
    can_draft_update_files = [RecordOwners()]

    can_add_community = [AuthenticatedUser()]
    can_remove_community = [AuthenticatedUser()]
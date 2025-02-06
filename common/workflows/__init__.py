from oarepo_communities.services.permissions.policy import (
    CommunityWorkflowPermissionPolicy,
)
from invenio_records_permissions.generators import (
    AnyUser,
)


class DocsCommunitiesPermissionPreset(CommunityWorkflowPermissionPolicy):
    can_manage_record_access = [AnyUser()]

from oarepo_requests.services.permissions.workflow_policies import (
    CreatorsFromWorkflowRequestsPermissionPolicy,
)
from oarepo_runtime.services.generators import UserWithRole


class NrDocsRequestsPermissionPolicy(CreatorsFromWorkflowRequestsPermissionPolicy):
    can_action_accept = (
        CreatorsFromWorkflowRequestsPermissionPolicy.can_action_accept
        + [UserWithRole("request_manager")]
    )
    can_action_decline = (
        CreatorsFromWorkflowRequestsPermissionPolicy.can_action_decline
        + [UserWithRole("request_manager")]
    )
    can_read = CreatorsFromWorkflowRequestsPermissionPolicy.can_read + [
        UserWithRole("request_manager"),
    ]

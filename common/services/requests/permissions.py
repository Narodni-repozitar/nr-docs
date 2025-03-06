from oarepo_workflows.requests.permissions import CreatorsFromWorkflowRequestsPermissionPolicy
from invenio_communities.members.services.request import CommunityInvitation

from invenio_records_permissions.generators import SystemProcess
from invenio_requests.customizations.event_types import CommentEventType, LogEventType
from invenio_requests.services.generators import Creator, Receiver
from invenio_requests.services.permissions import (
    PermissionPolicy as InvenioRequestsPermissionPolicy,
)

from oarepo_workflows.requests.generators.conditionals import IfEventType, IfRequestType
from oarepo_workflows.requests.generators.workflow_based import (
    EventCreatorsFromWorkflow,
    RequestCreatorsFromWorkflow,
)
from invenio_requests.services.permissions import PermissionPolicy as InvenioRequestsPermissionPolicy

class RequestsPermissionPolicy(CreatorsFromWorkflowRequestsPermissionPolicy):
    can_create = [
        SystemProcess(),
        RequestCreatorsFromWorkflow(),
        IfRequestType(
            [CommunityInvitation.type_id], InvenioRequestsPermissionPolicy.can_create
        )
    ]
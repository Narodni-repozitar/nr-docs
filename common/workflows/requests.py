import operator
from functools import reduce

from invenio_records_permissions.generators import ConditionalGenerator
from oarepo_requests.services.permissions.workflow_policies import (
    CreatorsFromWorkflowRequestsPermissionPolicy,
)
from oarepo_runtime.services.permissions import UserWithRole
from opensearch_dsl.query import MatchNone, Terms


class RequestTypeFilter(ConditionalGenerator):
    def __init__(self, request_types, then_, else_):
        super().__init__(then_, else_)
        self.request_types = request_types

    def _condition(self, request=None, **kwargs):
        """Condition to choose generators set."""
        return request.type.type_id in self.request_types

    def query_filter(self, **kwargs):
        then_filters = (
            reduce(operator.or_, (x.query_filter(**kwargs) for x in self.then_))
            if self.then_
            else MatchNone()
        )
        else_filters = (
            reduce(operator.or_, (x.query_filter(**kwargs) for x in self.else_))
            if self.else_
            else MatchNone()
        )
        return (
            Terms(type=self.request_types) & then_filters
            | ~Terms(type=self.request_types) & else_filters
        )


request_managers = [
    RequestTypeFilter(
        ["aai-community-invitation"], then_=[], else_=[UserWithRole("request_manager")]
    )
]


class NrDocsRequestsPermissionPolicy(CreatorsFromWorkflowRequestsPermissionPolicy):
    can_action_accept = (
        CreatorsFromWorkflowRequestsPermissionPolicy.can_action_accept
        + request_managers
    )
    can_action_decline = (
        CreatorsFromWorkflowRequestsPermissionPolicy.can_action_decline
        + request_managers
    )
    can_read = CreatorsFromWorkflowRequestsPermissionPolicy.can_read + request_managers
    can_create_comment = (
        CreatorsFromWorkflowRequestsPermissionPolicy.can_create_comment
        + request_managers
    )

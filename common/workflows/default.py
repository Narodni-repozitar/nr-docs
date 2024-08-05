from datetime import timedelta
from oarepo_workflows import (
    Workflow,
    WorkflowPermissionPolicy,
    WorkflowRequestPolicy,
    IfInState,
    WorkflowRequest,
    WorkflowTransitions,
    AutoApprove,
    WorkflowRequestEscalation,
)

# from oarepo_requests.services.permissions import IfRequestedBy
from oarepo_runtime.services.permissions import UserWithRole, RecordOwners
from invenio_communities.permissions import IfRestricted, CommunityMembers
# from oarepo_communities.services.permissions import CommunityRole

from invenio_records_permissions.generators import AnyUser

#
# Roles within the workflow:
#
# administrator == supercurator, NTK staff
#
# Community roles:
#
# CommunityRole("editor") == people who can create new records
# CommunityRole("curator") == people who can publish records and remove them
# CommunityMembers() == member of the community
#
# Synthetic roles:
#
# RecordOwners() == actual owner of the record (person who created it)
#
#
# Record states:
#
# draft == record is being created
# submitted == record is submitted for approval/publishing but not yet approved
# published == record is published
# deleting == record is in the process of being deleted (request filed but not yet approved)
#

# TODO: will be removed when communities are merged
CommunityRole = UserWithRole


class DefaultWorkflowPermissions(WorkflowPermissionPolicy):
    """Permissions for the default nr-docs workflow."""
    can_create = [
        CommunityRole("editor"),
    ]

    can_read = [
        RecordOwners(),
        # curator can see the record in any state
        CommunityRole("curator"),
        # administrator can see everything
        UserWithRole("administrator"),
        # if the record is published and restricted, only members of the community can see it,
        # otherwise, any user can see it
        IfInState(
            "published",
            then_=[
                IfRestricted(
                    "visibility",
                    then_=[CommunityMembers()],
                    else_=[AnyUser()],
                )
            ],
        ),

        IfInState("retracting", then_=[RecordOwners(), CommunityRole("curator")]),
    ]

    can_update = [
        IfInState(
            "draft",
            then_=[
                RecordOwners(),
                CommunityRole("curator"),
                UserWithRole("administrator"),
            ],
        ),
        # if not draft, can not be directly updated by any means, must use request
    ]

    can_delete = [
        # draft can be deleted, published record must be deleted via request
        IfInState(
            "draft",
            then_=[
                RecordOwners(),
                CommunityRole("curator"),
                UserWithRole("administrator"),
            ],
        ),
    ]


class DefaultWorkflowRequests(WorkflowRequestPolicy):
    """Requests for the default nr-docs workflow."""
    # TODO: will be uncommented when oarepo-requests are merged
    #
    # publish_request = WorkflowRequest(
    #     # if the record is in draft state, the owner or curator can request publishing
    #     requesters=[
    #         IfInState("draft", then_=[RecordOwners(), CommunityRole("curator")])
    #     ],
    #     recipients=[
    #         # if the requester is the curator of the community, auto approve the request
    #         IfRequestedBy(
    #             CommunityRole("curator"),
    #             then_=[AutoApprove()],
    #             else_=[CommunityRole("curator")],
    #         )
    #     ],
    #     transitions=WorkflowTransitions(
    #         submitted="submitted", accepted="published", declined="draft"
    #     ),
    #     # if the request is not resolved in 14 days, escalate it to the administrator
    #     escalations=[
    #         WorkflowRequestEscalation(
    #             after=timedelta(days=14), recipients=[UserWithRole("administrator")]
    #         )
    #     ],
    # )
    #
    # edit_request = WorkflowRequest(
    #     requesters=[
    #         IfInState("published", then_=[RecordOwners(), CommunityRole("curator")])
    #     ],
    #     # the request is auto-approve, we do not limit the owner of the record to create a new
    #     # draft version. It will need to be approved by the curator though.
    #     recipients=[AutoApprove()],
    # )
    #
    # delete_request = WorkflowRequest(
    #     # if the record is draft, it is covered by the delete permission
    #     # if published, only the owner or curator can request deleting
    #     requesters=[
    #         IfInState(
    #             "published",
    #             then_=[
    #                 RecordOwners(),
    #                 CommunityRole("curator"),
    #                 UserWithRole("administrator"),
    #             ],
    #         )
    #     ],
    #     # if the requester is the curator of the community, auto approve the request,
    #     # otherwise, the request is sent to the curator
    #     recipients=[
    #         IfRequestedBy(
    #             CommunityRole("curator"),
    #             then_=[AutoApprove()],
    #             else_=[CommunityRole("curator")],
    #         )
    #     ],
    #
    #     # the record comes to the state of retracting when the request is submitted. If the request
    #     # is approved, the record is deleted, if rejected, it is published again.
    #     transitions=WorkflowTransitions(submitted="retracting", declined="published", accepted="deleted"),
    #
    #     # if the request is not resolved in 14 days, escalate it to the administrator
    #     escalations=[
    #         WorkflowRequestEscalation(
    #             after=timedelta(days=14), recipients=[UserWithRole("administrator")]
    #         )
    #     ],
    # )
    #
    # assign_doi = WorkflowRequest(
    #     requesters=[
    #         RecordOwners(),
    #         CommunityRole("curator"),
    #         UserWithRole("administrator"),
    #     ],
    #     recipients=[
    #         IfRequestedBy(
    #             UserWithRole("administrator"),
    #             then_=[AutoApprove()],
    #             else_=[CommunityRole("curator")],
    #         )
    #     ],
    #     escalations=[
    #         WorkflowRequestEscalation(
    #             after=timedelta(days=14), recipients=[UserWithRole("administrator")]
    #         )
    #     ],
    # )


class DefaultWorkflow(Workflow):
    label = (_("Default nr-docs workflow"),)
    permission_policy_cls = DefaultWorkflowPermissions
    request_policy_cls = DefaultWorkflowRequests

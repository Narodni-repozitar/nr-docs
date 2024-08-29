#
# Roles within the workflow:
#
# administrator == supercurator, NTK staff
#
# Community roles:
#
# CommunityRole("submitter") == people who can create new records
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
# submitted == record is submitted for approval/publishing but not yet accepted
# published == record is published
# deleting == record is in the process of being deleted (request filed but not yet accepted)
#

from datetime import timedelta

from invenio_records_permissions.generators import AnyUser
from oarepo_communities.services.permissions.generators import (
    CommunityRole,
    PrimaryCommunityRole,
    PrimaryCommunityMembers,
)
from oarepo_communities.services.permissions.policy import CommunityDefaultWorkflowPermissions
from oarepo_requests.services.permissions.generators import IfRequestedBy, RequestActive
from oarepo_runtime.services.permissions.generators import RecordOwners, UserWithRole
from oarepo_workflows import (
    AutoApprove,
    IfInState,
    WorkflowRequest,
    WorkflowRequestEscalation,
    WorkflowRequestPolicy,
    WorkflowTransitions,
)
from oarepo_requests.services.permissions.workflow_policies import RequestBasedWorkflowPermissions


class DefaultWorkflowPermissions(CommunityDefaultWorkflowPermissions):
    can_create = [
        PrimaryCommunityRole("submitter"),
        PrimaryCommunityRole("curator"),
        UserWithRole("administrator"),
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
            then_=[AnyUser()],
            # then_=[
            #     IfRestricted( # todo - crashes on missing parent access field now
            #         "visibility",
            #         then_=[CommunityMembers()],
            #         else_=[AnyUser()],
            #     )
            # ],
        ),
        # every member of the community can see the metadata of the drafts, but not the files
        IfInState(
            "draft",
            then_=[PrimaryCommunityMembers()],
        ),
    ]

    can_update = [
        IfInState(
            "draft",
            then_=[
                RecordOwners(),
                PrimaryCommunityRole("curator"),
                UserWithRole("administrator"),
            ],
        ),
        # if not draft, can not be directly updated by any means, must use request
        IfInState(
            "submitted",
            then_=[
                PrimaryCommunityRole("curator"),
                UserWithRole("administrator"),
            ],
        ),
    ]

    can_delete = [
        # draft can be deleted, published record must be deleted via request
        IfInState(
            "draft",
            then_=[
                RecordOwners(),
                PrimaryCommunityRole("curator"),
                UserWithRole("administrator"),
            ],
        ),
    ] + CommunityDefaultWorkflowPermissions.can_delete


class DefaultWorkflowRequests(WorkflowRequestPolicy):
    publish_draft = WorkflowRequest(
        # if the record is in draft state, the owner or curator can request publishing
        requesters=[
            IfInState("draft", then_=[RecordOwners(), PrimaryCommunityRole("curator")])
        ],
        recipients=[
            # if the requester is the curator of the community, auto approve the request
            IfRequestedBy(
                requesters=PrimaryCommunityRole("curator"),
                then_=[AutoApprove()],
                else_=[PrimaryCommunityRole("curator")],
            )
        ],
        transitions=WorkflowTransitions(
            submitted="submitted", accepted="published", declined="draft"
        ),
        # if the request is not resolved in 21 days, escalate it to the administrator
        escalations=[
            WorkflowRequestEscalation(
                after=timedelta(days=21), recipients=[UserWithRole("administrator")]
            )
        ],
    )

    edit_published_record = WorkflowRequest(
        requesters=[
            IfInState(
                "published",
                then_=[
                    RecordOwners(),
                    PrimaryCommunityRole("curator"),
                    UserWithRole("administrator"),
                ],
            )
        ],
        # the request is auto-approve, we do not limit the owner of the record to create a new
        # draft version. It will need to be accepted by the curator though.
        recipients=[AutoApprove()],
    )

    new_version = WorkflowRequest(
        requesters=[
            IfInState(
                "published",
                then_=[
                    RecordOwners(),
                    PrimaryCommunityRole("curator"),
                    UserWithRole("administrator"),
                ],
            )
        ],
        # the request is auto-approve, we do not limit the owner of the record to create a new
        # draft version. It will need to be accepted by the curator though.
        recipients=[AutoApprove()],
    )

    delete_published_record = WorkflowRequest(
        # if the record is draft, it is covered by the delete permission
        # if published, only the owner or curator can request deleting
        requesters=[
            IfInState(
                "published",
                then_=[
                    RecordOwners(),
                    PrimaryCommunityRole("curator"),
                    UserWithRole("administrator"),
                ],
            )
        ],
        # if the requester is the curator of the community or administrator, auto approve the request,
        # otherwise, the request is sent to the curator
        recipients=[
            IfRequestedBy(
                requesters=[PrimaryCommunityRole("curator"), UserWithRole("administrator")],
                then_=[AutoApprove()],
                else_=[PrimaryCommunityRole("curator")],
            )
        ],
        # the record comes to the state of retracting when the request is submitted. If the request
        # is accepted, the record is deleted, if declined, it is published again.
        transitions=WorkflowTransitions(
            submitted="retracting", declined="published", accepted="deleted"
        ),
        # if the request is not resolved in 21 days, escalate it to the administrator
        escalations=[
            WorkflowRequestEscalation(
                after=timedelta(days=21), recipients=[UserWithRole("administrator")]
            )
        ],
    )

    assign_doi = WorkflowRequest(
        requesters=[
            RecordOwners(),
            PrimaryCommunityRole("curator"),
            UserWithRole("administrator"),
        ],
        recipients=[
            IfRequestedBy(
                requesters=[PrimaryCommunityRole("curator"), UserWithRole("administrator")],
                then_=[AutoApprove()],
                else_=[PrimaryCommunityRole("curator")],
            )
        ],
        escalations=[
            WorkflowRequestEscalation(
                after=timedelta(days=21), recipients=[UserWithRole("administrator")]
            )
        ],
    )

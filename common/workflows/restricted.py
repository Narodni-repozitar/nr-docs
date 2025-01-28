from datetime import timedelta

from invenio_rdm_records.services.generators import IfRestricted, IfDraft
from invenio_records_permissions.generators import AnyUser, Disable
from oarepo_communities.services.permissions.generators import (
    CommunityRole,
    PrimaryCommunityMembers,
    PrimaryCommunityRole,
)
from oarepo_communities.services.permissions.policy import (
    CommunityDefaultWorkflowPermissions,
)
from oarepo_requests.services.permissions.generators import IfRequestedBy
from oarepo_runtime.services.permissions.generators import RecordOwners
from oarepo_workflows import (
    AutoApprove,
    IfInState,
    WorkflowRequest,
    WorkflowRequestEscalation,
    WorkflowRequestPolicy,
    WorkflowTransitions,
)
from invenio_i18n import lazy_gettext as _


class RestrictedWorkflowPermissions(CommunityDefaultWorkflowPermissions):
    can_create = [
        PrimaryCommunityRole("submitter"),
        PrimaryCommunityRole("owner"),
        PrimaryCommunityRole("curator"),
    ]

    can_read_generic = [
        RecordOwners(),
        CommunityRole("curator"),
        CommunityRole("owner"),
        IfInState(
            "draft",
            then_=[PrimaryCommunityMembers()],
        ),
    ]

    can_read = can_read_generic + [
        IfInState(
            "published",
            then_=[
                IfRestricted(
                    "record",
                    then_=[PrimaryCommunityMembers()],
                    else_=[AnyUser()],
                )
            ],
        ),
    ]

    # Restricted files are accessible only to the record owner, curator, and community owner
    can_read_files = can_read_generic + [
        IfInState(
            "published",
            then_=[
                IfRestricted(
                    "files",
                    then_=[
                        RecordOwners(),
                        CommunityRole("curator"),
                        CommunityRole("owner"),
                    ],
                    else_=[AnyUser()],
                )
            ],
        ),
    ]

    can_list_files = can_read_files

    can_get_content_files = can_read_files

    can_update = [
        IfInState(
            "draft",
            then_=[
                RecordOwners(),
                PrimaryCommunityRole("curator"),
                PrimaryCommunityRole("owner"),
            ],
        ),
        IfInState(
            "submitted",
            then_=[
                PrimaryCommunityRole("curator"),
                PrimaryCommunityRole("owner"),
            ],
        ),
    ]

    can_delete = [
        IfInState(
            "draft",
            then_=[
                RecordOwners(),
                PrimaryCommunityRole("curator"),
                PrimaryCommunityRole("owner"),
            ],
        ),
    ] + CommunityDefaultWorkflowPermissions.can_delete

    can_manage_files = [
        Disable(),
    ]


class RestrictedWorkflowRequests(WorkflowRequestPolicy):
    publish_draft = WorkflowRequest(
        requesters=[
            IfInState("draft", then_=[RecordOwners(), PrimaryCommunityRole("curator")])
        ],
        recipients=[
            IfRequestedBy(
                requesters=[
                    PrimaryCommunityRole("curator"),
                    PrimaryCommunityRole("owner"),
                ],
                then_=[AutoApprove()],
                else_=[PrimaryCommunityRole("curator"), PrimaryCommunityRole("owner")],
            )
        ],
        transitions=WorkflowTransitions(
            submitted="submitted",
            accepted="published",
            declined="draft",
            cancelled="draft",
        ),
        escalations=[
            WorkflowRequestEscalation(
                after=timedelta(days=21),
                recipients=[
                    PrimaryCommunityRole("owner"),
                ],
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
                    PrimaryCommunityRole("owner"),
                ],
            )
        ],
        recipients=[AutoApprove()],
    )

    new_version = WorkflowRequest(
        requesters=[
            IfInState(
                "published",
                then_=[
                    RecordOwners(),
                    PrimaryCommunityRole("curator"),
                    PrimaryCommunityRole("owner"),
                ],
            )
        ],
        recipients=[AutoApprove()],
    )

    delete_published_record = WorkflowRequest(
        requesters=[
            IfInState(
                "published",
                then_=[
                    RecordOwners(),
                    PrimaryCommunityRole("curator"),
                    PrimaryCommunityRole("owner"),
                ],
            )
        ],
        recipients=[
            IfRequestedBy(
                requesters=[
                    PrimaryCommunityRole("curator"),
                    PrimaryCommunityRole("owner"),
                ],
                then_=[AutoApprove()],
                else_=[PrimaryCommunityRole("curator")],
            )
        ],
        transitions=WorkflowTransitions(
            submitted="retracting",
            declined="published",
            accepted="deleted",
            cancelled="published",
        ),
        escalations=[
            WorkflowRequestEscalation(
                after=timedelta(days=21),
                recipients=[
                    PrimaryCommunityRole("owner"),
                ],
            )
        ],
    )

    assign_doi = WorkflowRequest(
        requesters=[
            RecordOwners(),
            PrimaryCommunityRole("curator"),
            PrimaryCommunityRole("owner"),
        ],
        recipients=[
            IfRequestedBy(
                requesters=[
                    PrimaryCommunityRole("curator"),
                    PrimaryCommunityRole("owner"),
                ],
                then_=[AutoApprove()],
                else_=[PrimaryCommunityRole("curator")],
            )
        ],
        escalations=[
            WorkflowRequestEscalation(
                after=timedelta(days=21), recipients=[PrimaryCommunityRole("owner")]
            )
        ],
    )


if False:
    translated_strings = [
        _("state:draft"),
        _("state:published"),
        _("state:submitted"),
        _("state:retracting"),
        _("state:deleted"),
    ]

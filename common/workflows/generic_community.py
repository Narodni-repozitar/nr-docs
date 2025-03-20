from datetime import timedelta

from invenio_i18n import lazy_gettext as _
from invenio_rdm_records.services.generators import IfRestricted
from invenio_records_permissions.generators import (
    AnyUser,
    Disable,
    SystemProcess,
)
from oarepo_communities.services.permissions.generators import (
    CommunityRole,
    PrimaryCommunityRole,
)
from oarepo_communities.services.permissions.policy import (
    CommunityDefaultWorkflowPermissions,
)
from oarepo_oaipmh_harvester.services.generators import IfNotHarvested
from oarepo_requests.services.permissions.generators import IfRequestedBy
from oarepo_runtime.services.permissions.generators import IfDraftType, RecordOwners
from oarepo_workflows import (
    AutoApprove,
    IfInState,
    WorkflowRequest,
    WorkflowRequestEscalation,
    WorkflowRequestPolicy,
    WorkflowTransitions,
)


class GenericCommunityWorkflowPermissions(CommunityDefaultWorkflowPermissions):
    can_create = [
        PrimaryCommunityRole("submitter"),
        PrimaryCommunityRole("owner"),
        PrimaryCommunityRole("curator"),
    ]

    can_read_generic = [
        RecordOwners(),
        CommunityRole("owner"),
        CommunityRole("curator"),
    ]

    can_read = can_read_generic + [
        IfInState(
            "published",
            then_=[
                # If the record is published, anyone can see its metadata
                AnyUser(),
            ],
        ),
    ]

    can_read_files = can_read_generic + [
        IfInState(
            "published",
            then_=[
                IfRestricted(
                    "files",
                    then_=[
                        RecordOwners(),
                        PrimaryCommunityRole("curator"),
                        PrimaryCommunityRole("owner"),
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

    can_manage_files = [Disable()]


# if the record is in draft state, the owner or curator can request publishing
publish_requesters = IfNotHarvested(
    then_=IfInState("draft", then_=[RecordOwners(), PrimaryCommunityRole("curator")]),
    else_=SystemProcess(),
)

# if the requester is the curator of the community, auto approve the request
publish_recipients = IfRequestedBy(
    requesters=[
        PrimaryCommunityRole("curator"),
        PrimaryCommunityRole("owner"),
    ],
    then_=[AutoApprove()],
    else_=[PrimaryCommunityRole("curator"), PrimaryCommunityRole("owner")],
)

publish_transitions = WorkflowTransitions(
    submitted="submitted",
    accepted="published",
    declined="draft",
    cancelled="draft",
)

# if the request is not resolved in 21 days, escalate it to the administrator
publish_escalations = [
    WorkflowRequestEscalation(
        after=timedelta(days=21),
        recipients=[
            PrimaryCommunityRole("owner"),
        ],
    )
]


class GenericCommunityWorkflowRequests(WorkflowRequestPolicy):
    publish_draft = WorkflowRequest(
        requesters=[
            IfDraftType(
                "metadata",
                then_=publish_requesters,
            )
        ],
        recipients=[publish_recipients],
        transitions=publish_transitions,
        escalations=publish_escalations,
    )

    publish_new_version = WorkflowRequest(
        requesters=[
            IfDraftType(
                ["new_version", "initial"],
                then_=publish_requesters,
            )
        ],
        recipients=[publish_recipients],
        transitions=publish_transitions,
        escalations=publish_escalations,
    )

    edit_published_record = WorkflowRequest(
        requesters=[
            IfNotHarvested(
                then_=IfInState(
                    "published",
                    then_=[
                        RecordOwners(),
                        PrimaryCommunityRole("curator"),
                        PrimaryCommunityRole("owner"),
                    ],
                ),
                else_=[SystemProcess()],
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
            IfNotHarvested(
                then_=IfInState(
                    "published",
                    then_=[
                        RecordOwners(),
                        PrimaryCommunityRole("curator"),
                        PrimaryCommunityRole("owner"),
                    ],
                ),
                else_=[SystemProcess()],
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
            IfNotHarvested(
                then_=[
                    RecordOwners(),
                    PrimaryCommunityRole("curator"),
                    PrimaryCommunityRole("owner"),
                ],
                else_=[SystemProcess()],
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
        escalations=[
            WorkflowRequestEscalation(
                after=timedelta(days=21),
                recipients=[PrimaryCommunityRole("owner")],
            )
        ],
    )

    delete_doi = WorkflowRequest(
        requesters=[
            IfNotHarvested(
                then_=[
                    RecordOwners(),
                    PrimaryCommunityRole("curator"),
                    PrimaryCommunityRole("owner"),
                ],
                else_=[SystemProcess()],
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
        escalations=[
            WorkflowRequestEscalation(
                after=timedelta(days=21),
                recipients=[PrimaryCommunityRole("owner")],
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

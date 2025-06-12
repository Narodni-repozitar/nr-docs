#
# Roles within the workflow:
#
# Community roles:
#
# CommunityRole("submitter") == people who can create new records
# CommunityRole("curator") == people who can publish records and remove them
# CommunityRole("owner") == supercurator, NTK staff
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

from invenio_access import action_factory
from invenio_access.permissions import Permission
from invenio_i18n import lazy_gettext as _
from invenio_rdm_records.services.generators import (
    AccessGrant,
    IfRecordDeleted,
    IfRestricted,
    SecretLinks,
)
from invenio_records_permissions.generators import (
    AnyUser,
    Disable,
    Generator,
    SystemProcess,
)
from invenio_users_resources.services.permissions import UserManager
from oarepo_communities.services.permissions.generators import (
    CommunityRole,
    PrimaryCommunityMembers,
    PrimaryCommunityRole,
    TargetCommunityRole,
)
from oarepo_communities.services.permissions.policy import (
    CommunityDefaultWorkflowPermissions,
)
from oarepo_oaipmh_harvester.services.generators import IfNotHarvested
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

direct_publish_action = action_factory("administration-direct-publish")
permission = Permission(direct_publish_action)


class DirectPublishAction(Generator):
    def __init__(self):
        super(DirectPublishAction, self).__init__()

    def needs(self, **kwargs):
        return [direct_publish_action]


class RestrictedWorkflowPermissions(CommunityDefaultWorkflowPermissions):

    # region Read record

    _can_read_anytime = [
        # owner of the draft can see the record
        RecordOwners(),
        # curator can see the record in any state
        CommunityRole("curator"),
        # owner of community can see the record in any state
        CommunityRole("owner"),
        # if the record is published and restricted, only members of the community can see it,
        # otherwise, any user can see it
        # every member of the community can see the metadata of the drafts, but not the files
    ]

    # who can read a draft record (on an /api/user/documents url)
    can_read_draft = _can_read_anytime + [
        IfInState(
            ["draft", "submitted"],
            then_=[
                PrimaryCommunityMembers(),
                AccessGrant("preview"),
                AccessGrant("edit"),
                SecretLinks("preview"),
                SecretLinks("edit"),
            ],
        ),
    ]

    # who can read a published record (on an /api/documents/ url)
    can_read = _can_read_anytime + [
        IfInState(
            ["published", "deleted"],
            then_=[
                AccessGrant("preview"),
                AccessGrant("view"),
                AccessGrant("edit"),
                SecretLinks("preview"),
                SecretLinks("view"),
                SecretLinks("edit"),
                IfRestricted(
                    "record",
                    then_=[PrimaryCommunityMembers()],
                    else_=[AnyUser()],
                ),
            ],
        ),
    ]

    # who can read a deleted record (on an /api/documents/ url)
    # this is strange, but taken from RDM
    can_read_deleted = [
        IfRecordDeleted(
            then_=[
                UserManager,  # this is strange, but taken from RDM
                SystemProcess(),
            ],
            else_=can_read,
        )
    ]

    # endregion

    # region Update record
    # who can update a draft record (on an /api/user/documents url)
    can_update_draft = [
        IfInState(
            "draft",
            then_=[
                RecordOwners(),
                PrimaryCommunityRole("curator"),
                PrimaryCommunityRole("owner"),
                AccessGrant("edit"),
                SecretLinks("edit"),
            ],
        ),
        # if not draft, can not be directly updated by any means, must use request
        IfInState(
            "submitted",
            then_=[
                PrimaryCommunityRole("curator"),
                PrimaryCommunityRole("owner"),
            ],
        ),
    ]

    # no one can update a published record
    can_update = [Disable()]
    # endregion

    # region Delete record
    # who can read a draft record (on an /api/user/documents url)
    can_delete_draft = can_update_draft

    # who can delete a published record (on an /api/documents/ url)
    can_delete = CommunityDefaultWorkflowPermissions.can_delete
    # endregion

    # region Create record
    # who can create a new record (on an /api/user/documents url)
    can_create = [
        PrimaryCommunityRole("submitter"),
        PrimaryCommunityRole("owner"),
        PrimaryCommunityRole("curator"),
    ]
    # endregion

    # region Draft files
    can_draft_read_files = _can_read_anytime + [
        IfRestricted(
            "files",
            then_=[],
            else_=[PrimaryCommunityMembers()],
        )
    ]

    can_draft_get_content_files = can_draft_read_files

    can_draft_update_files = [
        IfInState(
            "draft",
            then_=[
                RecordOwners(),
                PrimaryCommunityRole("curator"),
                PrimaryCommunityRole("owner"),
                AccessGrant("edit"),
                SecretLinks("edit"),
            ],
        ),
    ]
    can_draft_create_files = can_draft_update_files
    can_draft_set_content_files = can_draft_update_files
    can_draft_commit_files = can_draft_update_files
    can_draft_manage_files = can_update_draft
    can_draft_delete_files = can_draft_update_files

    can_commit_files = [
        Disable(),
    ]

    can_create_files = [
        Disable(),
    ]
    can_set_content_files = [
        Disable(),
    ]
    can_delete_files = [
        Disable(),
    ]
    # endregion

    # region Published files
    can_read_files = _can_read_anytime + [
        IfInState(
            "published",
            then_=[
                AccessGrant("view"),
                AccessGrant("edit"),
                IfRestricted(
                    "files",
                    then_=[
                        RecordOwners(),
                        PrimaryCommunityRole("curator"),
                        PrimaryCommunityRole("owner"),
                        SecretLinks("view"),
                    ],
                    else_=[AnyUser()],
                ),
            ],
        ),
    ]
    can_list_files = can_read_files
    can_get_content_files = can_read_files

    # modification of files is only on drafts
    can_update_files = [Disable()]
    can_manage_files = [
        Disable(),
    ]
    can_read_deleted_files = [SystemProcess()]
    # endregion

    # region Direct publish (without request and approval process)
    can_publish = [
        *CommunityDefaultWorkflowPermissions.can_publish,
        # only those with "administration-direct-publish" can publish directly (DERS)
        DirectPublishAction(),
    ]
    # endregion

    # region Direct edit metadata (without request and approval process)
    can_edit = CommunityDefaultWorkflowPermissions.can_edit + [
        # only those with "administration-direct-publish" can edit directly (DERS)
        DirectPublishAction(),
    ]
    # endregion

    # region Direct create new version (without request and approval process)
    can_new_version = CommunityDefaultWorkflowPermissions.can_new_version + [
        # only those with "administration-direct-publish" can create new version directly (DERS)
        DirectPublishAction(),
    ]
    # endregion

    # region Embargoes
    can_lift_embargo = CommunityDefaultWorkflowPermissions.can_lift_embargo
    # endregion

    # region Default values
    can_bulk_add = CommunityDefaultWorkflowPermissions.can_bulk_add
    can_add_community = CommunityDefaultWorkflowPermissions.can_add_community
    can_remove_community = CommunityDefaultWorkflowPermissions.can_remove_community

    can_create_or_update_many = (
        CommunityDefaultWorkflowPermissions.can_create_or_update_many
    )
    can_manage = CommunityDefaultWorkflowPermissions.can_manage + [
        PrimaryCommunityRole("curator"),
        PrimaryCommunityRole("owner"),
        AccessGrant("manage"),
    ]
    can_manage_internal = CommunityDefaultWorkflowPermissions.can_manage_internal
    can_manage_quota = CommunityDefaultWorkflowPermissions.can_manage_quota
    can_manage_record_access = (
        CommunityDefaultWorkflowPermissions.can_manage_record_access
    )
    can_moderate = CommunityDefaultWorkflowPermissions.can_moderate

    can_pid_create = CommunityDefaultWorkflowPermissions.can_pid_create
    can_pid_delete = CommunityDefaultWorkflowPermissions.can_pid_delete
    can_pid_update = CommunityDefaultWorkflowPermissions.can_pid_update
    can_pid_discard = CommunityDefaultWorkflowPermissions.can_pid_discard
    can_pid_manage = CommunityDefaultWorkflowPermissions.can_pid_manage
    can_pid_register = CommunityDefaultWorkflowPermissions.can_pid_register

    can_preview = CommunityDefaultWorkflowPermissions.can_read

    can_purge = CommunityDefaultWorkflowPermissions.can_purge
    can_query_stats = CommunityDefaultWorkflowPermissions.can_query_stats

    can_remove_record = CommunityDefaultWorkflowPermissions.can_remove_record

    can_review = CommunityDefaultWorkflowPermissions.can_review
    can_view = CommunityDefaultWorkflowPermissions.can_view
    # endregion


# if the record is in draft state, the owner or curator can request publishing
publish_requesters = [
    IfNotHarvested(
        then_=IfInState(
            "draft",
            then_=[
                RecordOwners(),
                PrimaryCommunityRole("curator"),
                PrimaryCommunityRole("owner"),
            ],
        ),
        else_=SystemProcess(),
    )
]
# if the requester is the curator of the community, auto approve the request
publish_recipients = [
    IfRequestedBy(
        requesters=[
            PrimaryCommunityRole("curator"),
            PrimaryCommunityRole("owner"),
        ],
        then_=[AutoApprove()],
        else_=[PrimaryCommunityRole("curator"), PrimaryCommunityRole("owner")],
    )
]

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


class RestrictedWorkflowRequests(WorkflowRequestPolicy):
    publish_draft = WorkflowRequest(
        requesters=publish_requesters,
        recipients=publish_recipients,
        transitions=publish_transitions,
        escalations=publish_escalations,
    )

    publish_new_version = WorkflowRequest(
        requesters=publish_requesters,
        recipients=publish_recipients,
        transitions=publish_transitions,
        escalations=publish_escalations,
    )

    publish_changed_metadata = WorkflowRequest(
        requesters=publish_requesters,
        recipients=publish_recipients,
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
                        AccessGrant("edit"),
                    ],
                ),
                else_=SystemProcess(),
            )
        ],
        # the request is auto-approve, we do not limit the owner of the record to create a new
        # draft version. It will need to be accepted by the curator though.
        recipients=[AutoApprove()],
    )

    new_version = WorkflowRequest(
        requesters=[
            IfNotHarvested(
                then_=IfInState(
                    "published",
                    then_=[
                        RecordOwners(),
                        PrimaryCommunityRole("curator"),
                        PrimaryCommunityRole("owner"),
                        AccessGrant("edit"),
                    ],
                ),
                else_=SystemProcess(),
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
            IfNotHarvested(
                then_=IfInState(
                    "published",
                    then_=[
                        RecordOwners(),
                        PrimaryCommunityRole("curator"),
                        PrimaryCommunityRole("owner"),
                    ],
                ),
                else_=SystemProcess(),
            )
        ],
        # if the requester is the curator of the community or administrator, auto approve the request,
        # otherwise, the request is sent to the curator
        recipients=[
            IfRequestedBy(
                requesters=[
                    PrimaryCommunityRole("owner"),
                ],
                then_=[AutoApprove()],
                else_=[PrimaryCommunityRole("owner")],
            )
        ],
        # the record comes to the state of retracting when the request is submitted. If the request
        # is accepted, the record is deleted, if declined, it is published again.
        transitions=WorkflowTransitions(
            submitted="retracting",
            declined="published",
            accepted="deleted",
            cancelled="published",
        ),
        # if the request is not resolved in 21 days, escalate it to the administrator
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
                else_=SystemProcess(),
            )
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
        escalations=[
            WorkflowRequestEscalation(
                after=timedelta(days=21), recipients=[PrimaryCommunityRole("owner")]
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

    initiate_community_migration = WorkflowRequest(
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
                else_=SystemProcess(),
            )
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
    )
    confirm_community_migration = WorkflowRequest(
        requesters=[],
        recipients=[
            TargetCommunityRole("curator"),
            TargetCommunityRole("owner"),
        ],
    )
    secondary_community_submission = WorkflowRequest(
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
                else_=SystemProcess(),
            )
        ],
        recipients=[
            IfRequestedBy(
                requesters=[
                    TargetCommunityRole("curator"),
                    TargetCommunityRole("owner"),
                ],
                then_=[AutoApprove()],
                else_=[TargetCommunityRole("curator"), TargetCommunityRole("owner")],
            )
        ],
    )


if False:
    # just for translation extraction
    translated_strings = [
        _("state:draft"),
        _("state:published"),
        _("state:submitted"),
        _("state:retracting"),
        _("state:deleted"),
    ]

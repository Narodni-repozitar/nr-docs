from invenio_records_permissions import RecordPermissionPolicy

# from invenio_records_permissions.generators import SystemProcess, AnyUser
from invenio_administration.generators import Administration
from invenio_communities.generators import CommunityCurators
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    Disable,
    IfConfig,
    SystemProcess,
)
from invenio_records_permissions.policies.records import RecordPermissionPolicy
from invenio_requests.services.generators import Receiver, Status
from invenio_requests.services.permissions import (
    PermissionPolicy as RequestPermissionPolicy,
)
from invenio_users_resources.services.permissions import UserManager

from invenio_rdm_records.requests.access import GuestAccessRequest
from invenio_rdm_records.services.generators import (
    AccessGrant,
    CommunityInclusionReviewers,
    GuestAccessRequestToken,
    IfCreate,
    IfDeleted,
    IfExternalDOIRecord,
    IfFileIsLocal,
    IfNewRecord,
    IfRecordDeleted,
    IfRequestType,
    IfRestricted,
    RecordCommunitiesAction,
    RecordOwners,
    ResourceAccessToken,
    SecretLinks,
    SubmissionReviewer,
)


class DocumentsPermissionPolicy(RecordPermissionPolicy):
    """documents.records.api.DocumentsRecord permissions.
    Values in this class will be merged with permission presets.
    """
    can_search = []
    can_read = []
    can_create = []
    can_update = []
    can_delete = []
    can_manage = []
    can_read_files = []
    can_update_files = []

    # can_create = []
    # can_update = []
    # can_delete = []
    # can_manage = []
    # can_search = []
    #
    # can_read = []
    # can_curate = can_manage + [AccessGrant("edit"), SecretLinks("edit")]
    #
    # can_preview = can_curate + [
    #     AccessGrant("preview"),
    #     SecretLinks("preview"),
    #     SubmissionReviewer(),
    #     UserManager,
    # ]
    # can_view = can_preview + [
    #     AccessGrant("view"),
    #     SecretLinks("view"),
    #     SubmissionReviewer(),
    #     CommunityInclusionReviewers(),
    #     RecordCommunitiesAction("view"),
    # ]
    # can_all = [AnyUser(), SystemProcess()]
    #
    # can_read_files = [
    #     IfRestricted("files", then_=can_view, else_=can_all),
    #     ResourceAccessToken("read"),
    # ]
    #
    # can_update_files = []

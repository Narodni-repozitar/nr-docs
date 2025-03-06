from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_administration.generators import Administration
from invenio_records_permissions.generators import SystemProcess
from invenio_communities.generators import (
    CommunityManagersForRole,
)
from oarepo_communities.services.permissions.generators import PrimaryCommunityRole
from invenio_records_permissions.generators import Disable


class NrDocsCommunitiesPermissionPolicy(CommunityPermissionPolicy):
    """"""
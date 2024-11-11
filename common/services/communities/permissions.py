from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_administration.generators import Administration
from invenio_records_permissions.generators import SystemProcess
from invenio_communities.generators import CommunityManagersForRole
from invenio_records_permissions.generators import Disable

class NrDocsCommunitiesPermissionPolicy(CommunityPermissionPolicy):
    """Permissions for Community CRUD operations specific to nr-docs.

    This class extends the default CommunityPermissionPolicy with specific
    permissions for the nr-docs community.

    The commented-out permissions are the default permissions from the
    CommunityPermissionPolicy class. They are commented out to be able to see
    how the total permissions look like.
    """
    can_create = [Administration(), SystemProcess()]
    """Only administrators can create communities, not common users."""

    # can_read = [
    #     IfRestricted("visibility", then_=[CommunityMembers()], else_=[AnyUser()]),
    #     SystemProcess(),
    # ]
    # """Who can read a community record (profile, etc.)"""
    #
    # # Used for search filtering of deleted records
    # # cannot be implemented inside can_read - otherwise permission will
    # # kick in before tombstone renders
    # can_read_deleted = [
    #     IfCommunityDeleted(then_=[UserManager, SystemProcess()], else_=can_read)
    # ]
    # """Who can read a deleted community record"""
    #
    # can_update = [CommunityOwners(), SystemProcess()]
    # """Who can update community metadata"""
    #
    # can_delete = [CommunityOwners(), SystemProcess()]
    # """Who can delete community (but keep in db)"""
    #
    # can_purge = [CommunityOwners(), SystemProcess()]
    # """Who can purge (completely remove) community"""
    #
    # can_manage_access = [
    #     IfConfig("COMMUNITIES_ALLOW_RESTRICTED", then_=can_update, else_=[]),
    # ]
    # """Who can manage access to the community from public to restricted and vice versa"""
    #
    # can_create_restricted = [
    #     IfConfig("COMMUNITIES_ALLOW_RESTRICTED", then_=can_create, else_=[]),
    # ]
    # """Who can create a restricted community, that is, a community that is not visible to non-members"""
    #
    # can_search = [AnyUser(), SystemProcess()]
    # """Anyone has the ability to search for communities but will find it only if can_read is satisfied."""
    #
    # can_search_user_communities = [AuthenticatedUser(), SystemProcess()]
    # """Authenticated users can search for their own communities."""
    #
    # can_search_invites = [CommunityManagers(), SystemProcess()]
    # """Who can search inside invitations."""
    #
    # can_search_requests = [CommunityManagers(), CommunityCurators(), SystemProcess()]
    # """Who can search inside requests."""
    #
    # can_rename = [CommunityOwners(), SystemProcess()]
    # """Who can rename a community."""
    #
    can_submit_record = [ SystemProcess() ]
    """Who can submit a record to a community directly. 
       We have a workflow for this, so allow just the system process."""
    #
    # # who can include a record directly, without a review
    can_include_directly = [ SystemProcess() ]
    """We have a workflow for both including to a secondary community 
       and publishing within primary, so just the system process."""
    #
    can_members_add = [ SystemProcess() ]
    """In invenio, one can invite a group - we are disabling this behaviour as
    users are handled by AAI and the invitation process targets individual users."""
    #
    # can_members_invite = [
    #     CommunityManagersForRole(),
    #     AllowedMemberTypes("user", "email"),
    #     SystemProcess(),
    # ]
    # """Who can invite a member to a community. The real configuration
    # is in the COMMUNITY_ROLES in invenio.cfg"""
    #
    # can_members_manage = [
    #     CommunityManagers(),
    #     SystemProcess(),
    # ]
    # """who can manage members of a community (remove them, change visibility, ...)"""
    #
    # can_members_search = [
    #     CommunityMembers(),
    #     SystemProcess(),
    # ]
    # """Who can search for members of a community - just the members of the same community."""
    #
    # can_members_search_public = [
    #     IfRestricted(
    #         "visibility",
    #         then_=[CommunityMembers()],
    #         else_=[
    #             IfRestricted(
    #                 "members_visibility",
    #                 then_=[CommunityMembers()],
    #                 else_=[AnyUser()],
    #             ),
    #         ],
    #     ),
    #     SystemProcess(),
    # ]
    # """Who can search for members of a public community -
    #     - if the community is restricted, only the members can search for other members
    #     - if the members are restricted, only the members can search for other members
    #    - otherwise, anyone can search for members."""
    #
    # # Ability to use membership update api
    # can_members_bulk_update = [
    #     CommunityMembers(),
    #     SystemProcess(),
    # ]
    # """Who can update multiple memberships at once (role, visibility, ...).
    # Note: the members_update permission is evaluated for each updated member."""
    #
    # can_members_bulk_delete = can_members_bulk_update
    # """Who can delete multiple memberships at .
    # Note: the members_delete permission is evaluated for each deleted member.
    # """
    #
    # # Ability to update a single membership
    can_members_update = [
        CommunityManagersForRole(),
        SystemProcess(),
    ]
    """Who can update a single membership (role, visibility, ...).
    Note: in nr-docs we do not allow users to change their role or visibility,
    just the manager can do that."""

    #
    # # Ability to delete a single membership
    can_members_delete = can_members_update
    """Who can delete a single membership. As with the update, only the manager can do that."""
    #
    # can_invite_owners = [CommunityOwners(), SystemProcess()]
    # """TODO: Who can invite another owner to a community."""
    #
    # # Abilities for featured communities
    # can_featured_search = [AnyUser(), SystemProcess()]
    # can_featured_list = [Administration(), SystemProcess()]
    # can_featured_create = [Administration(), SystemProcess()]
    # can_featured_update = [Administration(), SystemProcess()]
    # can_featured_delete = [Administration(), SystemProcess()]
    #
    # # Used to hide at the moment the `is_verified` field. It should be set to
    # # correct permissions based on which the field will be exposed only to moderators
    # can_moderate = [Disable()]
    #
    # # Permissions to crud community theming
    # can_set_theme = [SystemProcess()]
    # can_delete_theme = can_set_theme
    #
    # # Permissions to set if communities can have children
    # can_manage_children = [SystemProcess()]
    #
    # # Permission for assigning a parent community
    # can_manage_parent = [Administration(), SystemProcess()]
    #
    # request_membership permission is based on configuration, community settings and
    # identity. Other factors (e.g., previous membership requests) are not under
    # its purview and are dealt with elsewhere.
    can_request_membership = [ Disable() ]
    """Currently user can not ask for direct inclusion (just invitations), 
    so disable the direct request."""

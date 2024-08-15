from invenio_records_permissions.generators import AuthenticatedUser
from oarepo_communities.services.permissions.policy import CommunityWorkflowPermissionPolicy

class DocsCommunitiesPermissionPreset(CommunityWorkflowPermissionPolicy):
    can_create = [
        # TODO: just a workaround for now before we have community support in the UI
        # the community and workflow are added later on, so there should be no issue
        # here
        #
        # Note: can not add it at the beginning of a service as permissions are evaluated
        # in the UI resource as well and the "create" on service has not been called yet.
        # We still need the service or service component to add the community and default
        # workflow
        AuthenticatedUser(),
    ]
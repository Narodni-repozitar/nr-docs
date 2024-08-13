from invenio_records_resources.services.uow import unit_of_work
from invenio_communities.communities.records.api import Community

class AddDefaultCommunityServiceMixin:

    @unit_of_work()
    def create(self, identity, data, uow=None, expand=False, **kwargs):
        parent = data.setdefault("parent", {})
        community = parent.setdefault("communities", {})
        if 'default' in community:
            # TODO: this part should be moved directly to oarepo-communities and generated for each model
            resolved_community = Community.pid.resolve(community['default'])
            community['default'] = str(resolved_community.id)
        else:
            default_community = Community.pid.resolve("generic")
            community.setdefault("default", str(default_community.id))

        parent.setdefault("workflow", community.custom_fields.get('workflow', "default"))

        return super().create(identity, data, uow=uow, expand=expand, **kwargs)
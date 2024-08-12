from invenio_records_resources.services.uow import unit_of_work


class AddDefaultCommunityServiceMixin:

    @unit_of_work()
    def create(self, identity, data, uow=None, expand=False, **kwargs):
        parent = data.setdefault("parent", {})
        community = parent.setdefault("communities", {})
        community.setdefault("default", "generic")

        # this should be taken from the community automatically !!!
        parent.setdefault("workflow", "default")

        return super().create(identity, data, uow=uow, expand=expand, **kwargs)
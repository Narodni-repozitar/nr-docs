from invenio_access.permissions import system_identity
from invenio_communities.proxies import current_communities
from invenio_drafts_resources.services.records.components import ServiceComponent


class AddOwnersComponent(ServiceComponent):
    def create(self, identity, **kwargs):
        community = kwargs.get("record", None)
        if community is None:
            return

        # add the communities owner group
        current_communities.service.members.add(
            system_identity,
            community.id,
            {
                "role": "owner",
                "members": [{"type": "group", "id": "communities_owner"}],
            },
            uow=self.uow,
        )

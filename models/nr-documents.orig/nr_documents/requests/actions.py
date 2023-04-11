from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.uow import RecordCommitOp
from invenio_requests.customizations import AcceptAction
from invenio_requests.resolvers.registry import ResolverRegistry


class DefaultRequestRequestAcceptAction(AcceptAction):
    def execute(self, identity, uow):
        topic = self.request.topic.resolve()
        ## todo - do something with the record
        # topic["status"] = "accepted"
        ##
        for resolver in ResolverRegistry.get_registered_resolvers():
            if resolver.matches_entity(topic):
                topic_service = current_service_registry.get(resolver._service_id)
                break
        else:
            raise KeyError(f"topic {topic} service not found")
        uow.register(RecordCommitOp(topic, topic_service.indexer))
        super().execute(identity, uow)

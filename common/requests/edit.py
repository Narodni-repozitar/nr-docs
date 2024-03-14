from invenio_requests.customizations import actions

from invenio_requests.customizations import RequestType

from oarepo_runtime.i18n import lazy_gettext as _

from oarepo_requests.types.generic import OARepoRequestType
from oarepo_requests.utils import get_matching_service_for_record


class EditTopicAcceptAction(actions.AcceptAction):
    log_event = True

    def execute(self, identity, uow):
        topic = self.request.topic.resolve()
        topic_service = get_matching_service_for_record(topic)
        if not topic_service:
            raise KeyError(f"topic {topic} service not found")
        topic_service.edit(identity, topic.id, uow=uow)
        super().execute(identity, uow)



class EditRecordRequestType(OARepoRequestType):
    available_actions = {
        **RequestType.available_actions,
        "accept": EditTopicAcceptAction,
    }
    description = _("Request re-opening of published record")
    receiver_can_be_none = True

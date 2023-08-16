from oarepo_requests.actions.publish_draft import PublishDraftSubmitAction
from oarepo_requests.types.publish_draft import SubmitDraftRequestType


class PublishDraftRequestType(SubmitDraftRequestType):
    type_id = "publish_draft"
    name = "Publish-draft"

    available_actions = {
        **SubmitDraftRequestType.available_actions,
        "submit": PublishDraftSubmitAction,
    }

    allowed_topic_ref_types = [
        "nr_documents_draft"
    ]  # On the Request record object, the topic is referenced by pid. This pid is
    # extracted by Resolver subclassed from RecordResolver, which has hardcoded
    # {"record": {pid}} as reference value. This reference is then by
    # setattr set on the Request record topic ReferencedEntityField, and the set
    # operation checks, whether this key is in allowed_topic_ref_types
    # TODO would it make sense to customize the topic ref types?

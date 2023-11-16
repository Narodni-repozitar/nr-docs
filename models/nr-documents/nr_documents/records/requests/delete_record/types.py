from oarepo_requests.actions.delete_topic import DeleteTopicSubmitAction
from oarepo_requests.types.delete_record import DeleteRecordRequestType


class DeleteRecordRequestType(DeleteRecordRequestType):
    type_id = "delete_record"
    name = "Delete-record"

    available_actions = {
        **DeleteRecordRequestType.available_actions,
        "submit": DeleteTopicSubmitAction,
    }

    allowed_topic_ref_types = [
        "nr_documents"
    ]  # On the Request record object, the topic is referenced by pid. This pid is
    # extracted by Resolver subclassed from RecordResolver, which has hardcoded
    # {"record": {pid}} as reference value. This reference is then by
    # setattr set on the Request record topic ReferencedEntityField, and the set
    # operation checks, whether this key is in allowed_topic_ref_types

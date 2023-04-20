from invenio_requests.customizations import RequestType

from nr_documents.requests.actions import DefaultRequestRequestAcceptAction


class DefaultRequestRequestType(RequestType):
    type_id = "default_request"
    name = "Default_request"

    available_actions = {
        **RequestType.available_actions,
        "accept": DefaultRequestRequestAcceptAction,
    }

    allowed_topic_ref_types = [
        "nr_documents"
    ]  # On the Request record object, the topic is referenced by pid. This pid is
    # extracted by Resolver subclassed from RecordResolver, which has hardcoded
    # {"record": {pid}} as reference value. This reference is then by
    # setattr set on the Request record topic ReferencedEntityField, and the set
    # operation checks, whether this key is in allowed_topic_ref_types
    # TODO would it make sense to customize the topic ref types?

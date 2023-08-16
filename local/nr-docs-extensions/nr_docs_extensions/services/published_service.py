from nr_documents.services.records.config import NrDocumentsServiceConfig
from oarepo_published_service.services import (
    PublishedService,
    PublishedServiceConfig
)
from oarepo_requests.components import PublishDraftComponent, OAICreateRequestsComponent
from oarepo_requests.components.requests import PublishDraftComponentPrivate
from functools import partial

def get_published_service():
    config = NrDocumentsServiceConfig()
    components = config.components
    for idx, component in enumerate(components):
        if isinstance(component, partial) and component.func == PublishDraftComponentPrivate:
            components.insert(idx, OAICreateRequestsComponent("delete_record"))
            components.remove(component)
            break

    return PublishedService(
        config=PublishedServiceConfig(
            proxied_drafts_config=config
        )
    )
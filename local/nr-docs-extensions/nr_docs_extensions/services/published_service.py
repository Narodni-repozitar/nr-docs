from nr_documents.services.records.config import NrDocumentsServiceConfig
from oarepo_published_service.services import (
    PublishedService,
    PublishedServiceConfig
)

def get_published_service():
    return PublishedService(
        config=PublishedServiceConfig(
            proxied_drafts_config=NrDocumentsServiceConfig()
        )
    )
from nr_docs_extensions.services.published_service import (
    NrDocumentsPublishedServiceConfig,
)
from oarepo_published_service.services.config import (
    PublishedServiceConfig as PublishedServiceConfig,
)


class NrDocumentsPublishedServiceConfig(NrDocumentsPublishedServiceConfig):
    service_id = "published_nr_documents"

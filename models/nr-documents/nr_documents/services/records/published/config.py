from nr_docs_extensions.services.published_service import (
    NrDocumentsPublishedServiceConfig as PublishedServiceConfig,
)
from oarepo_published_service.services.config import (
    PublishedServiceConfig as PublishedServiceConfig,
)
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin


class NrDocumentsPublishedServiceConfig(
    PublishedServiceConfig, PermissionsPresetsConfigMixin
):
    service_id = "published_nr_documents"

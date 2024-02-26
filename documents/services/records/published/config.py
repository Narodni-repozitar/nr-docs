from oarepo_published_service.services import PublishedServiceConfig
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin


class DocumentsPublishedServiceConfig(
    PublishedServiceConfig, PermissionsPresetsConfigMixin
):
    service_id = "published_documents"

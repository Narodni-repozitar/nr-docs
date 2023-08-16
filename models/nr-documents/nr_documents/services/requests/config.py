from oarepo_runtime.config.service import PermissionsPresetsConfigMixin
from invenio_requests.services.requests.config import RequestsServiceConfig


class NrDocumentsRequestsServiceConfig(
    PermissionsPresetsConfigMixin, RequestsServiceConfig
):
    """ThesisRecord service config."""

    PERMISSIONS_PRESETS = ["requests"]
    components = RequestsServiceConfig.components

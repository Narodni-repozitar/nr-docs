import copy

from nr_documents.services.records.config import NrDocumentsServiceConfig
from oarepo_published_service.services import (
    PublishedService,
    PublishedServiceConfig
)
from oarepo_requests.components import PublishDraftComponent, OAICreateRequestsComponent
from oarepo_requests.components.requests import PublishDraftComponentPrivate
from functools import partial

from oarepo_runtime.config.service import PermissionsPresetsConfigMixin


# todo: do this better, edit this on the lvel of published service config
class NrDocumentsPublishedServiceConfig(PublishedServiceConfig, PermissionsPresetsConfigMixin):
    @property
    def components(self):
        return [
            component for component in super().components
            if not (isinstance(component, partial) and component.func == PublishDraftComponentPrivate)
        ]

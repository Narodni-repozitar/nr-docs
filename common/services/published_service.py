from oarepo_published_service.services import PublishedServiceConfig
# from oarepo_requests.services.components import PublishDraftComponentPrivate

from functools import partial

from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin


# todo: do this better, edit this on the lvel of published service config
class NrDocumentsPublishedServiceConfig(
    PublishedServiceConfig, PermissionsPresetsConfigMixin
):
    @property
    def components(self):
        return [
            component
            for component in super().components
            # if not (isinstance(component, partial) and component.func == PublishDraftComponentPrivate)
        ]

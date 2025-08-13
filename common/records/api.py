from invenio_drafts_resources.records.api import DraftRecordIdProviderV2
from oarepo_runtime.records.pid_providers import UniversalPIDMixin

from common.records.pid_providers import ReuseNUSLMixin

class DocumentsIdProvider(UniversalPIDMixin, ReuseNUSLMixin, DraftRecordIdProviderV2):
    pid_type = "dcmnts"
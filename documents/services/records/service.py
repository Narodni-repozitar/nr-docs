from invenio_drafts_resources.services import RecordService as InvenioRecordService
from common.services.service import AddDefaultCommunityServiceMixin


class DocumentsService(AddDefaultCommunityServiceMixin, InvenioRecordService):
    """DocumentsRecord service."""

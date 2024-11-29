from invenio_drafts_resources.services import RecordService as InvenioRecordService
from invenio_rdm_records.services.services import RDMRecordService

class DocumentsService(RDMRecordService):
    """DocumentsRecord service."""

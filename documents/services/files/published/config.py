from documents.services.files.config import DocumentsFileServiceConfig
from invenio_rdm_records.services.config import RDMFileRecordServiceConfig

class DocumentsFilePublishedServiceConfig(RDMFileRecordServiceConfig):
    service_id = "published_documents_file"

    @property
    def components(self):
        return [*super().components]

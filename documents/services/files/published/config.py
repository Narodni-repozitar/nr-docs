from documents.services.files.config import DocumentsFileServiceConfig


class DocumentsFilePublishedServiceConfig(DocumentsFileServiceConfig):
    service_id = "published_documents_file"

    @property
    def components(self):
        return [*super().components]

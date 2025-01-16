# take allowed extensions from here:
# current_app.config[ALLOWED_DOCUMENT_FILE_EXTENSIONS]


# .venv/lib/python3.12/site-packages/invenio_records_resources/services/files/components/base.py

from flask import current_app
from invenio_records_resources.services.files.components.base import (
    FileServiceComponent,
)


class AllowedDocumentExtensionsComponent(FileServiceComponent):
    def init_files(self, identity, id, record, data):
        # schema = self.service.file_schema.schema(many=True)
        # validated_data = schema.load(data)

        # validate file extensions
        allowed_extensions = current_app.config["ALLOWED_DOCUMENT_FILE_EXTENSIONS"]
        for file_data in data:
            if file_data["key"].split(".")[-1] not in allowed_extensions:
                raise Exception("File extension not allowed")

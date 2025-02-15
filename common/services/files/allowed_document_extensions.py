from flask import current_app
from flask_babel import _
from flask_resources import HTTPJSONException
from invenio_records_resources.services.files.components.base import (
    FileServiceComponent,
)


class AllowedDocumentExtensionsComponent(FileServiceComponent):
    affects = "*"

    def init_files(self, identity, id, record, data):
        allowed_extensions = tuple(
            current_app.config["ALLOWED_DOCUMENT_FILE_EXTENSIONS"]
        )

        for file_data in data:
            file_name = file_data["key"]
            if not file_name.lower().endswith(allowed_extensions):
                raise InvalidFileExtensionException(file_name)


class InvalidFileExtensionException(Exception):
    """File has invalid extension. Refer to ALLOWED_DOCUMENT_FILE_EXTENSIONS in invenio.cfg for allowed extensions."""

    def __init__(self, file_key):
        """Constructor."""
        super().__init__(
            _(
                "Invalid file extension for '{file_key}'. Supported formats: {allowed_extensions}"
            ).format(
                file_key=file_key,
                allowed_extensions=", ".join(
                    current_app.config["ALLOWED_DOCUMENT_FILE_EXTENSIONS"]
                ),
            )
        )
        self.file_key = file_key


def create_invalid_file_extension_handler():
    return lambda e: HTTPJSONException(
        code=415,
        description=str(e),
    )


ERROR_HANDLERS = {
    InvalidFileExtensionException: create_invalid_file_extension_handler()
}

from invenio_records_resources.services import FileService
from invenio_rdm_records.services.files.service import RDMFileService
from invenio_records_resources.services.errors import FileKeyNotFoundError


class DocumentsFileService(FileService):
    """DocumentsFile service."""

    def _get_record(self, id_, identity, action, file_key=None, **kwargs):
        """Get the associated record.

        If a ``file_key`` is specified and the record in question doesn't have a file
        for that key, a ``FileKeyNotFoundError`` will be raised.
        """
        # FIXME: Remove "registered_only=False" since it breaks access to an
        # unpublished record.
        record = self.record_cls.pid.resolve(id_, registered_only=False)
        self.require_permission(identity, action, record=record, file_key=file_key, **kwargs)

        if file_key and file_key not in record.files:
            raise FileKeyNotFoundError(id_, file_key)

        return record

class DocumentsFileDraftService(FileService):
    """DocumentsFileDraft service."""

    def _get_record(self, id_, identity, action, file_key=None, **kwargs):
        """Get the associated record.

        If a ``file_key`` is specified and the record in question doesn't have a file
        for that key, a ``FileKeyNotFoundError`` will be raised.
        """
        # FIXME: Remove "registered_only=False" since it breaks access to an
        # unpublished record.
        record = self.record_cls.pid.resolve(id_, registered_only=False)
        self.require_permission(identity, action, record=record, file_key=file_key, **kwargs)

        if file_key and file_key not in record.files:
            raise FileKeyNotFoundError(id_, file_key)

        return record
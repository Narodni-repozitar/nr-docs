from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records_resources.records.api import FileRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext

from nr_documents.files.models import (
    NrDocumentsFileDraftMetadata,
    NrDocumentsFileMetadata,
)


class NrDocumentsFileIdProvider(RecordIdProviderV2):
    pid_type = "dcmsfl"


class NrDocumentsFile(FileRecord):
    model_cls = NrDocumentsFileMetadata

    index = IndexField("nr_documents_file-nr_documents_file-1.0.0")

    pid = PIDField(
        provider=NrDocumentsFileIdProvider, context_cls=PIDFieldContext, create=True
    )
    record_cls = None  # is defined inside the parent record


class NrDocumentsFileDraft(FileRecord):
    model_cls = NrDocumentsFileDraftMetadata

    index = IndexField("nr_documents_file_draft-nr_documents_file_draft-1.0.0")

    pid = PIDField(
        provider=NrDocumentsFileIdProvider, context_cls=PIDFieldContext, create=True
    )
    record_cls = None  # is defined inside the parent record

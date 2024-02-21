from oarepo_requests.resolvers.ui import (
    draft_record_entity_reference_ui_resolver,
    record_entity_reference_ui_resolver,
    user_entity_reference_ui_resolver,
)
from oarepo_requests.resources.draft.resource import DraftRecordRequestsResource
from oarepo_requests.services.draft.service import DraftRecordRequestsService
from oarepo_runtime.records.entity_resolvers import UserResolver

from documents.files.api import DocumentsFileDraft
from documents.files.requests.resolvers import DocumentsFileDraftResolver
from documents.records.api import DocumentsDraft, DocumentsRecord
from documents.records.requests.delete_record.types import DeleteRecordRequestType
from documents.records.requests.publish_draft.types import PublishDraftRequestType
from documents.records.requests.resolvers import (
    DocumentsDraftResolver,
    DocumentsResolver,
)
from documents.resources.files.config import (
    DocumentsFileDraftResourceConfig,
    DocumentsFileResourceConfig,
)
from documents.resources.files.resource import (
    DocumentsFileDraftResource,
    DocumentsFileResource,
)
from documents.resources.records.config import DocumentsResourceConfig
from documents.resources.records.resource import DocumentsResource
from documents.services.files.config import (
    DocumentsFileDraftServiceConfig,
    DocumentsFileServiceConfig,
)
from documents.services.files.service import (
    DocumentsFileDraftService,
    DocumentsFileService,
)
from documents.services.records.config import DocumentsServiceConfig
from documents.services.records.service import DocumentsService

DOCUMENTS_RECORD_RESOURCE_CONFIG = DocumentsResourceConfig


DOCUMENTS_RECORD_RESOURCE_CLASS = DocumentsResource


DOCUMENTS_RECORD_SERVICE_CONFIG = DocumentsServiceConfig


DOCUMENTS_RECORD_SERVICE_CLASS = DocumentsService


DOCUMENTS_REQUESTS_RESOURCE_CLASS = DraftRecordRequestsResource


DOCUMENTS_REQUESTS_SERVICE_CLASS = DraftRecordRequestsService


REQUESTS_REGISTERED_TYPES = [
    DeleteRecordRequestType(),
    PublishDraftRequestType(),
]


REQUESTS_ENTITY_RESOLVERS = [
    UserResolver(),
    DocumentsResolver(
        record_cls=DocumentsRecord, service_id="documents", type_key="documents"
    ),
    DocumentsDraftResolver(
        record_cls=DocumentsDraft, service_id="documents", type_key="documents_draft"
    ),
    DocumentsFileDraftResolver(
        record_cls=DocumentsFileDraft,
        service_id="documents_file_draft",
        type_key="documents_file_draft",
    ),
]


ENTITY_REFERENCE_UI_RESOLVERS = {
    "user": user_entity_reference_ui_resolver,
    "documents": record_entity_reference_ui_resolver,
    "documents_draft": draft_record_entity_reference_ui_resolver,
}


DOCUMENTS_FILES_RESOURCE_CONFIG = DocumentsFileResourceConfig


DOCUMENTS_FILES_RESOURCE_CLASS = DocumentsFileResource


DOCUMENTS_FILES_SERVICE_CONFIG = DocumentsFileServiceConfig


DOCUMENTS_FILES_SERVICE_CLASS = DocumentsFileService


DOCUMENTS_DRAFT_FILES_RESOURCE_CONFIG = DocumentsFileDraftResourceConfig


DOCUMENTS_DRAFT_FILES_RESOURCE_CLASS = DocumentsFileDraftResource


DOCUMENTS_DRAFT_FILES_SERVICE_CONFIG = DocumentsFileDraftServiceConfig


DOCUMENTS_DRAFT_FILES_SERVICE_CLASS = DocumentsFileDraftService

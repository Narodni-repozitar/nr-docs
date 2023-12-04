from invenio_users_resources.resolvers import UserResolver

from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord
from nr_documents.records.requests.delete_record.types import DeleteRecordRequestType
from nr_documents.records.requests.publish_draft.types import PublishDraftRequestType
from nr_documents.records.requests.resolvers import (
    NrDocumentsDraftResolver,
    NrDocumentsResolver,
)
from nr_documents.resources.records.config import NrDocumentsResourceConfig
from nr_documents.resources.records.resource import NrDocumentsResource
from nr_documents.services.records.config import NrDocumentsServiceConfig
from nr_documents.services.records.service import NrDocumentsService

NR_DOCUMENTS_RECORD_RESOURCE_CONFIG = NrDocumentsResourceConfig


NR_DOCUMENTS_RECORD_RESOURCE_CLASS = NrDocumentsResource


NR_DOCUMENTS_RECORD_SERVICE_CONFIG = NrDocumentsServiceConfig


NR_DOCUMENTS_RECORD_SERVICE_CLASS = NrDocumentsService


REQUESTS_REGISTERED_TYPES = [
    DeleteRecordRequestType,
    PublishDraftRequestType,
]

REQUESTS_ENTITY_RESOLVERS = [
    UserResolver(),
    NrDocumentsResolver(
        record_cls=NrDocumentsRecord, service_id="nr_documents", type_key="nr_documents"
    ),
    NrDocumentsDraftResolver(
        record_cls=NrDocumentsDraft,
        service_id="nr_documents",
        type_key="nr_documents_draft",
    ),
]

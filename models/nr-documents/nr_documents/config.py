from invenio_users_resources.resolvers import UserResolver

from nr_documents.records.api import NrDocumentsRecord
from nr_documents.records.requests.default_request.types import (
    DefaultRequestRequestType,
)
from nr_documents.records.requests.resolvers import NrDocumentsResolver
from nr_documents.requests.resolvers import NrDocumentsResolver
from nr_documents.requests.types import DefaultRequestRequestType
from nr_documents.resources.records.config import NrDocumentsResourceConfig
from nr_documents.resources.records.resource import NrDocumentsResource
from nr_documents.services.records.config import NrDocumentsServiceConfig
from nr_documents.services.records.service import NrDocumentsService

NR_DOCUMENTS_RESOURCE_CONFIG_NR_DOCUMENTS = NrDocumentsResourceConfig
NR_DOCUMENTS_RESOURCE_CLASS_NR_DOCUMENTS = NrDocumentsResource
NR_DOCUMENTS_SERVICE_CONFIG_NR_DOCUMENTS = NrDocumentsServiceConfig
NR_DOCUMENTS_SERVICE_CLASS_NR_DOCUMENTS = NrDocumentsService

REQUESTS_REGISTERED_TYPES = [
    DefaultRequestRequestType,
]
REQUESTS_ENTITY_RESOLVERS = [
    UserResolver(),
    NrDocumentsResolver(
        record_cls=NrDocumentsRecord, service_id="nr_documents", type_key="nr_documents"
    ),
]


NR_DOCUMENTS_RECORD_RESOURCE_CONFIG = NrDocumentsResourceConfig


NR_DOCUMENTS_RECORD_RESOURCE_CLASS = NrDocumentsResource


NR_DOCUMENTS_RECORD_SERVICE_CONFIG = NrDocumentsServiceConfig


NR_DOCUMENTS_RECORD_SERVICE_CLASS = NrDocumentsService

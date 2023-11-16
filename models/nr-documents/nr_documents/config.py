from invenio_users_resources.resolvers import UserResolver

from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord
from nr_documents.records.requests.delete_record.types import DeleteRecordRequestType
from nr_documents.records.requests.publish_draft.types import PublishDraftRequestType
from nr_documents.records.requests.resolvers import (
    NrDocumentsDraftResolver,
    NrDocumentsResolver,
)
from nr_documents.resources.community_records.config import (
    NrDocumentsCommunityRecordResourceConfig,
)
from nr_documents.resources.community_records.resource import (
    NrDocumentsCommunityRecordResource,
)
from nr_documents.resources.record_communities.config import (
    NrDocumentsRecordCommunitiesResourceConfig,
)
from nr_documents.resources.record_communities.resource import (
    NrDocumentsRecordCommunitiesResource,
)
from nr_documents.resources.records.config import NrDocumentsResourceConfig
from nr_documents.resources.records.resource import NrDocumentsResource
from nr_documents.services.community_records.config import (
    NrDocumentsCommunityRecordServiceConfig,
)
from nr_documents.services.community_records.service import (
    NrDocumentsCommunityRecordService,
)
from nr_documents.services.record_communities.config import (
    NrDocumentsRecordCommunitiesServiceConfig,
)
from nr_documents.services.record_communities.service import (
    NrDocumentsRecordCommunitiesService,
)
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


NR_DOCUMENTS_RECORD_COMMUNITIES_RESOURCE_CONFIG = (
    NrDocumentsRecordCommunitiesResourceConfig
)


NR_DOCUMENTS_RECORD_COMMUNITIES_RESOURCE_CLASS = NrDocumentsRecordCommunitiesResource


NR_DOCUMENTS_RECORD_COMMUNITIES_SERVICE_CONFIG = (
    NrDocumentsRecordCommunitiesServiceConfig
)


NR_DOCUMENTS_RECORD_COMMUNITIES_SERVICE_CLASS = NrDocumentsRecordCommunitiesService


NR_DOCUMENTS_COMMUNITY_RECORDS_RESOURCE_CONFIG = (
    NrDocumentsCommunityRecordResourceConfig
)


NR_DOCUMENTS_COMMUNITY_RECORDS_RESOURCE_CLASS = NrDocumentsCommunityRecordResource


NR_DOCUMENTS_COMMUNITY_RECORDS_SERVICE_CONFIG = NrDocumentsCommunityRecordServiceConfig


NR_DOCUMENTS_COMMUNITY_RECORDS_SERVICE_CLASS = NrDocumentsCommunityRecordService

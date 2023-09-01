from invenio_records_resources.references import RecordResolver
from oarepo_runtime.resolvers import DraftProxy


class NrDocumentsResolver(RecordResolver):
    # invenio_requests.registry.TypeRegistry
    # requires name of the resolver for the model; needs only to be unique for the model, so use the name of the model
    type_id = "nr_documents"


class NrDocumentsDraftResolver(RecordResolver):
    # invenio_requests.registry.TypeRegistry
    # requires name of the resolver for the model; needs only to be unique for the model, so use the name of the model
    type_id = "nr_documents_draft"

    proxy_cls = DraftProxy

    def __init__(self, record_cls, service_id, type_key):
        super().__init__(
            record_cls, service_id, type_key=type_key, proxy_cls=self.proxy_cls
        )

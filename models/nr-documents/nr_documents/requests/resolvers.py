from invenio_records_resources.references import RecordResolver


class NrDocumentsResolver(RecordResolver):
    # invenio_requests.registry.TypeRegistry
    # requires name of the resolver for the model; needs only to be unique for the model, so use the name of the model
    type_id = "nr_documents"

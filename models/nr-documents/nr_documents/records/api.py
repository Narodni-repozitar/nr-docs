from invenio_drafts_resources.records.api import Draft as InvenioDraft
from invenio_drafts_resources.records.api import DraftRecordIdProviderV2, ParentRecord
from invenio_drafts_resources.records.api import Record as InvenioRecord
from invenio_records.systemfields import ConstantField, RelationsField
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from invenio_requests.records import Request
from invenio_requests.records.systemfields.relatedrecord import RelatedRecord
from invenio_vocabularies.records.api import Vocabulary
from oarepo_runtime.drafts.systemfields.has_draftcheck import HasDraftCheckField
from oarepo_runtime.relations import PIDRelation, RelationsField

from nr_documents.records.dumper import NrDocumentsDraftDumper, NrDocumentsDumper
from nr_documents.records.models import (
    NrDocumentsDraftMetadata,
    NrDocumentsMetadata,
    NrDocumentsParentMetadata,
    NrDocumentsParentState,
)
from nr_documents.records.multilingual_dumper import MultilingualSearchDumper


class NrDocumentsParentRecord(ParentRecord):
    model_cls = NrDocumentsParentMetadata
    delete_record = RelatedRecord(
        Request,
        keys=["type", "receiver", "status"],
    )
    publish_draft = RelatedRecord(
        Request,
        keys=["type", "receiver", "status"],
    )

    # schema = ConstantField(
    #    "$schema", "local://parent-v1.0.0.json"
    # )


class NrDocumentsIdProvider(DraftRecordIdProviderV2):
    pid_type = "dcmnts"


class NrDocumentsRecord(InvenioRecord):
    model_cls = NrDocumentsMetadata

    schema = ConstantField("$schema", "local://nr_documents-1.0.0.json")

    index = IndexField("nr_documents-nr_documents-1.0.0")

    pid = PIDField(
        provider=NrDocumentsIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper_extensions = [MultilingualSearchDumper()]
    dumper = NrDocumentsDumper(extensions=dumper_extensions)

    relations = RelationsField(
        degreeGrantors=PIDRelation(
            "metadata.thesis.degreeGrantors",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
    )

    versions_model_cls = NrDocumentsParentState

    parent_record_cls = NrDocumentsParentRecord


class NrDocumentsDraft(InvenioDraft):
    model_cls = NrDocumentsDraftMetadata

    schema = ConstantField("$schema", "local://nr_documents-1.0.0.json")

    index = IndexField("nr_documents-nr_documents_draft-1.0.0")

    pid = PIDField(
        provider=NrDocumentsIdProvider,
        context_cls=PIDFieldContext,
        create=True,
        delete=False,
    )

    dumper_extensions = [MultilingualSearchDumper()]
    dumper = NrDocumentsDraftDumper(extensions=dumper_extensions)

    relations = RelationsField(
        degreeGrantors=PIDRelation(
            "metadata.thesis.degreeGrantors",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
    )

    versions_model_cls = NrDocumentsParentState

    parent_record_cls = NrDocumentsParentRecord
    has_draft = HasDraftCheckField(config_key="HAS_DRAFT_CUSTOM_FIELD")


NrDocumentsRecord.has_draft = HasDraftCheckField(
    draft_cls=NrDocumentsDraft, config_key="HAS_DRAFT_CUSTOM_FIELD"
)

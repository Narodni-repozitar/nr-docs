from invenio_drafts_resources.records.api import (
    Draft,
    DraftRecordIdProviderV2,
    ParentRecord,
    Record,
)
from invenio_records.systemfields import ConstantField, RelationsField
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from invenio_vocabularies.records.api import Vocabulary
from oarepo_runtime.relations import PIDRelation, RelationsField

from nr_documents.records.dumper import NrDocumentsDumper
from nr_documents.records.models import (
    NrDocumentsDraftMetadata,
    NrDocumentsMetadata,
    NrDocumentsParentRecordMetadata,
    ParentState,
)
from nr_documents.records.multilingual_dumper import MultilingualDumper


class NrDocumentsParentRecord(
    ParentRecord
):  # TODO create special name for these? assuming yes
    model_cls = NrDocumentsParentRecordMetadata

    schema = ConstantField("$schema", "local://parent-v1.0.0.json")


class NrDocumentsIdProvider(DraftRecordIdProviderV2):
    pid_type = "dcmnts"


class NrDocumentsRecord(Record):
    model_cls = NrDocumentsMetadata

    schema = ConstantField("$schema", "local://nr_documents-1.0.0.json")

    index = IndexField("nr_documents-nr_documents-1.0.0")

    pid = PIDField(
        provider=NrDocumentsIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper_extensions = [MultilingualDumper()]
    dumper = NrDocumentsDumper(extensions=dumper_extensions)

    relations = RelationsField(
        degreeGrantors_item=PIDRelation(
            "metadata.thesis.degreeGrantors",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        affiliations_item=PIDRelation(
            "metadata.creators.affiliations",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        role=PIDRelation(
            "metadata.contributors.role",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-roles"),
        ),
        affiliations_item_1=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        resourceType=PIDRelation(
            "metadata.resourceType",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        subjectCategories_item=PIDRelation(
            "metadata.subjectCategories",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("subject-categories"),
        ),
        languages_item=PIDRelation(
            "metadata.languages",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        rights_item=PIDRelation(
            "metadata.rights",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("licenses"),
        ),
        accessRights=PIDRelation(
            "metadata.accessRights",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("access-rights"),
        ),
        affiliations_item_2=PIDRelation(
            "metadata.relatedItems.itemCreators.affiliations",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        role_1=PIDRelation(
            "metadata.relatedItems.itemContributors.role",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-roles"),
        ),
        affiliations_item_3=PIDRelation(
            "metadata.relatedItems.itemContributors.affiliations",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        itemRelationType=PIDRelation(
            "metadata.relatedItems.itemRelationType",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("item-relation-types"),
        ),
        itemResourceType=PIDRelation(
            "metadata.relatedItems.itemResourceType",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        funder=PIDRelation(
            "metadata.fundingReferences.funder",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("funders"),
        ),
        country=PIDRelation(
            "metadata.events.eventLocation.country",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("countries"),
        ),
    )
    versions_model_cls = ParentState
    parent_record_cls = NrDocumentsParentRecord


class NrDocumentsDraft(Draft):
    model_cls = NrDocumentsDraftMetadata

    schema = ConstantField("$schema", "local://nr_documents-1.0.0.json")

    index = IndexField("nr_documents-draft-nr_documents-1.0.0")

    pid = PIDField(
        provider=NrDocumentsIdProvider,
        context_cls=PIDFieldContext,
        create=True,
        delete=False,
    )

    dumper_extensions = []
    dumper = NrDocumentsDumper(extensions=dumper_extensions)
    versions_model_cls = ParentState
    parent_record_cls = NrDocumentsParentRecord

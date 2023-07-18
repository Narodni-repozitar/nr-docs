from invenio_drafts_resources.records.api import ParentRecord
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField, RelationsField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from invenio_vocabularies.records.api import Vocabulary
from oarepo_runtime.relations import PIDRelation, RelationsField

from nr_documents.records.dumper import NrDocumentsDumper
from nr_documents.records.models import (
    DraftParentMetadata,
    NrDocumentsMetadata,
    ParentState,
)
from nr_documents.records.multilingual_dumper import MultilingualSearchDumper


class NrDocumentsIdProvider(RecordIdProviderV2):
    pid_type = "dcmnts"


class NrDocumentsRecord(Record):
    model_cls = NrDocumentsMetadata

    schema = ConstantField("$schema", "local://nr_documents-1.0.0.json")

    index = IndexField("nr_documents-nr_documents-1.0.0")

    pid = PIDField(
        provider=NrDocumentsIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper_extensions = [MultilingualSearchDumper()]
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
            keys=["id", "title", {"key": "type.id", "target": "type"}, "id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-roles"),
        ),
        affiliations_item_1=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        resourceType=PIDRelation(
            "metadata.resourceType",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "id", "title"],
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
            keys=["id", "title", {"key": "type.id", "target": "type"}, "id", "title"],
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
            keys=["id", "title", {"key": "type.id", "target": "type"}, "id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("item-relation-types"),
        ),
        itemResourceType=PIDRelation(
            "metadata.relatedItems.itemResourceType",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        funder=PIDRelation(
            "metadata.fundingReferences.funder",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("funders"),
        ),
        country=PIDRelation(
            "metadata.events.eventLocation.country",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("countries"),
        ),
        affiliations=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        creators_affiliations=PIDRelation(
            "metadata.creators.affiliations",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        languages=PIDRelation(
            "metadata.languages",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        itemContributors_affiliations=PIDRelation(
            "metadata.relatedItems.itemContributors.affiliations",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        itemContributors_role=PIDRelation(
            "metadata.relatedItems.itemContributors.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-roles"),
        ),
        itemCreators_affiliations=PIDRelation(
            "metadata.relatedItems.itemCreators.affiliations",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        rights=PIDRelation(
            "metadata.rights",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("licenses"),
        ),
        subjectCategories=PIDRelation(
            "metadata.subjectCategories",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("subject-categories"),
        ),
        degreeGrantors=PIDRelation(
            "metadata.thesis.degreeGrantors",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
    )

    versions_model_cls = ParentState

    parent_record_cls = DraftParentRecord


class DraftParentRecord(
    ParentRecord
):  # TODO create special name for these? assuming yes
    model_cls = DraftParentMetadata

    schema = ConstantField("$schema", "local://parent-v1.0.0.json")

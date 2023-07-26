from invenio_drafts_resources.records.api import Draft as InvenioDraft
from invenio_drafts_resources.records.api import DraftRecordIdProviderV2, ParentRecord
from invenio_drafts_resources.records.api import Record as InvenioRecord
from invenio_records.systemfields import ConstantField, RelationsField
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from invenio_vocabularies.records.api import Vocabulary

from oarepo_runtime.drafts.systemfields.has_draftcheck import HasDraftCheckField
from oarepo_runtime.relations import PIDRelation, RelationsField

from nr_documents.records.dumper import NrDocumentsDraftDumper, NrDocumentsDumper
from nr_documents.records.models import (
    DraftParentMetadata,
    NrDocumentsDraftMetadata,
    NrDocumentsMetadata,
    ParentState,
)
from nr_documents.records.multilingual_dumper import MultilingualSearchDumper


class DraftParentRecord(
    ParentRecord
):  # TODO create special name for these? assuming yes
    model_cls = DraftParentMetadata

    schema = ConstantField("$schema", "local://parent-v1.0.0.json")


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
        accessRights=PIDRelation(
            "metadata.accessRights",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("access-rights"),
        ),
        affiliations=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        role=PIDRelation(
            "metadata.contributors.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-roles"),
        ),
        creators_affiliations=PIDRelation(
            "metadata.creators.affiliations",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        country=PIDRelation(
            "metadata.events.eventLocation.country",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("countries"),
        ),
        funder=PIDRelation(
            "metadata.fundingReferences.funder",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("funders"),
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
        itemRelationType=PIDRelation(
            "metadata.relatedItems.itemRelationType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("item-relation-types"),
        ),
        itemResourceType=PIDRelation(
            "metadata.relatedItems.itemResourceType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        resourceType=PIDRelation(
            "metadata.resourceType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
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

    dumper_extensions = []
    dumper = NrDocumentsDraftDumper(extensions=dumper_extensions)

    relations = RelationsField(
        accessRights=PIDRelation(
            "metadata.accessRights",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("access-rights"),
        ),
        affiliations=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        role=PIDRelation(
            "metadata.contributors.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-roles"),
        ),
        creators_affiliations=PIDRelation(
            "metadata.creators.affiliations",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        country=PIDRelation(
            "metadata.events.eventLocation.country",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("countries"),
        ),
        funder=PIDRelation(
            "metadata.fundingReferences.funder",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("funders"),
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
        itemRelationType=PIDRelation(
            "metadata.relatedItems.itemRelationType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("item-relation-types"),
        ),
        itemResourceType=PIDRelation(
            "metadata.relatedItems.itemResourceType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        resourceType=PIDRelation(
            "metadata.resourceType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
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

    has_draft = HasDraftCheckField(config_key="HAS_DRAFT")


NrDocumentsRecord.has_draft = HasDraftCheckField(draft_cls=NrDocumentsDraft, config_key="HAS_DRAFT")
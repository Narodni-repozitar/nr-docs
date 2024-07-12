from invenio_drafts_resources.records.api import Draft as InvenioDraft
from invenio_drafts_resources.records.api import DraftRecordIdProviderV2, ParentRecord
from invenio_drafts_resources.records.api import Record as InvenioRecord
from invenio_records.systemfields import ConstantField, ModelField
from invenio_records_resources.records.systemfields import FilesField, IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from invenio_vocabularies.records.api import Vocabulary
from oarepo_runtime.records.relations import PIDRelation, RelationsField
from oarepo_runtime.records.systemfields import (
    FirstItemSelector,
    PathSelector,
    SyntheticSystemField,
)
from oarepo_runtime.records.systemfields.has_draftcheck import HasDraftCheckField
from oarepo_runtime.records.systemfields.icu import ICUSearchField
from oarepo_runtime.records.systemfields.owner import OwnersField
from oarepo_runtime.records.systemfields.record_status import RecordStatusSystemField

from common.records.synthetic_fields import KeywordsFieldSelector
from common.services.sort import TitleICUSortField
from documents.files.api import DocumentsFile, DocumentsFileDraft
from documents.records.dumpers.dumper import DocumentsDraftDumper, DocumentsDumper
from documents.records.models import (
    DocumentsDraftMetadata,
    DocumentsMetadata,
    DocumentsParentMetadata,
    DocumentsParentState,
)


class DocumentsParentRecord(ParentRecord):
    model_cls = DocumentsParentMetadata

    owners = OwnersField()


class DocumentsIdProvider(DraftRecordIdProviderV2):
    pid_type = "dcmnts"


class DocumentsRecord(InvenioRecord):

    model_cls = DocumentsMetadata

    schema = ConstantField("$schema", "local://documents-1.0.0.json")

    index = IndexField(
        "documents-documents-1.0.0",
    )

    pid = PIDField(
        provider=DocumentsIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper = DocumentsDumper()

    sort = TitleICUSortField(source_field="metadata.title")

    title_search = ICUSearchField(source_field="metadata.title")

    creator_search = ICUSearchField(source_field="metadata.creators.fullName")

    abstract_search = ICUSearchField(source_field="metadata.abstract.value")

    people = SyntheticSystemField(
        PathSelector("metadata.creators", "metadata.contributors"),
        filter=lambda x: x.get("nameType") == "Personal",
        map=lambda x: x.get("fullName"),
        key="syntheticFields.people",
    )

    institutions = SyntheticSystemField(
        PathSelector(
            "metadata.creators.affiliations",
            "metadata.contributors.affiliations",
            "metadata.thesis.degreeGrantors",
        ),
        key="syntheticFields.institutions",
    )

    keywords = SyntheticSystemField(
        selector=KeywordsFieldSelector("metadata.subjects.subject"),
        key="syntheticFields.keywords",
    )

    date = SyntheticSystemField(
        selector=FirstItemSelector("metadata.dateModified", "metadata.dateIssued"),
        key="syntheticFields.date",
    )

    year = SyntheticSystemField(
        selector=FirstItemSelector("metadata.dateModified", "metadata.dateIssued"),
        key="syntheticFields.year",
        filter=lambda x: len(x) >= 4,
        map=lambda x: x[:4],
    )

    defenseYear = SyntheticSystemField(
        selector=PathSelector("metadata.thesis.dateDefended"),
        key="syntheticFields.defenseYear",
        filter=lambda x: len(x) >= 4,
        map=lambda x: x[:4],
    )

    relations = RelationsField(
        accessRights=PIDRelation(
            "metadata.accessRights",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("access-rights"),
        ),
        affiliations=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        contributorType=PIDRelation(
            "metadata.contributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        Organizational_contributorType=PIDRelation(
            "metadata.contributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        Personal_affiliations=PIDRelation(
            "metadata.creators.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
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
        itemContributors_Personal_affiliations=PIDRelation(
            "metadata.relatedItems.itemContributors.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        Personal_contributorType=PIDRelation(
            "metadata.relatedItems.itemContributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        itemContributors_Organizational_contributorType=PIDRelation(
            "metadata.relatedItems.itemContributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        itemCreators_Personal_affiliations=PIDRelation(
            "metadata.relatedItems.itemCreators.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
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
            pid_field=Vocabulary.pid.with_type_ctx("rights"),
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
        institutions=PIDRelation(
            "syntheticFields.institutions",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
    )

    versions_model_cls = DocumentsParentState

    parent_record_cls = DocumentsParentRecord
    record_status = RecordStatusSystemField()
    has_draft = HasDraftCheckField(
        draft_cls=lambda: DocumentsDraft, config_key="HAS_DRAFT_CUSTOM_FIELD"
    )

    files = FilesField(file_cls=DocumentsFile, store=False, create=False, delete=False)

    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)


class DocumentsDraft(InvenioDraft):

    model_cls = DocumentsDraftMetadata

    schema = ConstantField("$schema", "local://documents-1.0.0.json")

    index = IndexField("documents-documents_draft-1.0.0", search_alias="documents")

    pid = PIDField(
        provider=DocumentsIdProvider,
        context_cls=PIDFieldContext,
        create=True,
        delete=False,
    )

    dumper = DocumentsDraftDumper()

    relations = RelationsField(
        accessRights=PIDRelation(
            "metadata.accessRights",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("access-rights"),
        ),
        affiliations=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        contributorType=PIDRelation(
            "metadata.contributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        Organizational_contributorType=PIDRelation(
            "metadata.contributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        Personal_affiliations=PIDRelation(
            "metadata.creators.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
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
        itemContributors_Personal_affiliations=PIDRelation(
            "metadata.relatedItems.itemContributors.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        Personal_contributorType=PIDRelation(
            "metadata.relatedItems.itemContributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        itemContributors_Organizational_contributorType=PIDRelation(
            "metadata.relatedItems.itemContributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        itemCreators_Personal_affiliations=PIDRelation(
            "metadata.relatedItems.itemCreators.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
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
            pid_field=Vocabulary.pid.with_type_ctx("rights"),
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
        institutions=PIDRelation(
            "syntheticFields.institutions",
            keys=["id", "title", "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
    )

    versions_model_cls = DocumentsParentState

    parent_record_cls = DocumentsParentRecord
    record_status = RecordStatusSystemField()

    has_draft = HasDraftCheckField(config_key="HAS_DRAFT_CUSTOM_FIELD")

    files = FilesField(file_cls=DocumentsFileDraft, store=False)

    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)


DocumentsFile.record_cls = DocumentsRecord

DocumentsFileDraft.record_cls = DocumentsDraft

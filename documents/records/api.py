from invenio_communities.records.records.systemfields import CommunitiesField
from invenio_drafts_resources.records.api import DraftRecordIdProviderV2
from invenio_drafts_resources.services.records.components.media_files import (
    MediaFilesAttrConfig,
)
from invenio_rdm_records.records.api import (
    RDMDraft,
    RDMMediaFileDraft,
    RDMMediaFileRecord,
    RDMParent,
    RDMRecord,
)
from invenio_records.systemfields import ConstantField, ModelField
from invenio_records_resources.records.systemfields import FilesField, IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from invenio_vocabularies.contrib.affiliations.api import Affiliation
from invenio_vocabularies.contrib.awards.api import Award
from invenio_vocabularies.contrib.funders.api import Funder
from nr_metadata.records.synthetic_fields import KeywordsFieldSelector
from oarepo_communities.records.systemfields.communities import (
    OARepoCommunitiesFieldContext,
)
from oarepo_runtime.records.relations import PIDRelation, RelationsField
from oarepo_runtime.records.systemfields import (
    FilteredSelector,
    FirstItemSelector,
    MultiSelector,
    PathSelector,
    SyntheticSystemField,
)
from oarepo_runtime.records.systemfields.has_draftcheck import HasDraftCheckField
from oarepo_runtime.records.systemfields.icu import ICUSearchField
from oarepo_runtime.records.systemfields.record_status import RecordStatusSystemField
from oarepo_vocabularies.records.api import Vocabulary
from oarepo_workflows.records.systemfields.state import (
    RecordStateField,
    RecordStateTimestampField,
)
from oarepo_workflows.records.systemfields.workflow import WorkflowField

from common.services.sort import TitleICUSortField
from documents.files.api import DocumentsFile, DocumentsFileDraft
from documents.records.dumpers.dumper import DocumentsDraftDumper, DocumentsDumper
from documents.records.models import (
    DocumentsCommunitiesMetadata,
    DocumentsDraftMetadata,
    DocumentsMetadata,
    DocumentsParentMetadata,
    DocumentsParentState,
)


class DocumentsParentRecord(RDMParent):
    model_cls = DocumentsParentMetadata

    workflow = WorkflowField()

    communities = CommunitiesField(
        DocumentsCommunitiesMetadata, context_cls=OARepoCommunitiesFieldContext
    )


class DocumentsIdProvider(DraftRecordIdProviderV2):
    pid_type = "dcmnts"


class DocumentsRecord(RDMRecord):

    model_cls = DocumentsMetadata

    schema = ConstantField("$schema", "local://documents-1.0.0.json")

    index = IndexField("documents-documents-1.0.0", search_alias="documents")

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
        filter=lambda x: x.get("person_or_org", {}).get("type") == "personal",
        map=lambda x: x.get("name"),
        key="syntheticFields.people",
    )

    # organizations = SyntheticSystemField(
    #     MultiSelector(
    #         FilteredSelector(
    #             PathSelector("metadata.creators", "metadata.contributors"),
    #             filter=lambda x: x["nameType"] == "Personal",
    #             projection="affiliations.title.cs",
    #         ),
    #         FilteredSelector(
    #             PathSelector("metadata.creators", "metadata.contributors"),
    #             filter=lambda x: x["nameType"] == "Organizational",
    #             projection="fullName",
    #         ),
    #     ),
    #     key="syntheticFields.organizations",
    # )

    keywords = SyntheticSystemField(
        selector=KeywordsFieldSelector("metadata.subjects.subject"),
        key="syntheticFields.keywords",
    )

    date = SyntheticSystemField(
        selector=FirstItemSelector("metadata.dateModified", "metadata.dateIssued"),
        key="syntheticFields.date",
    )

    year = SyntheticSystemField(
        selector=FirstItemSelector(
            "metadata.dateIssued", "metadata.thesis.dateDefended"
        ),
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

    state = RecordStateField(initial="published")

    state_timestamp = RecordStateTimestampField()

    media_files = FilesField(
        key=MediaFilesAttrConfig["_files_attr_key"],
        bucket_id_attr=MediaFilesAttrConfig["_files_bucket_id_attr_key"],
        bucket_attr=MediaFilesAttrConfig["_files_bucket_attr_key"],
        store=False,
        dump=False,
        file_cls=RDMMediaFileRecord,
        create=False,
        delete=False,
    )

    relations = RelationsField(
        affiliations=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        creators_affiliations=PIDRelation(
            "metadata.creators.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        country=PIDRelation(
            "metadata.events.eventLocation.country",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("countries"),
        ),
        award=PIDRelation(
            "metadata.funders.award",
            keys=[
                "title",
                "number",
                "identifiers",
                "acronym",
                "program",
                "subjects",
                "organizations",
            ],
            pid_field=Award.pid,
        ),
        funder=PIDRelation(
            "metadata.funders.funder",
            keys=["identifiers", "name"],
            pid_field=Funder.pid,
        ),
        languages=PIDRelation(
            "metadata.languages",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        Personal_affiliations=PIDRelation(
            "metadata.relatedItems.itemContributors.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("affiliations"),
        ),
        contributorType=PIDRelation(
            "metadata.relatedItems.itemContributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        Organizational_contributorType=PIDRelation(
            "metadata.relatedItems.itemContributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        itemCreators_Personal_affiliations=PIDRelation(
            "metadata.relatedItems.itemCreators.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("affiliations"),
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


class RDMRecordMediaFiles(DocumentsRecord):
    """RDM Media file record API."""

    files = FilesField(
        key=MediaFilesAttrConfig["_files_attr_key"],
        bucket_id_attr=MediaFilesAttrConfig["_files_bucket_id_attr_key"],
        bucket_attr=MediaFilesAttrConfig["_files_bucket_attr_key"],
        store=False,
        dump=False,
        file_cls=RDMMediaFileRecord,
        # Don't create
        create=False,
        # Don't delete, we'll manage in the service
        delete=False,
    )


class DocumentsDraft(RDMDraft):

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

    state = RecordStateField()

    state_timestamp = RecordStateTimestampField()

    sort = TitleICUSortField(source_field="metadata.title")

    title_search = ICUSearchField(source_field="metadata.title")

    creator_search = ICUSearchField(source_field="metadata.creators.fullName")

    abstract_search = ICUSearchField(source_field="metadata.abstract.value")

    people = SyntheticSystemField(
        PathSelector(
            "metadata.creators.person_or_org", "metadata.contributors.person_or_org"
        ),
        filter=lambda x: x.get("type") == "personal",
        map=lambda x: x.get("name"),
        key="syntheticFields.people",
    )

    organizations = SyntheticSystemField(
        MultiSelector(
            FilteredSelector(
                PathSelector(
                    "metadata.creators.person_or_org",
                    "metadata.contributors.person_or_org",
                ),
                filter=lambda x: x["type"] == "personal",
                projection="affiliations.title.cs",
            ),
            FilteredSelector(
                PathSelector(
                    "metadata.creators.person_or_org",
                    "metadata.contributors.person_or_org",
                ),
                filter=lambda x: x["type"] == "organizational",
                projection="name",
            ),
        ),
        key="syntheticFields.organizations",
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
        selector=FirstItemSelector(
            "metadata.dateIssued", "metadata.thesis.dateDefended"
        ),
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

    media_files = FilesField(
        key=MediaFilesAttrConfig["_files_attr_key"],
        bucket_id_attr=MediaFilesAttrConfig["_files_bucket_id_attr_key"],
        bucket_attr=MediaFilesAttrConfig["_files_bucket_attr_key"],
        store=False,
        dump=False,
        file_cls=RDMMediaFileDraft,
        create=False,
        delete=False,
    )

    relations = RelationsField(
        affiliations=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        creators_affiliations=PIDRelation(
            "metadata.creators.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        country=PIDRelation(
            "metadata.events.eventLocation.country",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("countries"),
        ),
        award=PIDRelation(
            "metadata.funders.award",
            keys=[
                "title",
                "number",
                "identifiers",
                "acronym",
                "program",
                "subjects",
                "organizations",
            ],
            pid_field=Award.pid,
        ),
        funder=PIDRelation(
            "metadata.funders.funder",
            keys=["identifiers", "name"],
            pid_field=Funder.pid,
        ),
        languages=PIDRelation(
            "metadata.languages",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        Personal_affiliations=PIDRelation(
            "metadata.relatedItems.itemContributors.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("affiliations"),
        ),
        contributorType=PIDRelation(
            "metadata.relatedItems.itemContributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        Organizational_contributorType=PIDRelation(
            "metadata.relatedItems.itemContributors.contributorType",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        itemCreators_Personal_affiliations=PIDRelation(
            "metadata.relatedItems.itemCreators.affiliations",
            keys=["id", "title", {"key": "props.ror", "target": "ror"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("affiliations"),
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
    )

    versions_model_cls = DocumentsParentState

    parent_record_cls = DocumentsParentRecord
    record_status = RecordStatusSystemField()

    has_draft = HasDraftCheckField(config_key="HAS_DRAFT_CUSTOM_FIELD")

    files = FilesField(file_cls=DocumentsFileDraft, store=False)

    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)


class RDMDraftMediaFiles(DocumentsDraft):
    """RDM Draft media file API."""

    files = FilesField(
        key=MediaFilesAttrConfig["_files_attr_key"],
        bucket_id_attr=MediaFilesAttrConfig["_files_bucket_id_attr_key"],
        bucket_attr=MediaFilesAttrConfig["_files_bucket_attr_key"],
        store=False,
        dump=False,
        file_cls=RDMMediaFileDraft,
        # Don't delete, we'll manage in the service
        delete=False,
    )


RDMMediaFileRecord.record_cls = RDMRecordMediaFiles
RDMMediaFileDraft.record_cls = RDMDraftMediaFiles

DocumentsFile.record_cls = DocumentsRecord

DocumentsFileDraft.record_cls = DocumentsDraft

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
from oarepo_runtime.records.pid_providers import UniversalPIDMixin
from oarepo_runtime.records.relations import (
    PIDRelation,
    RelationsField,
    UnstrictPIDRelation,
)
from oarepo_runtime.records.systemfields import (
    FilteredSelector,
    FirstItemSelector,
    MultiSelector,
    PathSelector,
    SyntheticSystemField,
)
from oarepo_runtime.records.systemfields.has_draftcheck import HasDraftCheckField
from oarepo_runtime.records.systemfields.icu import (
    FulltextIndexField,
    ICUSearchField,
    TermIndexField,
)
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


class DocumentsIdProvider(UniversalPIDMixin, DraftRecordIdProviderV2):
    pid_type = "dcmnts"


class DocumentsRecord(RDMRecord):

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

    search_title = ICUSearchField(source_field="metadata.title", boost=20)

    search_creator_name = FulltextIndexField(
        source_field="metadata.creators.person_or_org.name", boost=20
    )

    search_contributor_name = FulltextIndexField(
        source_field="metadata.contributors.person_or_org.name", boost=20
    )

    search_contributor_identifier = TermIndexField(
        source_field="metadata.contributors.person_or_org.identifiers.identifier",
        boost=20,
    )

    search_creator_identifier = TermIndexField(
        source_field="metadata.creators.person_or_org.identifiers.identifier", boost=20
    )

    search_abstract = ICUSearchField(source_field="metadata.abstract", boost=10)

    search_subjects_subject_value = FulltextIndexField(
        source_field="metadata.subjects.subject.value", boost=10
    )

    search_additional_title = ICUSearchField(
        source_field="metadata.additionalTitles.title", boost=9
    )

    search_objectIdentifiers = TermIndexField(
        source_field="metadata.objectIdentifiers.identifier", boost=8
    )

    search_funder_funder_id = TermIndexField(
        source_field="metadata.funders.funder.id", boost=7
    )

    search_funder_funder_name = FulltextIndexField(
        source_field="metadata.funders.funder.name", boost=7
    )

    search_funder_funder_title = ICUSearchField(
        source_field="metadata.funders.funder.title", boost=7
    )

    search_publishers = FulltextIndexField(source_field="metadata.publishers", boost=7)

    search_resourceType_title = ICUSearchField(
        source_field="metadata.resourceType.title", boost=7
    )

    search_thesis_degreeGrantors_id = TermIndexField(
        source_field="metadata.thesis.degreeGrantors.id", boost=6
    )

    search_thesis_degreeGrantors_title = ICUSearchField(
        source_field="metadata.thesis.degreeGrantors.title", boost=6
    )

    search_events_eventNameOriginal = FulltextIndexField(
        source_field="metadata.events.eventNameOriginal", boost=6
    )

    search_events_eventNameAlternate = FulltextIndexField(
        source_field="metadata.events.eventNameAlternate", boost=6
    )

    search_contributor_affiliations_name = FulltextIndexField(
        source_field="metadata.contributors.affiliations.name", boost=5
    )

    search_creator_affiliations_name = FulltextIndexField(
        source_field="metadata.creators.affiliations.name", boost=5
    )

    search_funder_award_number = TermIndexField(
        source_field="metadata.funders.award.number", boost=5
    )

    search_funder_award_title = ICUSearchField(
        source_field="metadata.funders.award.title", boost=5
    )

    search_relatedItems_itemTitle = FulltextIndexField(
        source_field="metadata.relatedItems.itemTitle", boost=5
    )

    search_series_title = FulltextIndexField(
        source_field="metadata.series.seriesTitle", boost=2
    )

    search_relatedItems_itemPIDs_identifier = TermIndexField(
        source_field="metadata.relatedItems.itemPIDs.identifier", boost=2
    )

    search_notes = FulltextIndexField(source_field="metadata.notes")

    search_systemIdentifiers_identifier = TermIndexField(
        source_field="metadata.systemIdentifiers.identifier"
    )

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
        affiliations=UnstrictPIDRelation(
            "metadata.contributors.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        role=PIDRelation(
            "metadata.contributors.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        creators_affiliations=UnstrictPIDRelation(
            "metadata.creators.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        creators_role=PIDRelation(
            "metadata.creators.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        country=PIDRelation(
            "metadata.events.eventLocation.country",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("countries"),
        ),
        award=UnstrictPIDRelation(
            "metadata.funders.award",
            keys=[
                "title",
                "id",
                "number",
                "program",
                "acronym",
                "identifiers",
                "subjects",
                "organizations",
                "@v",
            ],
            pid_field=Award.pid,
        ),
        funder=UnstrictPIDRelation(
            "metadata.funders.funder",
            keys=["id", "@v", "name", "title"],
            pid_field=Funder.pid,
        ),
        languages=PIDRelation(
            "metadata.languages",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        itemContributors_affiliations=UnstrictPIDRelation(
            "metadata.relatedItems.itemContributors.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        itemContributors_role=PIDRelation(
            "metadata.relatedItems.itemContributors.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        itemCreators_affiliations=UnstrictPIDRelation(
            "metadata.relatedItems.itemCreators.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        itemCreators_role=PIDRelation(
            "metadata.relatedItems.itemCreators.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
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
            pid_field=Vocabulary.pid.with_type_ctx("degree-grantors"),
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

    search_title = ICUSearchField(source_field="metadata.title", boost=20)

    search_creator_name = FulltextIndexField(
        source_field="metadata.creators.person_or_org.name", boost=20
    )

    search_contributor_name = FulltextIndexField(
        source_field="metadata.contributors.person_or_org.name", boost=20
    )

    search_contributor_identifier = TermIndexField(
        source_field="metadata.contributors.person_or_org.identifiers.identifier",
        boost=20,
    )

    search_creator_identifier = TermIndexField(
        source_field="metadata.creators.person_or_org.identifiers.identifier", boost=20
    )

    search_abstract = ICUSearchField(source_field="metadata.abstract", boost=10)

    search_subjects_subject_value = FulltextIndexField(
        source_field="metadata.subjects.subject.value", boost=10
    )

    search_additional_title = ICUSearchField(
        source_field="metadata.additionalTitles.title", boost=9
    )

    search_objectIdentifiers = TermIndexField(
        source_field="metadata.objectIdentifiers.identifier", boost=8
    )

    search_funder_funder_id = TermIndexField(
        source_field="metadata.funders.funder.id", boost=7
    )

    search_funder_funder_name = FulltextIndexField(
        source_field="metadata.funders.funder.name", boost=7
    )

    search_funder_funder_title = ICUSearchField(
        source_field="metadata.funders.funder.title", boost=7
    )

    search_publishers = FulltextIndexField(source_field="metadata.publishers", boost=7)

    search_resourceType_title = ICUSearchField(
        source_field="metadata.resourceType.title", boost=7
    )

    search_thesis_degreeGrantors_id = TermIndexField(
        source_field="metadata.thesis.degreeGrantors.id", boost=6
    )

    search_thesis_degreeGrantors_title = ICUSearchField(
        source_field="metadata.thesis.degreeGrantors.title", boost=6
    )

    search_events_eventNameOriginal = FulltextIndexField(
        source_field="metadata.events.eventNameOriginal", boost=6
    )

    search_events_eventNameAlternate = FulltextIndexField(
        source_field="metadata.events.eventNameAlternate", boost=6
    )

    search_contributor_affiliations_name = FulltextIndexField(
        source_field="metadata.contributors.affiliations.name", boost=5
    )

    search_creator_affiliations_name = FulltextIndexField(
        source_field="metadata.creators.affiliations.name", boost=5
    )

    search_funder_award_number = TermIndexField(
        source_field="metadata.funders.award.number", boost=5
    )

    search_funder_award_title = ICUSearchField(
        source_field="metadata.funders.award.title", boost=5
    )

    search_relatedItems_itemTitle = FulltextIndexField(
        source_field="metadata.relatedItems.itemTitle", boost=5
    )

    search_series_title = FulltextIndexField(
        source_field="metadata.series.seriesTitle", boost=2
    )

    search_relatedItems_itemPIDs_identifier = TermIndexField(
        source_field="metadata.relatedItems.itemPIDs.identifier", boost=2
    )

    search_notes = FulltextIndexField(source_field="metadata.notes")

    search_systemIdentifiers_identifier = TermIndexField(
        source_field="metadata.systemIdentifiers.identifier"
    )

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
        affiliations=UnstrictPIDRelation(
            "metadata.contributors.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        role=PIDRelation(
            "metadata.contributors.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        creators_affiliations=UnstrictPIDRelation(
            "metadata.creators.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        creators_role=PIDRelation(
            "metadata.creators.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        country=PIDRelation(
            "metadata.events.eventLocation.country",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("countries"),
        ),
        award=UnstrictPIDRelation(
            "metadata.funders.award",
            keys=[
                "title",
                "id",
                "number",
                "program",
                "acronym",
                "identifiers",
                "subjects",
                "organizations",
                "@v",
            ],
            pid_field=Award.pid,
        ),
        funder=UnstrictPIDRelation(
            "metadata.funders.funder",
            keys=["id", "@v", "name", "title"],
            pid_field=Funder.pid,
        ),
        languages=PIDRelation(
            "metadata.languages",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        itemContributors_affiliations=UnstrictPIDRelation(
            "metadata.relatedItems.itemContributors.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        itemContributors_role=PIDRelation(
            "metadata.relatedItems.itemContributors.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
        ),
        itemCreators_affiliations=UnstrictPIDRelation(
            "metadata.relatedItems.itemCreators.affiliations",
            keys=["name", "id"],
            pid_field=Affiliation.pid,
        ),
        itemCreators_role=PIDRelation(
            "metadata.relatedItems.itemCreators.role",
            keys=["id", "title"],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-types"),
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
            pid_field=Vocabulary.pid.with_type_ctx("degree-grantors"),
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

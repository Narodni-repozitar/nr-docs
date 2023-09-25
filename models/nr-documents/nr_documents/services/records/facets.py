"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_vocabularies.services.facets import HierarchyVocabularyFacet

_schema = TermsFacet(field="$schema", label=_("$schema.label"))

created = DateTimeFacet(field="created", label=_("created.label"))

_id = TermsFacet(field="id", label=_("id.label"))

metadata_collection = TermsFacet(
    field="metadata.collection", label=_("metadata/collection.label")
)

metadata_thesis_dateDefended = DateTimeFacet(
    field="metadata.thesis.dateDefended", label=_("metadata/thesis/dateDefended.label")
)

metadata_thesis_defended = TermsFacet(
    field="metadata.thesis.defended", label=_("metadata/thesis/defended.label")
)

metadata_thesis_degreeGrantors = HierarchyVocabularyFacet(
    field="metadata.thesis.degreeGrantors",
    label=_("metadata/thesis/degreeGrantors.label"),
    vocabulary="institutions",
)

metadata_thesis_studyFields = TermsFacet(
    field="metadata.thesis.studyFields", label=_("metadata/thesis/studyFields.label")
)

syntheticFields_institutions = TermsFacet(
    field="syntheticFields.institutions", label=_("syntheticFields/institutions.label")
)

syntheticFields_keywords_cs = TermsFacet(
    field="syntheticFields.keywords_cs", label=_("syntheticFields/keywords_cs.label")
)

syntheticFields_keywords_en = TermsFacet(
    field="syntheticFields.keywords_en", label=_("syntheticFields/keywords_en.label")
)

syntheticFields_person = TermsFacet(
    field="syntheticFields.person", label=_("syntheticFields/person.label")
)

updated = DateTimeFacet(field="updated", label=_("updated.label"))

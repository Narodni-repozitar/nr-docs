from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class NrDocumentsSearchOptions(InvenioSearchOptions):
    """NrDocumentsRecord search options."""

    facets = {
        "_schema": facets._schema,
        "created": facets.created,
        "_id": facets._id,
        "metadata_collection": facets.metadata_collection,
        "metadata_thesis_dateDefended": facets.metadata_thesis_dateDefended,
        "metadata_thesis_defended": facets.metadata_thesis_defended,
        "metadata_thesis_degreeGrantors": facets.metadata_thesis_degreeGrantors,
        "metadata_thesis_studyFields": facets.metadata_thesis_studyFields,
        "syntheticFields_institutions": facets.syntheticFields_institutions,
        "syntheticFields_keywords_cs": facets.syntheticFields_keywords_cs,
        "syntheticFields_keywords_en": facets.syntheticFields_keywords_en,
        "syntheticFields_person": facets.syntheticFields_person,
        "updated": facets.updated,
        **getattr(InvenioSearchOptions, "facets", {}),
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
    }

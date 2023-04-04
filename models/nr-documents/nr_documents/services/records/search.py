from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


def _(x):
    """Identity function for string extraction."""
    return x


class NrDocumentsSearchOptions(InvenioSearchOptions):
    """NrDocumentsRecord search options."""

    facets = {
        "metadata_thesis_dateDefended": facets.metadata_thesis_dateDefended,
        "metadata_thesis_defended": facets.metadata_thesis_defended,
        "metadata_thesis_degreeGrantors_id": facets.metadata_thesis_degreeGrantors_id,
        "metadata_thesis_degreeGrantors_type": (
            facets.metadata_thesis_degreeGrantors_type
        ),
        "metadata_thesis_degreeGrantors_hierarchy_parent": (
            facets.metadata_thesis_degreeGrantors_hierarchy_parent
        ),
        "metadata_thesis_degreeGrantors_hierarchy_level": (
            facets.metadata_thesis_degreeGrantors_hierarchy_level
        ),
        "metadata_thesis_degreeGrantors_hierarchy_ancestors": (
            facets.metadata_thesis_degreeGrantors_hierarchy_ancestors
        ),
        "metadata_thesis_degreeGrantors__version": (
            facets.metadata_thesis_degreeGrantors__version
        ),
        "metadata_thesis_studyFields": facets.metadata_thesis_studyFields,
        "metadata_collection": facets.metadata_collection,
        "metadata_title_keyword": facets.metadata_title_keyword,
        "metadata_additionalTitles_title_lang": (
            facets.metadata_additionalTitles_title_lang
        ),
        "metadata_additionalTitles_title_cs_keyword": (
            facets.metadata_additionalTitles_title_cs_keyword
        ),
        "metadata_additionalTitles_title_en_keyword": (
            facets.metadata_additionalTitles_title_en_keyword
        ),
        "metadata_additionalTitles_title_value_keyword": (
            facets.metadata_additionalTitles_title_value_keyword
        ),
        "metadata_additionalTitles_titleType": (
            facets.metadata_additionalTitles_titleType
        ),
        "metadata_creators_affiliations_id": facets.metadata_creators_affiliations_id,
        "metadata_creators_affiliations_type": (
            facets.metadata_creators_affiliations_type
        ),
        "metadata_creators_affiliations_hierarchy_parent": (
            facets.metadata_creators_affiliations_hierarchy_parent
        ),
        "metadata_creators_affiliations_hierarchy_level": (
            facets.metadata_creators_affiliations_hierarchy_level
        ),
        "metadata_creators_affiliations_hierarchy_ancestors": (
            facets.metadata_creators_affiliations_hierarchy_ancestors
        ),
        "metadata_creators_affiliations__version": (
            facets.metadata_creators_affiliations__version
        ),
        "metadata_creators_nameType": facets.metadata_creators_nameType,
        "metadata_creators_fullName": facets.metadata_creators_fullName,
        "metadata_creators_authorityIdentifiers_identifier": (
            facets.metadata_creators_authorityIdentifiers_identifier
        ),
        "metadata_creators_authorityIdentifiers_scheme": (
            facets.metadata_creators_authorityIdentifiers_scheme
        ),
        "metadata_contributors_role_id": facets.metadata_contributors_role_id,
        "metadata_contributors_role_type": facets.metadata_contributors_role_type,
        "metadata_contributors_role__version": (
            facets.metadata_contributors_role__version
        ),
        "metadata_contributors_affiliations_id": (
            facets.metadata_contributors_affiliations_id
        ),
        "metadata_contributors_affiliations_type": (
            facets.metadata_contributors_affiliations_type
        ),
        "metadata_contributors_affiliations_hierarchy_parent": (
            facets.metadata_contributors_affiliations_hierarchy_parent
        ),
        "metadata_contributors_affiliations_hierarchy_level": (
            facets.metadata_contributors_affiliations_hierarchy_level
        ),
        "metadata_contributors_affiliations_hierarchy_ancestors": (
            facets.metadata_contributors_affiliations_hierarchy_ancestors
        ),
        "metadata_contributors_affiliations__version": (
            facets.metadata_contributors_affiliations__version
        ),
        "metadata_contributors_nameType": facets.metadata_contributors_nameType,
        "metadata_contributors_fullName": facets.metadata_contributors_fullName,
        "metadata_contributors_authorityIdentifiers_identifier": (
            facets.metadata_contributors_authorityIdentifiers_identifier
        ),
        "metadata_contributors_authorityIdentifiers_scheme": (
            facets.metadata_contributors_authorityIdentifiers_scheme
        ),
        "metadata_resourceType_id": facets.metadata_resourceType_id,
        "metadata_resourceType_type": facets.metadata_resourceType_type,
        "metadata_resourceType__version": facets.metadata_resourceType__version,
        "metadata_dateAvailable": facets.metadata_dateAvailable,
        "metadata_dateModified": facets.metadata_dateModified,
        "metadata_subjects_subjectScheme": facets.metadata_subjects_subjectScheme,
        "metadata_subjects_subject_lang": facets.metadata_subjects_subject_lang,
        "metadata_subjects_subject_cs_keyword": (
            facets.metadata_subjects_subject_cs_keyword
        ),
        "metadata_subjects_subject_en_keyword": (
            facets.metadata_subjects_subject_en_keyword
        ),
        "metadata_subjects_subject_value_keyword": (
            facets.metadata_subjects_subject_value_keyword
        ),
        "metadata_subjects_valueURI": facets.metadata_subjects_valueURI,
        "metadata_subjects_classificationCode": (
            facets.metadata_subjects_classificationCode
        ),
        "metadata_subjectCategories_id": facets.metadata_subjectCategories_id,
        "metadata_subjectCategories_type": facets.metadata_subjectCategories_type,
        "metadata_subjectCategories__version": (
            facets.metadata_subjectCategories__version
        ),
        "metadata_languages_id": facets.metadata_languages_id,
        "metadata_languages_type": facets.metadata_languages_type,
        "metadata_languages__version": facets.metadata_languages__version,
        "metadata_abstract_lang": facets.metadata_abstract_lang,
        "metadata_abstract_cs_keyword": facets.metadata_abstract_cs_keyword,
        "metadata_abstract_en_keyword": facets.metadata_abstract_en_keyword,
        "metadata_abstract_value_keyword": facets.metadata_abstract_value_keyword,
        "metadata_methods_lang": facets.metadata_methods_lang,
        "metadata_methods_cs_keyword": facets.metadata_methods_cs_keyword,
        "metadata_methods_en_keyword": facets.metadata_methods_en_keyword,
        "metadata_methods_value_keyword": facets.metadata_methods_value_keyword,
        "metadata_technicalInfo_lang": facets.metadata_technicalInfo_lang,
        "metadata_technicalInfo_cs_keyword": facets.metadata_technicalInfo_cs_keyword,
        "metadata_technicalInfo_en_keyword": facets.metadata_technicalInfo_en_keyword,
        "metadata_technicalInfo_value_keyword": (
            facets.metadata_technicalInfo_value_keyword
        ),
        "metadata_rights_id": facets.metadata_rights_id,
        "metadata_rights_type": facets.metadata_rights_type,
        "metadata_rights__version": facets.metadata_rights__version,
        "metadata_accessRights_id": facets.metadata_accessRights_id,
        "metadata_accessRights_type": facets.metadata_accessRights_type,
        "metadata_accessRights__version": facets.metadata_accessRights__version,
        "metadata_relatedItems_itemCreators_affiliations_id": (
            facets.metadata_relatedItems_itemCreators_affiliations_id
        ),
        "metadata_relatedItems_itemCreators_affiliations_type": (
            facets.metadata_relatedItems_itemCreators_affiliations_type
        ),
        "metadata_relatedItems_itemCreators_affiliations_hierarchy_parent": (
            facets.metadata_relatedItems_itemCreators_affiliations_hierarchy_parent
        ),
        "metadata_relatedItems_itemCreators_affiliations_hierarchy_level": (
            facets.metadata_relatedItems_itemCreators_affiliations_hierarchy_level
        ),
        "metadata_relatedItems_itemCreators_affiliations_hierarchy_ancestors": (
            facets.metadata_relatedItems_itemCreators_affiliations_hierarchy_ancestors
        ),
        "metadata_relatedItems_itemCreators_affiliations__version": (
            facets.metadata_relatedItems_itemCreators_affiliations__version
        ),
        "metadata_relatedItems_itemCreators_nameType": (
            facets.metadata_relatedItems_itemCreators_nameType
        ),
        "metadata_relatedItems_itemCreators_fullName": (
            facets.metadata_relatedItems_itemCreators_fullName
        ),
        "metadata_relatedItems_itemCreators_authorityIdentifiers_identifier": (
            facets.metadata_relatedItems_itemCreators_authorityIdentifiers_identifier
        ),
        "metadata_relatedItems_itemCreators_authorityIdentifiers_scheme": (
            facets.metadata_relatedItems_itemCreators_authorityIdentifiers_scheme
        ),
        "metadata_relatedItems_itemContributors_role_id": (
            facets.metadata_relatedItems_itemContributors_role_id
        ),
        "metadata_relatedItems_itemContributors_role_type": (
            facets.metadata_relatedItems_itemContributors_role_type
        ),
        "metadata_relatedItems_itemContributors_role__version": (
            facets.metadata_relatedItems_itemContributors_role__version
        ),
        "metadata_relatedItems_itemContributors_affiliations_id": (
            facets.metadata_relatedItems_itemContributors_affiliations_id
        ),
        "metadata_relatedItems_itemContributors_affiliations_type": (
            facets.metadata_relatedItems_itemContributors_affiliations_type
        ),
        "metadata_relatedItems_itemContributors_affiliations_hierarchy_parent": (
            facets.metadata_relatedItems_itemContributors_affiliations_hierarchy_parent
        ),
        "metadata_relatedItems_itemContributors_affiliations_hierarchy_level": (
            facets.metadata_relatedItems_itemContributors_affiliations_hierarchy_level
        ),
        "metadata_relatedItems_itemContributors_affiliations_hierarchy_ancestors": (
            facets.metadata_relatedItems_itemContributors_affiliations_hierarchy_ancestors
        ),
        "metadata_relatedItems_itemContributors_affiliations__version": (
            facets.metadata_relatedItems_itemContributors_affiliations__version
        ),
        "metadata_relatedItems_itemContributors_nameType": (
            facets.metadata_relatedItems_itemContributors_nameType
        ),
        "metadata_relatedItems_itemContributors_fullName": (
            facets.metadata_relatedItems_itemContributors_fullName
        ),
        "metadata_relatedItems_itemContributors_authorityIdentifiers_identifier": (
            facets.metadata_relatedItems_itemContributors_authorityIdentifiers_identifier
        ),
        "metadata_relatedItems_itemContributors_authorityIdentifiers_scheme": (
            facets.metadata_relatedItems_itemContributors_authorityIdentifiers_scheme
        ),
        "metadata_relatedItems_itemPIDs_identifier": (
            facets.metadata_relatedItems_itemPIDs_identifier
        ),
        "metadata_relatedItems_itemPIDs_scheme": (
            facets.metadata_relatedItems_itemPIDs_scheme
        ),
        "metadata_relatedItems_itemURL": facets.metadata_relatedItems_itemURL,
        "metadata_relatedItems_itemYear": facets.metadata_relatedItems_itemYear,
        "metadata_relatedItems_itemVolume": facets.metadata_relatedItems_itemVolume,
        "metadata_relatedItems_itemIssue": facets.metadata_relatedItems_itemIssue,
        "metadata_relatedItems_itemStartPage": (
            facets.metadata_relatedItems_itemStartPage
        ),
        "metadata_relatedItems_itemEndPage": facets.metadata_relatedItems_itemEndPage,
        "metadata_relatedItems_itemPublisher": (
            facets.metadata_relatedItems_itemPublisher
        ),
        "metadata_relatedItems_itemRelationType_id": (
            facets.metadata_relatedItems_itemRelationType_id
        ),
        "metadata_relatedItems_itemRelationType_type": (
            facets.metadata_relatedItems_itemRelationType_type
        ),
        "metadata_relatedItems_itemRelationType__version": (
            facets.metadata_relatedItems_itemRelationType__version
        ),
        "metadata_relatedItems_itemResourceType_id": (
            facets.metadata_relatedItems_itemResourceType_id
        ),
        "metadata_relatedItems_itemResourceType_type": (
            facets.metadata_relatedItems_itemResourceType_type
        ),
        "metadata_relatedItems_itemResourceType__version": (
            facets.metadata_relatedItems_itemResourceType__version
        ),
        "metadata_fundingReferences_projectID": (
            facets.metadata_fundingReferences_projectID
        ),
        "metadata_fundingReferences_funder_id": (
            facets.metadata_fundingReferences_funder_id
        ),
        "metadata_fundingReferences_funder_type": (
            facets.metadata_fundingReferences_funder_type
        ),
        "metadata_fundingReferences_funder__version": (
            facets.metadata_fundingReferences_funder__version
        ),
        "metadata_version": facets.metadata_version,
        "metadata_geoLocations_geoLocationPlace": (
            facets.metadata_geoLocations_geoLocationPlace
        ),
        "metadata_geoLocations_geoLocationPoint_pointLongitude": (
            facets.metadata_geoLocations_geoLocationPoint_pointLongitude
        ),
        "metadata_geoLocations_geoLocationPoint_pointLatitude": (
            facets.metadata_geoLocations_geoLocationPoint_pointLatitude
        ),
        "metadata_accessibility_lang": facets.metadata_accessibility_lang,
        "metadata_accessibility_cs_keyword": facets.metadata_accessibility_cs_keyword,
        "metadata_accessibility_en_keyword": facets.metadata_accessibility_en_keyword,
        "metadata_accessibility_value_keyword": (
            facets.metadata_accessibility_value_keyword
        ),
        "metadata_series_seriesTitle": facets.metadata_series_seriesTitle,
        "metadata_series_seriesVolume": facets.metadata_series_seriesVolume,
        "metadata_externalLocation_externalLocationURL": (
            facets.metadata_externalLocation_externalLocationURL
        ),
        "metadata_originalRecord": facets.metadata_originalRecord,
        "metadata_objectIdentifiers_identifier": (
            facets.metadata_objectIdentifiers_identifier
        ),
        "metadata_objectIdentifiers_scheme": facets.metadata_objectIdentifiers_scheme,
        "metadata_systemIdentifiers_identifier": (
            facets.metadata_systemIdentifiers_identifier
        ),
        "metadata_systemIdentifiers_scheme": facets.metadata_systemIdentifiers_scheme,
        # TODO: generate proper facet type
        # ! date_range cannot be of type TermsFacet
        # "metadata_events_eventDate": facets.metadata_events_eventDate,
        "metadata_events_eventLocation_place": (
            facets.metadata_events_eventLocation_place
        ),
        "metadata_events_eventLocation_country_id": (
            facets.metadata_events_eventLocation_country_id
        ),
        "metadata_events_eventLocation_country_type": (
            facets.metadata_events_eventLocation_country_type
        ),
        "metadata_events_eventLocation_country__version": (
            facets.metadata_events_eventLocation_country__version
        ),
        "_id": facets._id,
        "created": facets.created,
        "updated": facets.updated,
        "_schema": facets._schema,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
        "bestmatch": dict(
            title=_("Best match"),
            fields=["_score"],  # ES defaults to desc on `_score` field
        ),
        "newest": dict(
            title=_("Newest"),
            fields=["-created"],
        ),
        "oldest": dict(
            title=_("Oldest"),
            fields=["created"],
        ),
    }

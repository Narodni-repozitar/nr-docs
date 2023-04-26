from flask_babelex import lazy_gettext as _
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class NrDocumentsSearchOptions(InvenioSearchOptions):
    """NrDocumentsRecord search options."""

    facets = {
        "metadata_thesis_dateDefended": facets.metadata_thesis_dateDefended,
        "metadata_thesis_defended": facets.metadata_thesis_defended,
        "metadata_thesis_degreeGrantors": facets.metadata_thesis_degreeGrantors,
        "metadata_thesis_studyFields": facets.metadata_thesis_studyFields,
        "metadata_collection": facets.metadata_collection,
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
        "metadata_creators_affiliations": facets.metadata_creators_affiliations,
        "metadata_creators_nameType": facets.metadata_creators_nameType,
        "metadata_creators_fullName": facets.metadata_creators_fullName,
        "metadata_creators_authorityIdentifiers_identifier": (
            facets.metadata_creators_authorityIdentifiers_identifier
        ),
        "metadata_creators_authorityIdentifiers_scheme": (
            facets.metadata_creators_authorityIdentifiers_scheme
        ),
        "metadata_contributors_role": facets.metadata_contributors_role,
        "metadata_contributors_affiliations": facets.metadata_contributors_affiliations,
        "metadata_contributors_nameType": facets.metadata_contributors_nameType,
        "metadata_contributors_fullName": facets.metadata_contributors_fullName,
        "metadata_contributors_authorityIdentifiers_identifier": (
            facets.metadata_contributors_authorityIdentifiers_identifier
        ),
        "metadata_contributors_authorityIdentifiers_scheme": (
            facets.metadata_contributors_authorityIdentifiers_scheme
        ),
        "metadata_resourceType": facets.metadata_resourceType,
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
        "metadata_subjectCategories": facets.metadata_subjectCategories,
        "metadata_languages": facets.metadata_languages,
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
        "metadata_rights": facets.metadata_rights,
        "metadata_accessRights": facets.metadata_accessRights,
        "metadata_relatedItems_itemCreators_affiliations": (
            facets.metadata_relatedItems_itemCreators_affiliations
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
        "metadata_relatedItems_itemContributors_role": (
            facets.metadata_relatedItems_itemContributors_role
        ),
        "metadata_relatedItems_itemContributors_affiliations": (
            facets.metadata_relatedItems_itemContributors_affiliations
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
        "metadata_relatedItems_itemRelationType": (
            facets.metadata_relatedItems_itemRelationType
        ),
        "metadata_relatedItems_itemResourceType": (
            facets.metadata_relatedItems_itemResourceType
        ),
        "metadata_fundingReferences_projectID": (
            facets.metadata_fundingReferences_projectID
        ),
        "metadata_fundingReferences_funder": facets.metadata_fundingReferences_funder,
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
        "metadata_events_eventDate": facets.metadata_events_eventDate,
        "metadata_events_eventLocation_place": (
            facets.metadata_events_eventLocation_place
        ),
        "metadata_events_eventLocation_country": (
            facets.metadata_events_eventLocation_country
        ),
        "_id": facets._id,
        "created": facets.created,
        "updated": facets.updated,
        "_schema": facets._schema,
        "metadata_thesis_dateDefended": facets.metadata_thesis_dateDefended,
        "metadata_thesis_defended": facets.metadata_thesis_defended,
        "metadata_thesis_degreeGrantors": facets.metadata_thesis_degreeGrantors,
        "metadata_thesis_studyFields": facets.metadata_thesis_studyFields,
        "metadata_collection": facets.metadata_collection,
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
        "metadata_creators_affiliations": facets.metadata_creators_affiliations,
        "metadata_creators_nameType": facets.metadata_creators_nameType,
        "metadata_creators_fullName": facets.metadata_creators_fullName,
        "metadata_creators_authorityIdentifiers_identifier": (
            facets.metadata_creators_authorityIdentifiers_identifier
        ),
        "metadata_creators_authorityIdentifiers_scheme": (
            facets.metadata_creators_authorityIdentifiers_scheme
        ),
        "metadata_contributors_role": facets.metadata_contributors_role,
        "metadata_contributors_affiliations": facets.metadata_contributors_affiliations,
        "metadata_contributors_nameType": facets.metadata_contributors_nameType,
        "metadata_contributors_fullName": facets.metadata_contributors_fullName,
        "metadata_contributors_authorityIdentifiers_identifier": (
            facets.metadata_contributors_authorityIdentifiers_identifier
        ),
        "metadata_contributors_authorityIdentifiers_scheme": (
            facets.metadata_contributors_authorityIdentifiers_scheme
        ),
        "metadata_resourceType": facets.metadata_resourceType,
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
        "metadata_subjectCategories": facets.metadata_subjectCategories,
        "metadata_languages": facets.metadata_languages,
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
        "metadata_rights": facets.metadata_rights,
        "metadata_accessRights": facets.metadata_accessRights,
        "metadata_relatedItems_itemCreators_affiliations": (
            facets.metadata_relatedItems_itemCreators_affiliations
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
        "metadata_relatedItems_itemContributors_role": (
            facets.metadata_relatedItems_itemContributors_role
        ),
        "metadata_relatedItems_itemContributors_affiliations": (
            facets.metadata_relatedItems_itemContributors_affiliations
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
        "metadata_relatedItems_itemRelationType": (
            facets.metadata_relatedItems_itemRelationType
        ),
        "metadata_relatedItems_itemResourceType": (
            facets.metadata_relatedItems_itemResourceType
        ),
        "metadata_fundingReferences_projectID": (
            facets.metadata_fundingReferences_projectID
        ),
        "metadata_fundingReferences_funder": facets.metadata_fundingReferences_funder,
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
        "metadata_events_eventDate": facets.metadata_events_eventDate,
        "metadata_events_eventLocation_place": (
            facets.metadata_events_eventLocation_place
        ),
        "metadata_events_eventLocation_country": (
            facets.metadata_events_eventLocation_country
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
        **InvenioSearchOptions.sort_options,
    }

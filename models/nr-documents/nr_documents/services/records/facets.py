"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

metadata_thesis_dateDefended = TermsFacet(
    field="metadata.thesis.dateDefended", label=_("metadata.thesis.dateDefended.label")
)


metadata_thesis_defended = TermsFacet(
    field="metadata.thesis.defended", label=_("metadata.thesis.defended.label")
)


metadata_thesis_degreeGrantors_id = TermsFacet(
    field="metadata.thesis.degreeGrantors.id",
    label=_("metadata.thesis.degreeGrantors.id.label"),
)


metadata_thesis_degreeGrantors_type = TermsFacet(
    field="metadata.thesis.degreeGrantors.type",
    label=_("metadata.thesis.degreeGrantors.type.label"),
)


metadata_thesis_degreeGrantors_hierarchy_parent = TermsFacet(
    field="metadata.thesis.degreeGrantors.hierarchy.parent",
    label=_("metadata.thesis.degreeGrantors.hierarchy.parent.label"),
)


metadata_thesis_degreeGrantors_hierarchy_level = TermsFacet(
    field="metadata.thesis.degreeGrantors.hierarchy.level",
    label=_("metadata.thesis.degreeGrantors.hierarchy.level.label"),
)


metadata_thesis_degreeGrantors_hierarchy_ancestors = TermsFacet(
    field="metadata.thesis.degreeGrantors.hierarchy.ancestors",
    label=_("metadata.thesis.degreeGrantors.hierarchy.ancestors.label"),
)


metadata_thesis_degreeGrantors__version = TermsFacet(
    field="metadata.thesis.degreeGrantors.@v",
    label=_("metadata.thesis.degreeGrantors.@v.label"),
)


metadata_thesis_studyFields = TermsFacet(
    field="metadata.thesis.studyFields", label=_("metadata.thesis.studyFields.label")
)


metadata_collection = TermsFacet(
    field="metadata.collection", label=_("metadata.collection.label")
)


metadata_title_keyword = TermsFacet(
    field="metadata.title.keyword", label=_("metadata.title.keyword.label")
)


metadata_additionalTitles_title_lang = NestedLabeledFacet(
    path="metadata.additionalTitles.title",
    nested_facet=TermsFacet(
        field="metadata.additionalTitles.title.lang",
        label=_("metadata.additionalTitles.title.lang.label"),
    ),
)


metadata_additionalTitles_title_cs_keyword = TermsFacet(
    field="metadata.additionalTitles.title_cs.keyword"
)


metadata_additionalTitles_title_en_keyword = TermsFacet(
    field="metadata.additionalTitles.title_en.keyword"
)


metadata_additionalTitles_title_value_keyword = NestedLabeledFacet(
    path="metadata.additionalTitles.title",
    nested_facet=TermsFacet(
        field="metadata.additionalTitles.title.value.keyword",
        label=_("metadata.additionalTitles.title.value.keyword.label"),
    ),
)


metadata_additionalTitles_titleType = TermsFacet(
    field="metadata.additionalTitles.titleType",
    label=_("metadata.additionalTitles.titleType.label"),
)


metadata_creators_affiliations_id = TermsFacet(
    field="metadata.creators.affiliations.id",
    label=_("metadata.creators.affiliations.id.label"),
)


metadata_creators_affiliations_type = TermsFacet(
    field="metadata.creators.affiliations.type",
    label=_("metadata.creators.affiliations.type.label"),
)


metadata_creators_affiliations_hierarchy_parent = TermsFacet(
    field="metadata.creators.affiliations.hierarchy.parent",
    label=_("metadata.creators.affiliations.hierarchy.parent.label"),
)


metadata_creators_affiliations_hierarchy_level = TermsFacet(
    field="metadata.creators.affiliations.hierarchy.level",
    label=_("metadata.creators.affiliations.hierarchy.level.label"),
)


metadata_creators_affiliations_hierarchy_ancestors = TermsFacet(
    field="metadata.creators.affiliations.hierarchy.ancestors",
    label=_("metadata.creators.affiliations.hierarchy.ancestors.label"),
)


metadata_creators_affiliations__version = TermsFacet(
    field="metadata.creators.affiliations.@v",
    label=_("metadata.creators.affiliations.@v.label"),
)


metadata_creators_nameType = TermsFacet(
    field="metadata.creators.nameType", label=_("metadata.creators.nameType.label")
)


metadata_creators_fullName = TermsFacet(
    field="metadata.creators.fullName", label=_("metadata.creators.fullName.label")
)


metadata_creators_authorityIdentifiers_identifier = TermsFacet(
    field="metadata.creators.authorityIdentifiers.identifier",
    label=_("metadata.creators.authorityIdentifiers.identifier.label"),
)


metadata_creators_authorityIdentifiers_scheme = TermsFacet(
    field="metadata.creators.authorityIdentifiers.scheme",
    label=_("metadata.creators.authorityIdentifiers.scheme.label"),
)


metadata_contributors_role_id = TermsFacet(
    field="metadata.contributors.role.id",
    label=_("metadata.contributors.role.id.label"),
)


metadata_contributors_role_type = TermsFacet(
    field="metadata.contributors.role.type",
    label=_("metadata.contributors.role.type.label"),
)


metadata_contributors_role__version = TermsFacet(
    field="metadata.contributors.role.@v",
    label=_("metadata.contributors.role.@v.label"),
)


metadata_contributors_affiliations_id = TermsFacet(
    field="metadata.contributors.affiliations.id",
    label=_("metadata.contributors.affiliations.id.label"),
)


metadata_contributors_affiliations_type = TermsFacet(
    field="metadata.contributors.affiliations.type",
    label=_("metadata.contributors.affiliations.type.label"),
)


metadata_contributors_affiliations_hierarchy_parent = TermsFacet(
    field="metadata.contributors.affiliations.hierarchy.parent",
    label=_("metadata.contributors.affiliations.hierarchy.parent.label"),
)


metadata_contributors_affiliations_hierarchy_level = TermsFacet(
    field="metadata.contributors.affiliations.hierarchy.level",
    label=_("metadata.contributors.affiliations.hierarchy.level.label"),
)


metadata_contributors_affiliations_hierarchy_ancestors = TermsFacet(
    field="metadata.contributors.affiliations.hierarchy.ancestors",
    label=_("metadata.contributors.affiliations.hierarchy.ancestors.label"),
)


metadata_contributors_affiliations__version = TermsFacet(
    field="metadata.contributors.affiliations.@v",
    label=_("metadata.contributors.affiliations.@v.label"),
)


metadata_contributors_nameType = TermsFacet(
    field="metadata.contributors.nameType",
    label=_("metadata.contributors.nameType.label"),
)


metadata_contributors_fullName = TermsFacet(
    field="metadata.contributors.fullName",
    label=_("metadata.contributors.fullName.label"),
)


metadata_contributors_authorityIdentifiers_identifier = TermsFacet(
    field="metadata.contributors.authorityIdentifiers.identifier",
    label=_("metadata.contributors.authorityIdentifiers.identifier.label"),
)


metadata_contributors_authorityIdentifiers_scheme = TermsFacet(
    field="metadata.contributors.authorityIdentifiers.scheme",
    label=_("metadata.contributors.authorityIdentifiers.scheme.label"),
)


metadata_resourceType_id = TermsFacet(
    field="metadata.resourceType.id", label=_("metadata.resourceType.id.label")
)


metadata_resourceType_type = TermsFacet(
    field="metadata.resourceType.type", label=_("metadata.resourceType.type.label")
)


metadata_resourceType__version = TermsFacet(
    field="metadata.resourceType.@v", label=_("metadata.resourceType.@v.label")
)


metadata_dateAvailable = TermsFacet(
    field="metadata.dateAvailable", label=_("metadata.dateAvailable.label")
)


metadata_dateModified = TermsFacet(
    field="metadata.dateModified", label=_("metadata.dateModified.label")
)


metadata_subjects_subjectScheme = TermsFacet(
    field="metadata.subjects.subjectScheme",
    label=_("metadata.subjects.subjectScheme.label"),
)


metadata_subjects_subject_lang = NestedLabeledFacet(
    path="metadata.subjects.subject",
    nested_facet=TermsFacet(
        field="metadata.subjects.subject.lang",
        label=_("metadata.subjects.subject.lang.label"),
    ),
)


metadata_subjects_subject_cs_keyword = TermsFacet(
    field="metadata.subjects.subject_cs.keyword"
)


metadata_subjects_subject_en_keyword = TermsFacet(
    field="metadata.subjects.subject_en.keyword"
)


metadata_subjects_subject_value_keyword = NestedLabeledFacet(
    path="metadata.subjects.subject",
    nested_facet=TermsFacet(
        field="metadata.subjects.subject.value.keyword",
        label=_("metadata.subjects.subject.value.keyword.label"),
    ),
)


metadata_subjects_valueURI = TermsFacet(
    field="metadata.subjects.valueURI", label=_("metadata.subjects.valueURI.label")
)


metadata_subjects_classificationCode = TermsFacet(
    field="metadata.subjects.classificationCode",
    label=_("metadata.subjects.classificationCode.label"),
)


metadata_subjectCategories_id = TermsFacet(
    field="metadata.subjectCategories.id",
    label=_("metadata.subjectCategories.id.label"),
)


metadata_subjectCategories_type = TermsFacet(
    field="metadata.subjectCategories.type",
    label=_("metadata.subjectCategories.type.label"),
)


metadata_subjectCategories__version = TermsFacet(
    field="metadata.subjectCategories.@v",
    label=_("metadata.subjectCategories.@v.label"),
)


metadata_languages_id = TermsFacet(
    field="metadata.languages.id", label=_("metadata.languages.id.label")
)


metadata_languages_type = TermsFacet(
    field="metadata.languages.type", label=_("metadata.languages.type.label")
)


metadata_languages__version = TermsFacet(
    field="metadata.languages.@v", label=_("metadata.languages.@v.label")
)


metadata_abstract_lang = NestedLabeledFacet(
    path="metadata.abstract",
    nested_facet=TermsFacet(
        field="metadata.abstract.lang", label=_("metadata.abstract.lang.label")
    ),
)


metadata_abstract_cs_keyword = TermsFacet(field="metadata.abstract_cs.keyword")


metadata_abstract_en_keyword = TermsFacet(field="metadata.abstract_en.keyword")


metadata_abstract_value_keyword = NestedLabeledFacet(
    path="metadata.abstract",
    nested_facet=TermsFacet(
        field="metadata.abstract.value.keyword",
        label=_("metadata.abstract.value.keyword.label"),
    ),
)


metadata_methods_lang = NestedLabeledFacet(
    path="metadata.methods",
    nested_facet=TermsFacet(
        field="metadata.methods.lang", label=_("metadata.methods.lang.label")
    ),
)


metadata_methods_cs_keyword = TermsFacet(field="metadata.methods_cs.keyword")


metadata_methods_en_keyword = TermsFacet(field="metadata.methods_en.keyword")


metadata_methods_value_keyword = NestedLabeledFacet(
    path="metadata.methods",
    nested_facet=TermsFacet(
        field="metadata.methods.value.keyword",
        label=_("metadata.methods.value.keyword.label"),
    ),
)


metadata_technicalInfo_lang = NestedLabeledFacet(
    path="metadata.technicalInfo",
    nested_facet=TermsFacet(
        field="metadata.technicalInfo.lang",
        label=_("metadata.technicalInfo.lang.label"),
    ),
)


metadata_technicalInfo_cs_keyword = TermsFacet(
    field="metadata.technicalInfo_cs.keyword"
)


metadata_technicalInfo_en_keyword = TermsFacet(
    field="metadata.technicalInfo_en.keyword"
)


metadata_technicalInfo_value_keyword = NestedLabeledFacet(
    path="metadata.technicalInfo",
    nested_facet=TermsFacet(
        field="metadata.technicalInfo.value.keyword",
        label=_("metadata.technicalInfo.value.keyword.label"),
    ),
)


metadata_rights_id = TermsFacet(
    field="metadata.rights.id", label=_("metadata.rights.id.label")
)


metadata_rights_type = TermsFacet(
    field="metadata.rights.type", label=_("metadata.rights.type.label")
)


metadata_rights__version = TermsFacet(
    field="metadata.rights.@v", label=_("metadata.rights.@v.label")
)


metadata_accessRights_id = TermsFacet(
    field="metadata.accessRights.id", label=_("metadata.accessRights.id.label")
)


metadata_accessRights_type = TermsFacet(
    field="metadata.accessRights.type", label=_("metadata.accessRights.type.label")
)


metadata_accessRights__version = TermsFacet(
    field="metadata.accessRights.@v", label=_("metadata.accessRights.@v.label")
)


metadata_relatedItems_itemCreators_affiliations_id = TermsFacet(
    field="metadata.relatedItems.itemCreators.affiliations.id",
    label=_("metadata.relatedItems.itemCreators.affiliations.id.label"),
)


metadata_relatedItems_itemCreators_affiliations_type = TermsFacet(
    field="metadata.relatedItems.itemCreators.affiliations.type",
    label=_("metadata.relatedItems.itemCreators.affiliations.type.label"),
)


metadata_relatedItems_itemCreators_affiliations_hierarchy_parent = TermsFacet(
    field="metadata.relatedItems.itemCreators.affiliations.hierarchy.parent",
    label=_("metadata.relatedItems.itemCreators.affiliations.hierarchy.parent.label"),
)


metadata_relatedItems_itemCreators_affiliations_hierarchy_level = TermsFacet(
    field="metadata.relatedItems.itemCreators.affiliations.hierarchy.level",
    label=_("metadata.relatedItems.itemCreators.affiliations.hierarchy.level.label"),
)


metadata_relatedItems_itemCreators_affiliations_hierarchy_ancestors = TermsFacet(
    field="metadata.relatedItems.itemCreators.affiliations.hierarchy.ancestors",
    label=_(
        "metadata.relatedItems.itemCreators.affiliations.hierarchy.ancestors.label"
    ),
)


metadata_relatedItems_itemCreators_affiliations__version = TermsFacet(
    field="metadata.relatedItems.itemCreators.affiliations.@v",
    label=_("metadata.relatedItems.itemCreators.affiliations.@v.label"),
)


metadata_relatedItems_itemCreators_nameType = TermsFacet(
    field="metadata.relatedItems.itemCreators.nameType",
    label=_("metadata.relatedItems.itemCreators.nameType.label"),
)


metadata_relatedItems_itemCreators_fullName = TermsFacet(
    field="metadata.relatedItems.itemCreators.fullName",
    label=_("metadata.relatedItems.itemCreators.fullName.label"),
)


metadata_relatedItems_itemCreators_authorityIdentifiers_identifier = TermsFacet(
    field="metadata.relatedItems.itemCreators.authorityIdentifiers.identifier",
    label=_("metadata.relatedItems.itemCreators.authorityIdentifiers.identifier.label"),
)


metadata_relatedItems_itemCreators_authorityIdentifiers_scheme = TermsFacet(
    field="metadata.relatedItems.itemCreators.authorityIdentifiers.scheme",
    label=_("metadata.relatedItems.itemCreators.authorityIdentifiers.scheme.label"),
)


metadata_relatedItems_itemContributors_role_id = TermsFacet(
    field="metadata.relatedItems.itemContributors.role.id",
    label=_("metadata.relatedItems.itemContributors.role.id.label"),
)


metadata_relatedItems_itemContributors_role_type = TermsFacet(
    field="metadata.relatedItems.itemContributors.role.type",
    label=_("metadata.relatedItems.itemContributors.role.type.label"),
)


metadata_relatedItems_itemContributors_role__version = TermsFacet(
    field="metadata.relatedItems.itemContributors.role.@v",
    label=_("metadata.relatedItems.itemContributors.role.@v.label"),
)


metadata_relatedItems_itemContributors_affiliations_id = TermsFacet(
    field="metadata.relatedItems.itemContributors.affiliations.id",
    label=_("metadata.relatedItems.itemContributors.affiliations.id.label"),
)


metadata_relatedItems_itemContributors_affiliations_type = TermsFacet(
    field="metadata.relatedItems.itemContributors.affiliations.type",
    label=_("metadata.relatedItems.itemContributors.affiliations.type.label"),
)


metadata_relatedItems_itemContributors_affiliations_hierarchy_parent = TermsFacet(
    field="metadata.relatedItems.itemContributors.affiliations.hierarchy.parent",
    label=_(
        "metadata.relatedItems.itemContributors.affiliations.hierarchy.parent.label"
    ),
)


metadata_relatedItems_itemContributors_affiliations_hierarchy_level = TermsFacet(
    field="metadata.relatedItems.itemContributors.affiliations.hierarchy.level",
    label=_(
        "metadata.relatedItems.itemContributors.affiliations.hierarchy.level.label"
    ),
)


metadata_relatedItems_itemContributors_affiliations_hierarchy_ancestors = TermsFacet(
    field="metadata.relatedItems.itemContributors.affiliations.hierarchy.ancestors",
    label=_(
        "metadata.relatedItems.itemContributors.affiliations.hierarchy.ancestors.label"
    ),
)


metadata_relatedItems_itemContributors_affiliations__version = TermsFacet(
    field="metadata.relatedItems.itemContributors.affiliations.@v",
    label=_("metadata.relatedItems.itemContributors.affiliations.@v.label"),
)


metadata_relatedItems_itemContributors_nameType = TermsFacet(
    field="metadata.relatedItems.itemContributors.nameType",
    label=_("metadata.relatedItems.itemContributors.nameType.label"),
)


metadata_relatedItems_itemContributors_fullName = TermsFacet(
    field="metadata.relatedItems.itemContributors.fullName",
    label=_("metadata.relatedItems.itemContributors.fullName.label"),
)


metadata_relatedItems_itemContributors_authorityIdentifiers_identifier = TermsFacet(
    field="metadata.relatedItems.itemContributors.authorityIdentifiers.identifier",
    label=_(
        "metadata.relatedItems.itemContributors.authorityIdentifiers.identifier.label"
    ),
)


metadata_relatedItems_itemContributors_authorityIdentifiers_scheme = TermsFacet(
    field="metadata.relatedItems.itemContributors.authorityIdentifiers.scheme",
    label=_("metadata.relatedItems.itemContributors.authorityIdentifiers.scheme.label"),
)


metadata_relatedItems_itemPIDs_identifier = TermsFacet(
    field="metadata.relatedItems.itemPIDs.identifier",
    label=_("metadata.relatedItems.itemPIDs.identifier.label"),
)


metadata_relatedItems_itemPIDs_scheme = TermsFacet(
    field="metadata.relatedItems.itemPIDs.scheme",
    label=_("metadata.relatedItems.itemPIDs.scheme.label"),
)


metadata_relatedItems_itemURL = TermsFacet(
    field="metadata.relatedItems.itemURL",
    label=_("metadata.relatedItems.itemURL.label"),
)


metadata_relatedItems_itemYear = TermsFacet(
    field="metadata.relatedItems.itemYear",
    label=_("metadata.relatedItems.itemYear.label"),
)


metadata_relatedItems_itemVolume = TermsFacet(
    field="metadata.relatedItems.itemVolume",
    label=_("metadata.relatedItems.itemVolume.label"),
)


metadata_relatedItems_itemIssue = TermsFacet(
    field="metadata.relatedItems.itemIssue",
    label=_("metadata.relatedItems.itemIssue.label"),
)


metadata_relatedItems_itemStartPage = TermsFacet(
    field="metadata.relatedItems.itemStartPage",
    label=_("metadata.relatedItems.itemStartPage.label"),
)


metadata_relatedItems_itemEndPage = TermsFacet(
    field="metadata.relatedItems.itemEndPage",
    label=_("metadata.relatedItems.itemEndPage.label"),
)


metadata_relatedItems_itemPublisher = TermsFacet(
    field="metadata.relatedItems.itemPublisher",
    label=_("metadata.relatedItems.itemPublisher.label"),
)


metadata_relatedItems_itemRelationType_id = TermsFacet(
    field="metadata.relatedItems.itemRelationType.id",
    label=_("metadata.relatedItems.itemRelationType.id.label"),
)


metadata_relatedItems_itemRelationType_type = TermsFacet(
    field="metadata.relatedItems.itemRelationType.type",
    label=_("metadata.relatedItems.itemRelationType.type.label"),
)


metadata_relatedItems_itemRelationType__version = TermsFacet(
    field="metadata.relatedItems.itemRelationType.@v",
    label=_("metadata.relatedItems.itemRelationType.@v.label"),
)


metadata_relatedItems_itemResourceType_id = TermsFacet(
    field="metadata.relatedItems.itemResourceType.id",
    label=_("metadata.relatedItems.itemResourceType.id.label"),
)


metadata_relatedItems_itemResourceType_type = TermsFacet(
    field="metadata.relatedItems.itemResourceType.type",
    label=_("metadata.relatedItems.itemResourceType.type.label"),
)


metadata_relatedItems_itemResourceType__version = TermsFacet(
    field="metadata.relatedItems.itemResourceType.@v",
    label=_("metadata.relatedItems.itemResourceType.@v.label"),
)


metadata_fundingReferences_projectID = TermsFacet(
    field="metadata.fundingReferences.projectID",
    label=_("metadata.fundingReferences.projectID.label"),
)


metadata_fundingReferences_funder_id = TermsFacet(
    field="metadata.fundingReferences.funder.id",
    label=_("metadata.fundingReferences.funder.id.label"),
)


metadata_fundingReferences_funder_type = TermsFacet(
    field="metadata.fundingReferences.funder.type",
    label=_("metadata.fundingReferences.funder.type.label"),
)


metadata_fundingReferences_funder__version = TermsFacet(
    field="metadata.fundingReferences.funder.@v",
    label=_("metadata.fundingReferences.funder.@v.label"),
)


metadata_version = TermsFacet(
    field="metadata.version", label=_("metadata.version.label")
)


metadata_geoLocations_geoLocationPlace = TermsFacet(
    field="metadata.geoLocations.geoLocationPlace",
    label=_("metadata.geoLocations.geoLocationPlace.label"),
)


metadata_geoLocations_geoLocationPoint_pointLongitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPoint.pointLongitude",
    label=_("metadata.geoLocations.geoLocationPoint.pointLongitude.label"),
)


metadata_geoLocations_geoLocationPoint_pointLatitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPoint.pointLatitude",
    label=_("metadata.geoLocations.geoLocationPoint.pointLatitude.label"),
)


metadata_accessibility_lang = NestedLabeledFacet(
    path="metadata.accessibility",
    nested_facet=TermsFacet(
        field="metadata.accessibility.lang",
        label=_("metadata.accessibility.lang.label"),
    ),
)


metadata_accessibility_cs_keyword = TermsFacet(
    field="metadata.accessibility_cs.keyword"
)


metadata_accessibility_en_keyword = TermsFacet(
    field="metadata.accessibility_en.keyword"
)


metadata_accessibility_value_keyword = NestedLabeledFacet(
    path="metadata.accessibility",
    nested_facet=TermsFacet(
        field="metadata.accessibility.value.keyword",
        label=_("metadata.accessibility.value.keyword.label"),
    ),
)


metadata_series_seriesTitle = TermsFacet(
    field="metadata.series.seriesTitle", label=_("metadata.series.seriesTitle.label")
)


metadata_series_seriesVolume = TermsFacet(
    field="metadata.series.seriesVolume", label=_("metadata.series.seriesVolume.label")
)


metadata_externalLocation_externalLocationURL = TermsFacet(
    field="metadata.externalLocation.externalLocationURL",
    label=_("metadata.externalLocation.externalLocationURL.label"),
)


metadata_originalRecord = TermsFacet(
    field="metadata.originalRecord", label=_("metadata.originalRecord.label")
)


metadata_objectIdentifiers_identifier = TermsFacet(
    field="metadata.objectIdentifiers.identifier",
    label=_("metadata.objectIdentifiers.identifier.label"),
)


metadata_objectIdentifiers_scheme = TermsFacet(
    field="metadata.objectIdentifiers.scheme",
    label=_("metadata.objectIdentifiers.scheme.label"),
)


metadata_systemIdentifiers_identifier = TermsFacet(
    field="metadata.systemIdentifiers.identifier",
    label=_("metadata.systemIdentifiers.identifier.label"),
)


metadata_systemIdentifiers_scheme = TermsFacet(
    field="metadata.systemIdentifiers.scheme",
    label=_("metadata.systemIdentifiers.scheme.label"),
)


metadata_events_eventDate = TermsFacet(
    field="metadata.events.eventDate", label=_("metadata.events.eventDate.label")
)


metadata_events_eventLocation_place = TermsFacet(
    field="metadata.events.eventLocation.place",
    label=_("metadata.events.eventLocation.place.label"),
)


metadata_events_eventLocation_country_id = TermsFacet(
    field="metadata.events.eventLocation.country.id",
    label=_("metadata.events.eventLocation.country.id.label"),
)


metadata_events_eventLocation_country_type = TermsFacet(
    field="metadata.events.eventLocation.country.type",
    label=_("metadata.events.eventLocation.country.type.label"),
)


metadata_events_eventLocation_country__version = TermsFacet(
    field="metadata.events.eventLocation.country.@v",
    label=_("metadata.events.eventLocation.country.@v.label"),
)


_id = TermsFacet(field="id", label=_("id.label"))


created = TermsFacet(field="created", label=_("created.label"))


updated = TermsFacet(field="updated", label=_("updated.label"))


_schema = TermsFacet(field="$schema", label=_("$schema.label"))

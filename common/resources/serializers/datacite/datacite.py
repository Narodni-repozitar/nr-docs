from invenio_access.permissions import system_identity
from invenio_vocabularies.proxies import current_service as vocabulary_service
from babel_edtf import parse_edtf


def generate_datacite(json_data):
    metadata = json_data["metadata"]
    creators = creatibutor(metadata, "creators")
    titles = title(metadata)
    publishers = publisher(metadata)

    dc_resource_type = resource_type(metadata)

    payload = {}
    payload["creators"] = creators
    payload["titles"] = titles
    payload["publisher"] = publishers
    payload["types"] = {}
    payload["types"]["resourceTypeGeneral"] = dc_resource_type

    # optional
    if "subjects" in metadata:
        dc_subjects = subjects(metadata)
        payload["subjects"] = dc_subjects
    if "contributors" in metadata:
        dc_contributors = creatibutor(metadata, "contributors")
        payload["contributors"] = dc_contributors

    date_obj = parse_edtf(metadata["dateIssued"])

    year = date_obj.year

    payload["publicationYear"] = year

    dc_dates = []
    if "dateAvailable" in metadata:
        dc_dates.append(
            {"date": metadata["dateAvailable"], "dateType": "Available"}
        )
    if "dateModified" in metadata:
        dc_dates.append({"date": metadata["dateModified"], "dateType": "Updated"})
    if "dateIssued" in metadata:
        dc_dates.append({"date": metadata["dateIssued"], "dateType": "Issued"})
    if len(dc_dates) > 0:
        payload["dates"] = dc_dates

    if "rights" in metadata:
        dc_rights = []
        right = metadata["rights"]
        dc_rights.append(
            {"rights": right["title"], "rightsIdentifier": right["id"]}
        )
        if len(dc_rights) > 0:
            payload["rightsList"] = dc_rights
    if "abstract" in metadata:
        dc_descriptions = []
        for abstr in metadata["abstract"]:
            dc_descriptions.append(
                {
                    "lang": abstr["lang"],
                    "description": abstr["value"],
                    "descriptionType": "Abstract",
                }
            )
        if len(dc_descriptions) > 0:
            payload["descriptions"] = dc_descriptions

    if "funders" in metadata:
        payload["fundingReferences"] = funder(metadata)

    if "relatedItems" in metadata:
        payload["relatedItems"], payload["relatedIdentifiers"] = related_items(
            metadata
        )

    if "languages" in metadata:
        payload["language"] = metadata["languages"][0]["id"]

    return payload
def publisher(data):
    if "publishers" in data:
        return data["publishers"][0]


def resource_type(data):
    if "resourceType" in data:
        voc = vocabulary_service.read(
            system_identity, ("resource-types", data["resourceType"]["id"])
        )
        return voc.data["props"]["dataCiteType"]


def subjects(data):
    dc_subjects = []
    for sub in data["subjects"]:
        if "subject" in sub:
            for s in sub["subject"]:
                dc_sub = {}
                if "value" in s:
                    dc_sub["subject"] = s["value"]
                if "lang" in s:
                    dc_sub["lang"] = s["lang"]
                if dc_sub != {}:
                    dc_sub["subjectScheme"] = "keyword"
                    dc_subjects.append(dc_sub)
    return dc_subjects


def title(data):
    datacite_titles = []
    if "title" in data:
        title_def = data["title"]
        datacite_titles.append({"title": title_def})
    if "additionalTitles" in data:
        for add_title in data["additionalTitles"]:
            additional_datacite_title = {}
            if "title" in add_title:
                additional_datacite_title["lang"] = add_title["title"]["lang"]
                additional_datacite_title["title"] = add_title["title"]["value"]
            if "titleType" in add_title:
                additional_datacite_title["titleType"] = (
                    add_title["titleType"][0].upper() + add_title["titleType"][1:]
                )
            if additional_datacite_title != {}:
                datacite_titles.append(additional_datacite_title)

    return datacite_titles


def creatibutor(data, type):
    creatibutor_def = data[type]
    datacite_creatibutors = []
    for creatibutor in creatibutor_def:
        datacite_creatibutor = {}
        if "name" in creatibutor["person_or_org"]:  # required
            datacite_creatibutor["name"] = creatibutor["person_or_org"]["name"]
        if "type" in creatibutor["person_or_org"]:
            datacite_creatibutor["nameType"] = creatibutor["person_or_org"]["type"].capitalize()
        if "role" in creatibutor:
            voc = vocabulary_service.read(
                system_identity,
                ("contributor-types", creatibutor["role"]["id"]),
            )
            if "dataCiteCode" in voc.data["props"]:
                contr_type = voc.data["props"]["dataCiteCode"]
            else:
                contr_type = "Other"
            datacite_creatibutor["contributorType"] = contr_type
        if "identifiers" in creatibutor["person_or_org"]:
            creatibutors_ids = []
            for id in creatibutor["person_or_org"]["identifiers"]:
                creatibutor_id = {}
                if "scheme" in id:  # required
                    creatibutor_id["nameIdentifierScheme"] = id["scheme"]
                if "identifier" in id:
                    creatibutor_id["nameIdentifier"] = id["identifier"]
                if creatibutor_id != {}:
                    creatibutors_ids.append(creatibutor_id)
            if len(creatibutors_ids) > 0:
                datacite_creatibutor["nameIdentifiers"] = creatibutors_ids
        datacite_creatibutors.append(datacite_creatibutor)
    return datacite_creatibutors


def funder(data):
    funders_def = data["funders"]
    dc_funders = []
    for f in funders_def:
        dc_funder = {}
        if "funder" in f:
            voc = vocabulary_service.read(
                system_identity,
                ("funders", f["funder"]["id"]),
            )
            if "name" in voc.data:

                dc_funder["funderName"] = voc.data["name"]

        if "award" in f:
            if "title" in f["award"]:
                value = next(iter(f["award"]["title"].values()))
                dc_funder["awardTitle"] = value
            if "number" in f["award"]:
                dc_funder["awardNumber"] = f["award"]["number"]
        dc_funders.append(dc_funder)
    return dc_funders


def related_items(data):
    dc_related_items = []
    related_items_def = data["relatedItems"]
    dc_related_identifiers = []
    for rel in related_items_def:
        dc_rel = {}
        if "itemContributors" in rel:
            dc_rel["contributors"] = creatibutor(rel, "itemContributors")
        if "itemCreators" in rel:
            dc_rel["creators"] = creatibutor(rel, "itemCreators")
        if "itemRelationType" in rel:
            dc_rel["relationType"] = (
                rel["itemRelationType"]["id"][0].upper()
                + rel["itemRelationType"]["id"][1:]
            )
        if "itemResourceType" in rel:
            voc = vocabulary_service.read(
                system_identity, ("resource-types", rel["itemResourceType"]["id"])
            )
            dc_rel["relatedItemType"] = voc.data["props"]["dataCiteType"]
        if "itemPIDs" in rel:
            identifier_definition = {}
            for identifier in rel["itemPIDs"]:
                if "identifier" in identifier and "scheme" in identifier:
                    if identifier["scheme"] == "DOI":
                        identifier_definition["relatedItemIdentifier"] = identifier[
                            "identifier"
                        ]
                        identifier_definition["relatedItemIdentifierType"] = identifier[
                            "scheme"
                        ]
                        break
                    elif identifier_definition == {} and identifier["scheme"] != "RIV":
                        identifier_definition["relatedItemIdentifier"] = identifier[
                            "identifier"
                        ]
                        identifier_definition["relatedItemIdentifierType"] = identifier[
                            "scheme"
                        ]
                    else:
                        continue
            if identifier_definition != {}:
                if "relationType" in dc_rel and "relatedItemType" in dc_rel:
                    dc_related_identifiers.append(
                        {
                            "relationType": dc_rel["relationType"],
                            "relatedIdentifier": identifier_definition[
                                "relatedItemIdentifier"
                            ],
                            "relatedIdentifierType": identifier_definition[
                                "relatedItemIdentifierType"
                            ],
                            "resourceTypeGeneral": dc_rel["relatedItemType"],
                        }
                    )

                dc_rel["relatedItemIdentifier"] = identifier_definition
        if "itemStartPage" in rel:
            dc_rel["firstPage"] = rel["itemStartPage"]
        if "itemEndPage" in rel:
            dc_rel["lastPage"] = rel["itemEndPage"]
        if "itemIssue" in rel:
            dc_rel["issue"] = rel["itemIssue"]
        if "itemTitle" in rel:
            dc_rel["title"] = {"title": rel["itemTitle"]}
        if "itemVolume" in rel:
            dc_rel["volume "] = rel["itemVolume"]
        if "itemYear" in rel:
            dc_rel["PublicationYear"] = rel["itemYear"]

        if dc_rel != {}:
            dc_related_items.append(dc_rel)
    return dc_related_items, dc_related_identifiers

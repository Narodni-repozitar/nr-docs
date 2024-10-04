from datetime import datetime
from invenio_access.permissions import system_identity
from invenio_vocabularies.proxies import current_service as vocabulary_service


class DataCiteMappingNRDocs:

        def metadata_check(self, data):
        errors = {}
        data = data["metadata"]
        if "creators" not in data:
            errors["metadata.creators"] = ["Creators are mandatory"]
        else:
            for i, creator in enumerate(data["creators"]):
                if "fullName" not in creator:
                    errors["metadata.creators[{i}].fullName"] = ["Full name of creator is mandatory"]
                if "authorityIdentifiers" in creator:
                    for j, id in enumerate(creator["authorityIdentifiers"]):
                        if "scheme" not in id:
                            errors["metadata.creators[{i}].authorityIdentifiers[{j}].scheme"] = [
                                "Authority identifier scheme is mandatory"]
        if "contributors" in data:
            for i, contributor in enumerate(data["contributors"]):
                if "fullName" not in contributor:
                    errors["metadata.contributors[{i}].fullName"] = [
                        "Full name of contributor is mandatory"]
                if "authorityIdentifiers" in contributor:
                    for j, id in enumerate(contributor["authorityIdentifiers"]):
                        if "scheme" not in id:
                            errors["metadata.contributors[{i}].authorityIdentifiers[{j}].scheme"] = [
                                "Authority identifier scheme is mandatory"]
        if "title" not in data:
            errors["metadata.title"] = ["Title is mandatory"]
        if "resourceType" not in data:
            errors["metadata.resourceType"] = ["Resource type is mandatory"]
        if "dateIssued" not in data:
            errors["metadata.dateIssued"] = ["Date issued is mandatory"]
        if "fundingReferences" in data:
            for i, fund in enumerate(data["fundingReferences"]):
                if "projectName" not in fund:
                    errors["metadata.fundingReferences[{i}].projectName"] = ["Funder name is mandatory"]

        return errors

    def create_datacite_payload(self, data):
        # mandatory
        metadata = data["metadata"]
        creators = creatibutor(metadata, "creators")
        titles = title(metadata)
        # publishers = publisher(data)

        #todo: what is the correct value here? if it should be from the record data - check also needs to be added since publisher field is mandatory in DC
        publishers = "NTK"

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


        date_obj = datetime.strptime(metadata['dateIssued'], '%Y-%m-%d')
        year = date_obj.year
        
        payload["publicationYear"] = year
        payload["url"] = data['links']['self']

        dc_dates = []
        if "dateAvailable" in metadata:
            dc_dates.append({"date": metadata["dateAvailable"], "dateType": "Available"})
        if "dateModified" in metadata:
            dc_dates.append({"date": metadata["dateModified"], "dateType": "Updated"})
        if "dateIssued" in metadata:
            dc_dates.append({"date": metadata["dateIssued"], "dateType": "Issued"})
        if len(dc_dates) > 0:
            payload["dates"] = dc_dates

        if "rights" in metadata:
            dc_rights = []
            right = metadata["rights"]
            dc_rights.append({"rights": right["title"], "rightsIdentifier": right["id"]})
            if len(dc_rights) > 0:
                payload ["rightsList"] = dc_rights
        if "abstract" in metadata:
            dc_descriptions = []
            for abstr in metadata["abstract"]:
                dc_descriptions.append(
                    {"lang": abstr["lang"], "description": abstr["value"], "descriptionType": "Abstract"})
            if len(dc_descriptions) > 0:
                payload["descriptions"] = dc_descriptions

        if "fundingReferences" in metadata:
            payload["FundingReference"] = funder(metadata)

        if "relatedItems" in metadata:
            payload["relatedItems"] = related_items(metadata)

        if "languages" in metadata:
            payload["language"] = metadata["languages"][0]["id"]

        return payload

    def get_doi(self, record):
        object_identifiers = record["metadata"].get("objectIdentifiers", [])
        doi = None
        for id in object_identifiers:
            if id["scheme"] == "DOI":
                doi = id["identifier"]
        return doi

    def add_doi(self, record, data,  doi_value):
        doi = {"scheme": "DOI", "identifier": doi_value}

        if "objectIdentifiers" in data["metadata"]:
            data["metadata"]["objectIdentifiers"].append(doi)
        else:
            data["metadata"]["objectIdentifiers"] = [doi]

        record.update(data)
        record.commit()




def publisher(data):
    if "publishers" in data:
        return data["publishers"][0]

def resource_type(data):
    if "resourceType" in data:
        voc = vocabulary_service.read(system_identity, ('resource-types', data["resourceType"]["id"]))
        return voc.data['props']['dataCiteType']

def subjects(data):
    dc_subjects = []
    for sub in data["subjects"]:
        dc_sub = {}
        if "subject" in sub:
            dc_sub["subject"] = sub["subject"][0]["value"]
        if "subjectScheme" in sub:
            dc_sub["subjectScheme"] = sub["subjectScheme"]
        if dc_sub != {}:
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
                additional_datacite_title["titleType"] = add_title["titleType"][0].upper() + add_title["titleType"][1:]
            if additional_datacite_title != {}:
                datacite_titles.append(additional_datacite_title)

    return datacite_titles


def creatibutor(data, type):
    creatibutor_def = data[type]
    datacite_creatibutors = []
    for creatibutor in creatibutor_def:
        datacite_creatibutor = {}
        if "fullName" in creatibutor: #required
            datacite_creatibutor["name"] = creatibutor["fullName"]
        if "nameType" in creatibutor:
            datacite_creatibutor["nameType"] = creatibutor["nameType"]
        if "contributorType" in creatibutor:
            voc = vocabulary_service.read(system_identity, ('contributor-types', creatibutor["contributorType"]["id"]))
            if 'dataCiteType' in voc.data['props']:
                contr_type = voc.data['props']['dataCiteType']
            else:
                contr_type = "Other"
            datacite_creatibutor["contributorType"] = contr_type
        if "authorityIdentifiers" in creatibutor:
            creatibutors_ids = []
            for id in creatibutor["authorityIdentifiers"]:
                creatibutor_id = {}
                if "scheme" in id: #required
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
    funders_def = data["fundingReferences"]
    dc_funders = []
    for f in funders_def:
        dc_funder = {}
        if "funder" in f:
            dc_funder["funderName"] = f["funder"]
        dc_funders.append(dc_funder)
    return dc_funders

def related_items(data):
    dc_related_items = []
    related_items_def = data["relatedItems"]
    for rel in related_items_def:
        dc_rel = {}
        if "itemContributors" in rel:
            dc_rel["contributors"] = creatibutor(rel, "itemContributors")
        if "itemCreators" in rel:
            dc_rel["creators"] = creatibutor(rel, "itemCreators")
        if "itemRelationType" in rel:
            dc_rel["relationType"] = rel["itemRelationType"]["id"][0].upper() + rel["itemRelationType"]["id"][1:]
        if "itemResourceType" in rel:
            voc = vocabulary_service.read(system_identity, ('resource-types', rel["itemResourceType"]["id"]))
            dc_rel["relatedItemType"] = voc.data['props']['dataCiteType']
        if "itemStartPage" in rel:
            dc_rel["firstPage"] = rel["itemStartPage"]
        if "itemEndPage" in rel:
            dc_rel["lastPage"] = rel["itemEndPage"]
        if "itemIssue" in rel:
            dc_rel["issue"] = rel["itemIssue"]
        if "itemTitle" in rel:
            dc_rel["Title"] = {"title" : rel["itemTitle"]}
        if "itemVolume" in rel:
            dc_rel["volume "] = rel["itemVolume"]
        if "itemYear" in rel:
            dc_rel["PublicationYear"] = rel["itemYear"]

        if dc_rel != {}:
            dc_related_items.append(dc_rel)
    return dc_related_items


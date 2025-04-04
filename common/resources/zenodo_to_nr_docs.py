import re
from datetime import datetime
from urllib.parse import urlparse

from flask_resources import RequestBodyParser, JSONDeserializer


class ZenodoRequestBodyParser(RequestBodyParser):

    def parse(self):
        """Parse the request body."""
        json = super().parse()
        return zenodo_to_nr_docs(json)


REQUEST_BODY_PARSERS = {
    'application/zenodo+json': ZenodoRequestBodyParser(JSONDeserializer()),
}


def zenodo_to_nr_docs(zenodo_record):
    metadata = zenodo_record.get('metadata', {}).copy()

    nr_docs = {'languages': transform_languages(metadata)}

    # we will use it as default lang, because Zenodo does not have specified field for abstract/title etc.
    used_language = 'en'
    if nr_docs['languages']:
        used_language = nr_docs['languages'][0]['id']
    else:
        nr_docs['languages'] = [
            {'id': used_language}
        ]
    community = metadata['communities'][0]['identifier']

    transform_funcs = {
        'additionalTitles': transform_additional_titles,
        'relatedItems': transform_related_items,
        'rights': transform_rights,
        'subjects': transform_subjects,
        'creators': transform_creators,
        'contributors': transform_contributors,
        'notes': transform_notes,
        'title': transform_title,
        'accessibility': transform_accessibility,
        'publishers': transform_publishers,
        'dateIssued': transform_dates,
        'abstract': transform_abstract,
        'resourceType': transform_resource_type,
    }

    for key, func in transform_funcs.items():
        nr_docs[key] = func(metadata, used_language)

    return {'parent': {'communities': {'default': community}}, 'metadata': nr_docs}


def transform_subjects(rec, lang='en'):
    subjects = [
        {"subject": [{"lang": lang, "value": keyword}]}
        for keyword in rec.pop('keywords', [])
    ]
    return subjects


def transform_additional_titles(rec, lang='en'):
    return [
        {
            "title": {
                "lang": lang,
                "value": title.get("description", "")
            },
            "titleType": title.get("type", {}).get("id", "")
        }
        for title in rec.get('additional_descriptions', []) if title.get('type', {}).get('id', '') != 'notes'
    ]


def transform_relation_type(zenodo_relation_type):
    translations = {
        "collects": ("collects", "sbírá"),
        "compiles": ("compiles", "kompiluje (co)"),
        "continues": ("continues", "pokračuje (čím)"),
        "describes": ("describes", "popisuje (co)"),
        "documents": ("documents", "dokumentuje (co)"),
        "hasMetadata": ("has metadata", "má metadata"),
        "hasPart": ("has part", "má část/i"),
        "hasVersion": ("has version", "má verzi"),
        "isCitedBy": ("is cited by", "je citován (čím)"),
        "isCollectedBy": ("is collected by", "je sbírán (čím)"),
        "isCompiledBy": ("is compiled by", "kompilován (čím)"),
        "isContinuedBy": ("is continued by", "je pokračováním (čeho)"),
        "isDerivedFrom": ("is derived from", "je odvozen od (čeho)"),
        "isDescribedBy": ("is described by", "je popsán (čím)"),
        "isDocumentedBy": ("is documented by", "je zdokumentován (čím)"),
        "isIdenticalTo": ("is identical to", "je identický s"),
        "isMetadataFor": ("is metadata for", "je metadaty pro"),
        "isNewVersionOf": ("is new version of", "je novou verzí (čeho)"),
        "isObsoletedBy": ("is obsoleted by", "je nahrazen (čím)"),
        "isOriginalFormOf": ("is original form of", "je původní variantou (čeho)"),
        "isPartOf": ("is part of", "je součástí"),
        "isPreviousVersionOf": ("is previous version of", "je předchozí verzí (čeho)"),
        "isPublishedIn": ("is published in", "je publikován v"),
        "isReferencedBy": ("is referenced by", "je na něj odkazováno z (čeho)"),
        "isRequiredBy": ("is required by", "je požadován (čím)"),
        "isReviewedBy": ("is reviewed by", "je recenzován (čím)"),
        "isSourceOf": ("is source of", "je zdrojem odvozené verze"),
        "isSupplementTo": ("is supplement to", "je doplňkem k (čemu)"),
        "isSupplementedBy": ("is supplemented by", "má doplněk"),
        "isVariantFormOf": ("is variant form of", "je variantou (čeho)"),
        "isVersionOf": ("is version of", "je verzí"),
        "obsoletes": ("obsoletes", "nahrazuje (co)"),
        "references": ("references", "odkazuje (na co)"),
        "requires": ("requires", "požaduje (co)"),
        "reviews": ("reviews", "recenzuje (co)")
    }

    en, cs = translations.get(zenodo_relation_type, ("", ""))

    if en == '' and cs == '':
        raise ValueError(f"unknown relation type '{zenodo_relation_type}'")

    return {
        'id': zenodo_relation_type,
        'title': {
            'en': en,
            'cs': cs
        }
    }


def transform_related_items(rec, lang='en'):
    related_identifiers = rec.pop('related_identifiers', [])
    res = []
    index = 0
    for related_identifier in related_identifiers:
        related_item = {
            'itemTitle': f'Related Item {index + 1}.',  # necessary field in schema, but zenodo records does not have it
            'itemRelationType': transform_relation_type(related_identifier.get('relation'))
        }

        identifier = related_identifier.get('identifier')

        # if it is URL but not doi.org extract it, else try to extract identifier and scheme
        if related_identifier.get('scheme', "").upper() == 'URL' or (
                "http" in identifier and "doi" not in identifier):
            related_item['itemURL'] = related_identifier.pop('identifier')
        else:
            scheme, identifier = get_scheme_and_identifier(related_identifier)

            if not scheme:
                continue

            related_item['itemPIDs'] = [{
                'identifier': identifier,
                'scheme': scheme
            }]

        index += 1
        res.append(related_item)

    return res


def get_scheme_and_identifier(identifier):
    scheme = None

    if 'scheme' in identifier and identifier.get('scheme') != 'pmid':  # not supporing pmid scheme
        scheme = identifier['scheme'].upper()
    elif bool(re.match('^[0-9]{4}-[0-9]{3}[0-9X]$', identifier.get('identifier'))):
        scheme = 'ISSN'
    elif bool(re.match('(ISBN[-]*(1[03])*[ ]*(: ){0,1})*(([0-9Xx][- ]*){13}|([0-9Xx][- ]*){10})',
                       identifier.get('identifier'))):
        scheme = 'ISBN'
    elif 'doi' in identifier.get('identifier'):
        scheme = 'DOI'

    if scheme == 'DOI' and 'http' in identifier.get('identifier'):  # if is doi.org url
        return "DOI", extract_doi_from_url(identifier.get('identifier'))

    return scheme, identifier.get('identifier')


def extract_doi_from_url(url: str) -> str:
    doi_pattern = re.compile(r"10\.\d{4,9}/[^\s]+")

    match = doi_pattern.search(url)
    if match:
        return match.group(0)

    parsed_url = urlparse(url)
    match = doi_pattern.search(parsed_url.path)
    if match:
        return match.group(0)

    match = re.search(r"https://doi\.org/([^\s]+)", url)
    if match:
        return match.group(1)
    return ""


def transform_rights_to_ours(zenodo_rights):
    rights_mapping = {
        'cc-by-4.0': {'id': '4-BY', "title": {"en": "Creative Commons Attribution 4.0 International License"}},
        'cc-by-nc-nd-4.0': {'id': '4-BY-NC-ND', "title": {
            "en": "Creative Commons Attribution-NonCommercial-NoDerivs 4.0 International License"}},
        'cc-by-nc-4.0': {'id': '4-BY-NC',
                         "title": {"en": "Creative Commons Attribution-NonCommercial 4.0 International License"}},
        'other-nc': {},  # no alternative in our vocabulary
        'cc-by-3.0': {},  # no alternative in our vocabulary
        'cc-by-sa-4.0': {'id': '4-BY-SA',
                         "title": {"en": "Creative Commons Attribution-ShareAlike 4.0 International License"}},
        'cc-by-nc-nd-1.0': {'id': '1-BY-ND-NC',
                            "title": {"en": "Creative Commons Attribution-NoDerivs-NonCommercial 1.0 Generic License"}},
    }
    return rights_mapping.get(zenodo_rights, {})


def transform_rights(rec, lang='en'):
    rights = rec.pop('license', [])

    return transform_rights_to_ours(rights['id']) if rights else {}


def transform_person_or_org(creatibutor):
    if not creatibutor:
        return {}

    res = {"type": creatibutor.pop('type', "personal")}
    if creatibutor.get('orcid'):
        res['identifiers'] = [{
            'identifier': creatibutor.pop('orcid'),
            'scheme': 'orcid'
        }]

    name = creatibutor.pop("name")
    if ',' in name:
        family, given = name.split(",", 1)
        res.update({"given_name": given.strip(), "family_name": family.strip(), "name": name})
    else:
        first_name, surname = name.split(" ", 1)
        res.update({"family_name": surname, "given_name": first_name, "name": name})

    return res


def transform_creators(rec, lang='en'):
    return [transform_creatibutor(c) for c in rec.pop('creators', [])]


def transform_contributors(rec, lang='en'):
    return [transform_creatibutor(c) for c in rec.pop('contributors', [])]


def transform_creatibutor(creatibutor):
    res = {
        'person_or_org': transform_person_or_org(creatibutor)
    }
    if creatibutor.get("affiliation") and isinstance(creatibutor['affiliation'], str):
        res['affiliations'] = [{'name': creatibutor['affiliation']}]
    return res


def transform_notes(rec, lang='en'):
    notes = rec.pop('notes', [])
    res = []

    if isinstance(notes, str):
        return [notes]

    for note in notes:
        res.append(note)

    return res


def transform_title(record, lang='en'):
    return record.pop('title', '')


def transform_accessibility(rec, lang='en'):
    accessibility = rec.pop('access_right')
    return [{'lang': 'en', 'value': accessibility}] if accessibility else []


def transform_publishers(rec, lang='en'):
    publisher = rec.pop('publisher', 'Zenodo')
    return [publisher]


def transform_dates(record, lang='en'):
    return record.pop('publication_date', '')


def transform_abstract(record, lang='en'):
    abstract = record.pop('description', '')
    return [{'lang': lang, 'value': abstract}] if abstract else []


def transform_resource_type(rec, lang='en'):
    resource_type = rec.pop('resource_type', {})  # TODO add others
    if resource_type.get('type', {}) == 'other' or rec.get('publication_type', "") == 'other':
        return {'id': 'other', 'title': {'en': 'Other specialized materials'}}

    if resource_type.get('type', {}) == 'publication' or rec.get('publication_type', "") == 'article':
        return {'id': 'article', 'title': {'en': 'Journal article'}}
    return {}


def transform_languages(rec, lang='en'):
    langs = rec.pop('language', [])
    if isinstance(langs, str):
        return [check_language(langs)]

    res = []
    for lang_item in langs:
        res.append(check_language(lang_item))

    return res


def check_language(lang):
    if lang == 'eng':
        return {'id': 'en'}
    elif lang == 'ces':
        return {'id': 'cs'}
    else:
        return {'id': lang}


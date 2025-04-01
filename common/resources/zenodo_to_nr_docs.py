import re
from datetime import datetime

from flask_resources import RequestBodyParser, JSONDeserializer


class ZenodoRequestBodyParser(RequestBodyParser):

    def parse(self):
        """Parse the request body."""
        json = super().parse()
        return zenodo_to_nr_docs(json)

REQUEST_BODY_PARSERS = {
    'application/zenodo+json':  ZenodoRequestBodyParser(JSONDeserializer()),
}

def zenodo_to_nr_docs(zenodo_record):
    # nr_docs = {'originalRecord': zenodo_record['links']['self_html']} dont know if we pull directly from zenodo or not
    nr_docs = {}
    metadata = zenodo_record.get('metadata', {}).copy()

    nr_docs['languages'] = transform_languages(metadata)
    used_language = 'en'
    if nr_docs['languages']:
        used_language = nr_docs['languages'][0]['id']

    transform_funcs = {
        'dateModified': transform_date_modified,
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
        if key == 'dateModified':
            nr_docs[key] = func(zenodo_record, used_language)
            continue

        nr_docs[key] = func(metadata, used_language)

    return {'metadata': nr_docs}


def transform_date_modified(rec, lang='en'):
    timestamp = rec.get('modified')
    if not timestamp:
        return ""
    
    dt = datetime.fromisoformat(timestamp)
    date_part = dt.strftime("%Y-%m-%d")
    return date_part


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

    for index, related_identifier in enumerate(related_identifiers):
        related_item = {
            'itemTitle': f'Related Item {index + 1}.',
            'itemRelationType': transform_relation_type(related_identifier.get('relation'))
        }

        identifier = related_identifier.get('identifier')

        if related_identifier.get('scheme', "").upper() == 'URL' or "http" in identifier:
            related_item['itemURL'] = related_identifier.pop('identifier')
        else:
            related_item['itemPIDs'] = [
                {'identifier': identifier,
                 'scheme': get_scheme_from_identifier(related_identifier)
                 }]
        res.append(related_item)

    return res


def get_scheme_from_identifier(identifier):
    if 'scheme' in identifier:
        return identifier['scheme'].upper()

    if bool(re.match('^[0-9]{4}-[0-9]{3}[0-9X]$', identifier.get('identifier'))):
        return 'ISSN'
    elif bool(re.match('(ISBN[-]*(1[03])*[ ]*(: ){0,1})*(([0-9Xx][- ]*){13}|([0-9Xx][- ]*){10})', identifier.get('identifier'))):
        return 'ISBN'
    else:
        return 'unknown'

def transform_rights_to_ours(zenodo_rights):
    rights_mapping = {
        'cc-by-4.0': {'id': '4-BY', "title": {"en": "Creative Commons Attribution 4.0 International License"}},
        'cc-by-nc-nd-4.0': {'id': '4-BY-NC-ND', "title": {
            "en": "Creative Commons Attribution-NonCommercial-NoDerivs 4.0 International License"}},
        'cc-by-nc-4.0': {'id': '4-BY-NC',
                         "title": {"en": "Creative Commons Attribution-NonCommercial 4.0 International License"}},
        'other-nc': {},
        'cc-by-3.0': {},
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

    res = {"nameType": creatibutor.pop('type', "Personal").capitalize()}
    if creatibutor.get('orcid'):
        res['authorityIdentifiers'] = [{
            'identifier': creatibutor.pop('orcid'),
            'scheme': 'orcid'
        }]

    name = creatibutor.pop("name")
    if ',' in name:
        family, given = name.split(",", 1)
        res.update({"givenName": given.strip(), "familyName": family.strip(), "fullName": name})
    else:
        first_name, surname = name.split(" ", 1)
        res.update({"familyName": surname, "givenName": first_name, "fullName": name})

    return res


def transform_creators(rec, lang='en'):
    return [transform_creatibutor(c) for c in rec.pop('creators', [])]


def transform_contributors(rec, lang='en'):
    return [transform_creatibutor(c) for c in rec.pop('contributors', [])]


def transform_creatibutor(creatibutor):
    res = transform_person_or_org(creatibutor)
    if creatibutor.get("affiliation"):
        res['affiliations'] = transform_affiliations(creatibutor)
    return res


def transform_affiliations(rec):
    affiliations = rec.pop('affiliation', [])

    if isinstance(affiliations, str):
        aff = map_affiliation_by_name(affiliations)
        return [aff] if aff['id'] else []
    elif isinstance(affiliations, list):
        return transform_affiliation_list(affiliations)
    else:
        raise ValueError(f'affiliation not string or list: {affiliations}')


def transform_affiliation_list(affiliations):
    res = []
    for affiliation in affiliations:
        if affiliation.get('name', ""):
            possible_match = map_affiliation_by_name(affiliation.get('name', ""))
            if not possible_match['id']:
                continue

            res.append(possible_match)
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
    return [publisher] if publisher else []


def transform_dates(record, lang='en'):
    return record.pop('publication_date', '')


def transform_abstract(record, lang='en'):
    abstract = record.pop('description', '')
    return [{'lang': lang, 'value': abstract}] if abstract else []


def transform_resource_type(rec, lang='en'):
    resource_type = rec.pop('resource_type', {}) # TODO add others
    if resource_type.get('type', {}) == 'other' or rec.get('publication_type',"") == 'other':
        return {'id': 'other', 'title': {'en': 'Other specialized materials'}}

    if resource_type.get('type', {}) == 'publication' or rec.get('publication_type', "") == 'article':
        return {'id': 'article', 'title': {'en': 'Journal article'}}
    return {}


def transform_languages(rec, lang='en'):
    langs = rec.pop('language', [])
    if isinstance(langs, str):
        return [check_language(langs)]

    res = []
    for lang in langs:
        res.append(check_language(lang))

    return res


def check_language(lang):
    if lang == 'eng':
        return {'id': 'en'}
    elif lang == 'ces':
        return {'id': 'cs'}
    else:
        return {'id': lang}


# was obtained from /vocabularies and it was the easiest way to match affiliations with regular expressions
aff_vocab = {
    "umprum": {"en": "Academy of Arts, Architecture and Design in Prague",
               "cs": "Vysoká škola uměleckoprůmyslová v Praze"
               },
    "avu": {"en": "Academy of Fine Arts in Prague", "cs": "Akademie výtvarných umění v Praze"},
    "amu": {"en": "Academy of Performing Arts in Prague", "cs": "Akademie múzických umění v Praze"},
    "advacam": {"en": "ADVACAM", "cs": "ADVACAM"},
    "zemedelsky-vyzkum": {"en": "Agricultural Research", "cs": "Zemědělský výzkum"},
    "agritec-vyzkum-slechteni-sluzby": {"en": "AGRITEC Research, Breeding and Services",
                                        "cs": "AGRITEC, výzkum, šlechtění, služby"},
    "agrovyzkum-rapotin": {"en": "Agrovyzkum Rapotin", "cs": "Agrovýzkum Rapotín"},
    "am-uni": {"en": "Aix-Marseille University", "cs": ""},
    "aau": {"en": "Anglo-americká vysoká škola", "cs": "Anglo-American University"},
    "archip": {"en": "Architectural Institute in Prague", "cs": "Architectural Institute in Prague"},
    "arnika": {"en": "Arnika", "cs": "Arnika"},
    "idu": {"en": "Arts and Theatre Institute", "cs": "Institut umění - Divadelní ústav"},
    "simi": {"en": "Association for Integration and Migration", "cs": "Sdružení pro integraci a migraci"},
    "astronomicky-ustav-av-cr": {"en": "Astronomical Institute of the CAS", "cs": "Astronomický ústav AV ČR"},
    "biologicke-centrum-av-cr": {"en": "Biology Centre of the CAS", "cs": "Biologické centrum AV ČR"},
    "vut": {"en": "Brno University of Technology", "cs": "Vysoké učení technické v Brně"},
    "fakultni-nemocnice-bulovka": {"en": "Bulovka University Hospital", "cs": "Fakultní nemocnice Bulovka"},
    "cenia-ceska-informacni-agentura-zivotniho-prostredi": {"en": "CENIA",
                                                            "cs": "CENIA, česká informační agentura životního prostředí"},
    "stredoceska-vedecka-knihovna-v-kladne": {"en": "Central Bohemian Research Library in Kladno",
                                              "cs": "Středočeská vědecká knihovna v Kladně"},
    "central-european-policy-institute": {"en": "Central European Policy Institute", "cs": ""},
    "stredisko-spolecnych-cinnosti": {"en": "Centre for Administration and Operations of the ASCR",
                                      "cs": "Středisko společných činností"},
    "centrum-pro-studium-vysokeho-skolstvi": {"en": "Centre for Higher Education Studies",
                                              "cs": "Centrum pro studium vysokého školství"},
    "centrum-pro-regionalni-rozvoj-ceske-republiky": {"en": "Centre for Regional Development of the Czech Republic",
                                                      "cs": "Centrum pro regionální rozvoj České republiky"},
    "centrum-pro-dopravu-a-energetiku": {"en": "Centre for Transport and Energy",
                                         "cs": "Centrum pro dopravu a energetiku"},
    "centrum-kardiovaskularni-a-transplantacni-chirurgie-brno": {
        "en": "Centre of Cardiovascular and Transplantation Surgery",
        "cs": "Centrum kardiovaskulární a transplantační chirurgie Brno"},
    "uk": {"en": "Charles University", "cs": "Univerzita Karlova",
           'other_options':
               [
                   'Institute of Endocrinology, Prague, Czech Republic',
                   'Charles Univ Prague, Univ Hosp, Dept Cardiol, Plzen, Czech Republic',
                   'Charles Univ Prague, Fac Med 1, Gen Teaching Hosp, Dept Internal Med 2.Cardiovasc Med, Prague, Czech Republic',
                   'Charles Univ Prague, Fac Med 3, Cardioctr, Srobarova 50, Prague 10034, Czech Republic',
                   'Faculty of Science, CharlesUniversity, 128 40 Prague 2, Czech Republic',
                   'Faculty of Science, CharlesUniversity, 128 40 Prague 2, Czech Republic',
                   'Faculty of Science, CharlesUniversity, 128 40 Prague 2, Czech Republic',
                   'Department of Pathophysiology, 2nd Faculty of Medicine, Charles  University, Prague, Czech Republic',
                   'Institute of Anatomy, First Faculty of Medicine, Charles  University, Prague, Czech Republic',
                   'Department of Pathophysiology, 2nd Faculty of Medicine, Charles  University, Prague, Czech Republic',
                   'Department of Pathophysiology,Second Faculty of Medicine, CharlesUniversity, Prague, Czech Republic'
                   'Department of Physiology, SecondFaculty of Medicine, CharlesUniversity, Prague, Czech Republic',
                   '3rd Department of Internal Medicine,1st Faculty of Medicine, Charles'
                   'Institute of Anatomy, First Faculty of Medicine, Charles  University, Prague, Czech Republic',
                   'Centrum preventivní kardiologie, III. interní klinika – endokrinologie a metabolismu 1. LF UK a VFN v Praze',
                   'Department of Physical and Macromolecular Chemistry, Faculty of Science, Charles  University, Hlavova 8, Prague, 128 00, Czech Republic',
                   'Internal Department of Third Faculty of Medicine and Královské Vinohrady University Hospital, Charles  University Prague, Prague, Czech Republic',
                   'Department of Pathology, 3rd Faculty of Medicine, Charles  University, Prague, Czech Republic',
                   'Department of Physiology, Faculty of Science, Charles  University, Prague, Czech Republic',
                   '1st Faculty of Medicine, Institute of Pathological Physiology, Charles  University, Prague, Czech Republic',
                   'Department of Physiology, Faculty of Science, Charles  University, Prague, Czech Republic',
                   'Ústav hygieny a preventivní medicíny a 1. interní klinika LF UK a FN Plzeň',
                   '3. interní klinika – klinika endokrinologie a metabolismu 1. LF UK a VFN v Praze',
                   'Charles Univ Prague, Med Fac 1, Prague,',
                   'Charles Univ Prague, Fac Med 1, Dept Cardiol, Prague, Czech Republic',
                   'Charles Univ Prague, Inst Physiol, Fac Med 1, Prague, Czech Republic'
               ]},
    "vysoka-skola-podnikani-a-prava": {"en": "College of Entrepreneurship and Law",
                                       "cs": "Vysoká škola podnikání a práva"},
    "vsers": {"en": "College of European and Regional Studies", "cs": "Vysoká škola evropských a regionálních studií"},
    "vsmie": {"en": "College of Information Management Business Administration and Law",
              "cs": "Vysoká škola manažerské informatiky, ekonomiky a práva"},
    "vstvs palestra": {"en": "College of Physical Education and Sport PALESTRA",
                       "cs": "Vysoká škola tělesné výchovy a sportu PALESTRA"},
    "vysoka-skola-polytechnicka-jihlava": {"en": "College of Polytechnics Jihlava",
                                           "cs": "Vysoká škola polytechnická Jihlava"},
    "ambis": {"en": "College of Regional Development and Banking Institute - AMBIS", "cs": "AMBIS vysoká škola"},
    "uniba": {"en": "Comenius University Bratislava", "cs": ""},
    "vssav": {"en": "Computing Centre of the Slovak Academy od Sciences", "cs": ""},
    "vurv": {"en": "Crop Research Institute", "cs": "Výzkumný ústav rostlinné výroby"},
    "szpi": {"en": "Czech Agriculture and Food Inspection Authority",
             "cs": "Státní zemědělská a potravinářská inspekce"},
    "ceska-asociace-ergoterapeutu": {"en": "Czech Association of Occupational Therapists",
                                     "cs": "Česká asociace ergoterapeutů"},
    "crdm": {"en": "Czech Council of Children and Youth", "cs": "Česká rada dětí a mládeže"},
    "ceska-geologicka-sluzba": {"en": "Czech Geological Survey", "cs": "Česká geologická služba"},
    "chmu": {"en": "Czech Hydrometeorological Institute", "cs": "Český hydrometeorologický ústav"},
    "ustav-pro-jazyk-cesky-av-cr": {"en": "Czech Language Institute of the CAS", "cs": "Ústav pro jazyk český AV ČR"},
    "cnb": {"en": "Czech National Bank", "cs": "Česká národní banka"},
    "czepa": {"en": "Czech Paraplegics Association", "cs": "Česká asociace paraplegiků"},
    "surao": {"en": "Czech Radioactive Waste Repository Authority", "cs": "Správa úložišť radioaktivních odpadů"},
    "gacr": {"en": "Czech Science Foundation", "cs": "Grantová agentura České republiky"},
    "ceska-spolecnost-ornitologicka": {"en": "Czech Society for Ornithology", "cs": "Česká společnost ornitologická"},
    "csu": {"en": "Czech Statistical Office", "cs": "Český statistický úřad"},
    "cvut": {"en": "Czech Technical University in Prague", "cs": "České vysoké učení technické v Praze",
             'other_options':
                 [
                     'Czech Tech Univ, Dept Comp Sci, Prague, Czech Republic',
                     'Faculty of Biomedical Engineering, Czech Technical University, Prague, Czechia',
                     'Fakulta jaderná a fyzikálně inženýrská ČVUT, Praha'
                 ]},
    "czu": {"en": "Czech University of Life Sciences Prague", "cs": "Česká zemědělská univerzita v Praze"},
    "czwa": {"en": "Czech Water Association", "cs": "Asociace pro vodu ČR"},
    "muzeum-vychodnich-cech-v-hradci-kralove": {"en": "East Bohemian Museum in Hradec Králové",
                                                "cs": "Muzeum východních Čech v Hradci Králové"},
    "narodohospodarsky-ustav-av-cr": {"en": "Economics Institute of the CAS", "cs": "Národohospodářský ústav AV ČR"},
    "studijni-a-vedecka-knihovna-plzenskeho-kraje": {"en": "Education and Research Library of Pilsener Region",
                                                     "cs": "Studijní a vědecká knihovna Plzeňského kraje"},
    "ekodomov": {"en": "Ekodomov", "cs": "Ekodomov"},
    "elte": {"en": "Eötvös Loránd University", "cs": ""},
    "edri": {"en": "European Digital Rights", "cs": ""},
    "eruni": {"en": "European Research University", "cs": "Evropská výzkumná univerzita"},
    "euipo": {"en": "European Union Intellectual Property Office", "cs": "Úřad Evropské unie pro duševní vlastnictví"},
    "evropske-hodnoty": {"en": "European Values", "cs": "Evropské hodnoty"},
    "fairtrade-cesko-a-slovensko": {"en": "Fairtrade Czech Republic & Slovakia", "cs": "Fairtrade Česko a Slovensko"},
    "vupp": {"en": "Food Research Institute Prague", "cs": "Výzkumný ústav potravinářský Praha"},
    "vulhm": {"en": "Forestry and Game Management Research Institute",
              "cs": "Výzkumný ústav lesního hospodářství a myslivosti"},
    "krajska-knihovna-frantiska-bartose-ve-zline": {"en": "František Bartoš Regional Library in Zlín",
                                                    "cs": "Krajská knihovna Františka Bartoše ve Zlíně"},
    "fu-berlin": {"en": "Free University of Berlin", "cs": ""},
    "gvuo": {"en": "Gallery of Fine Arts in Ostrava", "cs": "Galerie výtvarného umění v Ostravě"},
    "gender-studies": {"en": "Gender Studies", "cs": "Gender Studies"},
    "vfn": {"en": "General University Hospital in Prague", "cs": "Všeobecná fakultní nemocnice v Praze"},
    "gle": {"en": "GLE", "cs": "GLE"},
    "czechglobe": {"en": "Global Change Research Institute of the CAS", "cs": "Ústav výzkumu globální změny AV ČR"},
    "goethe-institut": {"en": "Goethe Institute", "cs": ""},
    "greynet": {"en": "GreyNet International", "cs": ""},
    "hartree-centre": {"en": "Hartree Centre", "cs": ""},
    "hestia": {"en": "HESTIA", "cs": "HESTIA"},
    "chmelarsky-institut": {"en": "Hop Research Institute", "cs": "Chmelařský institut"},
    "knihovna-města-hradce-kralove": {"en": "Hradec Králové City Library", "cs": "Knihovna města Hradce Králové"},
    "indira-gandhi-centre-for-atomic-research": {"en": "Indira Gandhi Centre for Atomic Research", "cs": ""},
    "upv": {"en": "Industrial Property Office", "cs": "Úřad průmyslového vlastnictví"},
    "ikem": {"en": "Institute for Clinical and Experimental Medicine",
             "cs": "Institut klinické a experimentální medicíny",
             'other_options': [
                 'Institut klinicke a experimentalni mediciny',
                 'Institute of Clinical and Experimental Medicine',
                 'Diabetes Centre, Institute for Clinical and Experimental  Medicine, Prague, Czechia',
                 '3Department of Clinical and Transplant Pathology, Institute for Clinical  and Experimental Medicine, Prague, Czech Republic',
                 'Information Technology Division,Institute for  Clinical and Experimental Medicine,Prague',
                 'Department of Medical Technology and  Investments,Institute for Clinical and  Experimental Medicine,Prague',
                 'MR Unit,Department of Diagnostic and  Interventional Radiology,Institute for Clinical  and Experimental Medicine,Prague',
                 'Centrum diabetologie IKEM, Praha',
                 'Centrum diabetologie IKEM, Praha',
                 'Centrum diabetologie, IKEM',
                 'Centrum experimentální medicíny, IKEM Praha',
                 'IKEM, Praha',
                 'IKEM',
                 'Department of Nanotoxicology and Molecular Epidemiology, Institute of Experimental Medicine of the Czech  Academy of Sciences, 14220 Prague,'
                 'Department of Nanotoxicology and Molecular Epidemiology, Institute of Experimental Medicine of the Czech  Academy of Sciences, 14220 Prague, Czech Republic',
                 'Department of Nanotoxicology and Molecular Epidemiology, Institute of Experimental Medicine of the Czech  Academy of Sciences, 14220 Prague',
                 'Institute for Clinical & Experimental Medicine (IKEM) Transplant Ctr, Dept Nephrol, Prague',
                 'Institute for Clinical & Experimental Medicine (IKEM) Transplant Lab, Prague',
                 'Institute for Clinical & Experimental Medicine (IKEM) Transplant Pathol Ctr',
                 'Institute for Clinical & Experimental Medicine (IKEM) Transplant Ctr, Dept Nephrol, Prague',
                 'Institute for Clinical & Experimental Medicine (IKEM) Transplant Lab, Prague'
             ]},
    "institut-postgradualniho-vzdelavani-ve-zdravotnictvi": {"en": "Institute for Postgraduate Medical Education",
                                                             "cs": "Institut postgraduálního vzdělávání ve zdravotnictví"},
    "ustr": {"en": "Institute for the Study of Totalitarian Regimes", "cs": "Ústav pro studium totalitních režimů"},
    "uzei": {"en": "Institute of Agricultural Economics and Information",
             "cs": "Ústav zemědělské ekonomiky a informací"},
    "ustav-analyticke-chemie-av-cr": {"en": "Institute of Analytical Chemistry of the CAS",
                                      "cs": "Ústav analytické chemie AV ČR"},
    "ustav-zivocisne-fyziologie-a-genetiky-av-cr": {"en": "Institute of Animal Physiology and Genetics  of the CAS",
                                                    "cs": "Ústav živočišné fyziologie a genetiky AV ČR",
                                                    'other_options':
                                                        [
                                                            'Laboratory of Anaerobic Microbiology, Institute of Animal Physiology and Genetics, CAS, Prague',
                                                            'Institute of Animal Physiology and Genetics, CAS, Prague',

                                                        ]},
    "vuzv": {"en": "Institute of Animal Science", "cs": "Výzkumný ústav živočišné výroby"},
    "arub": {"en": "Institute of Archaeology of the CAS, Brno", "cs": "Archeologický ústav AV ČR, Brno"},
    "archeologicky-ustav-av-cr-praha": {"en": "Institute of Archaeology of the CAS, Prague",
                                        "cs": "Archeologický ústav AV ČR, Praha"},
    "ustav-archeologicke-pamatkove-pece-severozapadnich-cech": {
        "en": "Institute of Archeological and Cultural Heritage Preservation in Northwestern Bohemia",
        "cs": "Ústav archeologické památkové péče severozápadních Čech"},
    "ustav-dejin-umeni-av-cr": {"en": "Institute of Art History of the CAS", "cs": "Ústav dějin umění AV ČR"},
    "ustav-fyziky-atmosfery-av-cr": {"en": "Institute of Atmospheric Physics  of the CAS",
                                     "cs": "Ústav fyziky atmosféry AV ČR"},
    "biofyzikalni-ustav-av-cr": {"en": "Institute of Biophysics of the CAS", "cs": "Biofyzikální ústav AV ČR"},
    "biotechnologicky-ustav-av-cr": {"en": "Institute of Biotechnology of the CAS",
                                     "cs": "Biotechnologický ústav AV ČR"},
    "botanicky-ustav-av-cr": {"en": "Institute of Botany of the CAS", "cs": "Botanický ústav AV ČR"},
    "institute-of-chemical-engineering-sciences": {"en": "Institute of Chemical Engineering Sciences", "cs": ""},
    "ustav-chemickych-procesu-av-cr": {"en": "Institute of Chemical Process Fundamentals of the CAS",
                                       "cs": "Ústav chemických procesů AV ČR"},
    "ustav-informatiky-av-cr": {"en": "Institute of Computer Science of the CAS", "cs": "Ústav informatiky AV ČR",
                                'other_options': [
                                    'Institute of Computer Science, Czech Academy of Sciences, Prague,  Czech Republic',

                                ]},
    "ustav-pro-soudobe-dejiny-av-cr": {"en": "Institute of Contemporary History of the CAS",
                                       "cs": "Ústav pro soudobé dějiny AV ČR"},
    "ustav-pro-ceskou-literaturu-av-cr": {"en": "Institute of Czech Literature of the CAS",
                                          "cs": "Ústav pro českou literaturu AV ČR"},
    "ustav-pro-elektrotechniku": {"en": "Institute of Electrical Engineering", "cs": "Ústav pro elektrotechniku"},
    "entomologicky-ustav-av-cr": {"en": "Institute of Entomology of the CAS", "cs": "Entomologický ústav AV ČR"},
    "etnologicky-ustav-av-cr": {"en": "Institute of Ethnology of the CAS", "cs": "Etnologický ústav AV ČR"},
    "ustav-experimentalni-botaniky-av-cr": {"en": "Institute of Experimental Botany of the CAS",
                                            "cs": "Ústav experimentální botaniky AV ČR"},
    "ustav-experimentalni-mediciny-av-cr": {"en": "Institute of Experimental Medicine of the CAS",
                                            "cs": "Ústav experimentální medicíny AV ČR"},
    "geologicky-ustav-av-cr": {"en": "Institute of Geology of the CAS", "cs": "Geologický ústav AV ČR"},
    "ustav-geoniky-av-cr": {"en": "Institute of Geonics of the CAS", "cs": "Ústav geoniky AV ČR"},
    "geofyzikalni-ustav-av-cr": {"en": "Institute of Geophysics of the CAS", "cs": "Geofyzikální ústav AV ČR"},
    "ukht": {"en": "Institute of Hematology and Blood Transfusion", "cs": "Ústav hematologie a krevní transfuze",
             'other_options': [
                 'Inst Hematol & Blood Transfus, Prague, Czech Republic',

             ]},
    "historicky-ustav-av-cr": {"en": "Institute of History of the CAS", "cs": "Historický ústav AV ČR"},
    "hydrobiologicky-ustav-av-cr": {"en": "Institute of Hydrobiology of the CAS", "cs": "Hydrobiologický ústav AV ČR"},
    "ustav-pro-hydrodynamiku-av-cr": {"en": "Institute of Hydrodynamics of the CAS",
                                      "cs": "Ústav pro hydrodynamiku AV ČR"},
    "ustav-teorie-informace-a-automatizace-av-cr": {"en": "Institute of Information Theory and Automation of the CAS",
                                                    "cs": "Ústav teorie informace a automatizace AV ČR"},
    "ustav-anorganicke-chemie-av-cr": {"en": "Institute of Inorganic Chemistry of the CAS",
                                       "cs": "Ústav anorganické chemie AV ČR"},
    "umv": {"en": "Institute of International Relations Prague", "cs": "Ústav mezinárodních vztahů"},
    "ustav-makromolekularni-chemie-av-cr": {"en": "Institute of Macromolecular Chemistry of the CAS",
                                            "cs": "Ústav makromolekulární chemie AV ČR",
                                            'other_options': [
                                                'Department of Chemistry and Physics of Surfaces and Interfaces, Institute of Macromolecular Chemistry, AS CR, Prague',
                                                'Institute of Macromolecular Chemistry, AS CR, Prague',
                                                'Institute of Macromolecular Chemistry, Czech Academy of Sciences, Heyrovskéhonám.2, Prague, Czech Republic',
                                                'Institute of Macromolecular Chemistry, Czech Academy of Sciences, Heyrovsky square  2, 162 06 Prague, Czech Republic',
                                                'Institute of Macromolecular Chemistry, AS CR, Prague 6 162 06, Czech Republic',
                                                'Institute of Macromolecular Chemistry, Czech Academy of Sciences, Heyrovského nám. 2, 162 00 Prague 6, Czech  Republic'
                                                'Czech Academy of Sciences, Institute of Macromolecular Chemistry'
                                            ]},
    "matematicky-ustav-av-cr": {"en": "Institute of Mathematics of the CAS", "cs": "Matematický ústav AV ČR"},
    "mikrobiologicky-ustav-av-cr": {"en": "Institute of Microbiology of the CAS", "cs": "Mikrobiologický ústav AV ČR",
                                    'other_options': [
                                        'Laboratory of Molecular Structure Characterization, Institute of Microbiology of the Czech Academy of Sciences, Vídeňská 1083, 142 00 Prague, Czech Republic'
                                    ]},
    "ustav-molekularni-genetiky-av-cr": {"en": "Institute of Molecular Genetics of the CAS",
                                         "cs": "Ústav molekulární genetiky AV ČR", 'other_options': [
            'Institute of Molecular Genetics of the Czech  Academy of Sciences, Prague, Czech Republic',
            'Institute of Molecular Genetics of the Czech  Academy of Sciences, Prague, Czech Republic;'
            'Institute of Molecular Genetics of the Czech  Academy of Sciences',
            'Laboratory of Genomics andBioinformatics, Institute of MolecularGenetics of the Czech Academy ofSciences, Prague, Czech Republic'
        ]},
    "ustav-organicke-chemie-a-biochemie-av-cr": {"en": "Institute of Organic Chemistry and Biochemistry of the CAS",
                                                 "cs": "Ústav organické chemie a biochemie AV ČR"},
    "parazitologicky-ustav-av-cr": {"en": "Institute of Parasitology of the CAS", "cs": "Parazitologický ústav AV ČR"},
    "filosoficky-ustav-av-cr": {"en": "Institute of Philosophy of the CAS", "cs": "Filosofický ústav AV ČR"},
    "ustav-fotoniky-a-elektroniky-av-cr": {"en": "Institute of Photonics and Electronics of the CAS",
                                           "cs": "Ústav fotoniky a elektroniky AV ČR"},
    "ustav-fyziky-materialu-av-cr": {"en": "Institute of Physics of Materials of the CAS",
                                     "cs": "Ústav fyziky materiálů AV ČR"},
    "fyzikalni-ustav-av-cr": {"en": "Institute of Physics of the CAS", "cs": "Fyzikální ústav AV ČR"},
    "fyziologicky-ustav-av-cr": {"en": "Institute of Physiology of the CAS", "cs": "Fyziologický ústav AV ČR",
                                 'other_options': [
                                     'Institute of Physiology of the Czech Academy of Sciences, Prague, Czech Republic',
                                     'Institute of Physiology of the Czech Academy of Sciences',
                                     'Institute of Physiology, Czech Academy of Sciences, 14200 Prague, Czech Republic',
                                     'Institute of Physiology, Czech Academy of Sciences, Prague, Czech Republic',
                                     'Institute of Physiology, Czech Academy of Sciences, Prague, Czech',
                                     'Laboratory of Developmental Cardiology, Institute of Physiology, Academy of Sciences of the Czech Republic (ASCR), Prague, Czechia',
                                     'Institute of Physiology, Czech Academy of Sciences, 14220 Prague, Czech Republic',
                                     'Department of Metabolism of Bioactive Lipids, Institute of Physiology of the Czech Academy of Sciences, Videnska 1083, 142 00, Prague, Czech Republic'
                                     'Department of Adipose Tissue Biology, Institute of Physiology of the Czech Academy of Sciences, Videnska 1083, 142 00, Prague, Czech Republic',
                                     'Department of Metabolomics, Institute of Physiology of the Czech Academy of Sciences, Videnska 1083, 142 00, Prague, Czech Republic',
                                     'Department of Metabolism of Bioactive Lipids, Institute of Physiology of the Czech Academy of Sciences, Videnska 1083, 142 00, Prague, Czech Republic',
                                     'Institute of Physiology, Academy of Sciences of the Czech Republic,  Prague, Czech Republic',
                                     'Institute of Physiology, Czech Academy of Sciences,Prague, Czech Republic,',
                                     'Institute of Physiology, Czech Academy of Sciences,Prague, Czech Republic',
                                     'Institute of Physiology, Czech Academy of Sciences,Prague, Czech Republic'
                                 ]},
    "ustav-molekularni-biologie-rostlin-av-cr": {"en": "Institute of Plant Molecular Biology of the CAS",
                                                 "cs": "Ústav molekulární biologie rostlin AV ČR"},
    "ustav-fyziky-plazmatu-av-cr": {"en": "Institute of Plasma Physics of the CAS",
                                    "cs": "Ústav fyziky plazmatu AV ČR"},
    "psychologicky-ustav-av-cr": {"en": "Institute of Psychology of the CAS", "cs": "Psychologický ústav AV ČR"},
    "ustav-struktury-a-mechaniky-hornin-av-cr": {"en": "Institute of Rock Structure and Mechanics of the CAS",
                                                 "cs": "Ústav struktury a mechaniky hornin AV ČR"},
    "ustav-pristrojove-techniky-av-cr": {"en": "Institute of Scientific Instruments of the CAS",
                                         "cs": "Ústav přístrojové techniky AV ČR",
                                         'other_options': [
                                             'Institute of Scientific Instruments, Czech Academy of Sciences, Brno, Czech Republic'
                                         ]},
    "slovansky-ustav-av-cr": {"en": "Institute of Slavonic Studies of the CAS", "cs": "Slovanský ústav AV ČR"},
    "sociologicky-ustav-av-cr": {"en": "Institute of Sociology of the CAS", "cs": "Sociologický ústav AV ČR"},
    "ustav-pudni-biologie-av-cr": {"en": "Institute of Soil Biology of the CAS", "cs": "Ústav půdní biologie AV ČR"},
    "ustav-statu-a-prava-av-cr": {"en": "Institute of State and Law of the CAS", "cs": "Ústav státu a práva AV ČR"},
    "vysoka-skola-technicka-a-ekonomicka-v-ceskych-budejovicich": {
        "en": "Institute of Technology and Business in České Budějovice",
        "cs": "Vysoká škola technická a ekonomická v Českých Budějovicích"},
    "ustav-teoreticke-a-aplikovane-mechaniky-av-cr": {"en": "Institute of Theoretical and Applied Mechanics of the CAS",
                                                      "cs": "Ústav teoretické a aplikované mechaniky AV ČR"},
    "ustav-termomechaniky-av-cr": {"en": "Institute of Thermomechanics of the CAS", "cs": "Ústav termomechaniky AV ČR"},
    "ustav-biologie-obratlovcu-av-cr": {"en": "Institute of Vertebrate Biology of the CAS",
                                        "cs": "Ústav biologie obratlovců AV ČR"},
    "isga": {"en": "International School Grounds Alliance", "cs": ""},
    "iucn": {"en": "International Union for Conservation of Nature", "cs": ""},
    "ustav-fyzikalni-chemie-j-heyrovskeho-av-cr": {"en": "J. Heyrovsky Institute of Physical Chemistry of the CAS",
                                                   "cs": "Ústav fyzikální chemie J. Heyrovského AV ČR"},
    "ujak": {"en": "Jan Amos Komenský University Prague", "cs": "Univerzita Jana Amose Komenského Praha"},
    "ujep": {"en": "Jan Evangelista Purkyně University in Ústí nad Labem",
             "cs": "Univerzita Jana Evangelisty Purkyně v Ústí nad Labem"},
    "jamu": {"en": "Janáček Academy of Music and Performing Arts in Brno",
             "cs": "Janáčkova akademie múzických umění v Brně"},
    "nadace-promeny-karla-komarka": {"en": "Karel Komárek Family Foundation",
                                     "cs": "Nadace Karel Komárek Family Foundation"},
    "knav": {"en": "Library of the Czech Academy of Sciences", "cs": "Knihovna AV ČR"},
    "masarykuv-ustav-a-archiv-av-cr": {"en": "Masaryk Institute and Archives of the CAS",
                                       "cs": "Masarykův ústav a Archiv AV ČR"},
    "masarykuv-onkologicky-ustav": {"en": "Masaryk Memorial Cancer Institute", "cs": "Masarykův onkologický ústav"},
    "mu": {"en": "Masaryk University", "cs": "Masarykova univerzita",
           'other_options': [
               'Masaryk Univ, Fac Med, Dept Internal Med Cardioangiol 1, ICRC, Brno, Czech Republic',
               'Masaryk Univ, Fac Med, Inst Biostat & Anal, Brno, Czech Republic'
           ]},
    "ror:042nb2s44": {"en": "Massachusetts Institute of Technology", "cs": ""},
    "membrain": {"en": "MemBrain", "cs": "MemBrain"},
    "mendelu": {"en": "Mendel University in Brno", "cs": "Mendelova univerzita v Brně"},
    "mup": {"en": "Metropolitan University Prague", "cs": "Metropolitní univerzita Praha"},
    "metu": {"en": "Middle East Technical University", "cs": ""},
    "migration-policy-task-force": {"en": "Migration Policy Task Force", "cs": ""},
    "vojenska-nemocnice-brno": {"en": "Military Hospital Brno", "cs": "Vojenská nemocnice Brno"},
    "mkcr": {"en": "Ministry of Culture", "cs": "Ministerstvo Kultury České Republiky"},
    "ministerstvo-obrany-cr": {"en": "Ministry of Defence of the Czech Republic", "cs": "Ministerstvo obrany ČR"},
    "msmt": {"en": "Ministry of Education, Youth and Sports", "cs": "Ministerstvo školství, mládeže a tělovýchovy"},
    "ministerstvo-financ-cr": {"en": "Ministry of Finance of the Czech Republic", "cs": "Ministerstvo financí ČR"},
    "ministerstvo-spravedlnosti-cr": {"en": "Ministry of Justice of the Czech Republic",
                                      "cs": "Ministerstvo spravedlnosti ČR"},
    "mpsv": {"en": "Ministry of Labour and Social Affairs",
             "cs": "Ministerstvo práce a sociálních věcí České republiky"},
    "ministerstvo-zivotniho-prostredi-cr": {"en": "Ministry of the Environment of the Czech Republic",
                                            "cs": "Ministerstvo životního prostředí ČR"},
    "mvcr": {"en": "Ministry of the Interior", "cs": "Ministerstvo vnitra České republiky"},
    "moravska-galerie-v-brne": {"en": "Moravian Gallery in Brno", "cs": "Moravská galerie v Brně"},
    "mzk": {"en": "Moravian Library", "cs": "Moravská zemská knihovna"},
    "moravskoslezska-vedecka-knihovna-v-ostrave": {"en": "Moravian-Silesian Research Library in Ostrava",
                                                   "cs": "Moravskoslezská vědecká knihovna v Ostravě"},
    "fakultni-nemocnice-v-motole": {"en": "Motol University Hospital", "cs": "Fakultní nemocnice v Motole",
                                    'other_options': [
                                        'Department of Geriatric Internal Medicine, 2nd Medical Faculty Motol,  Prague, Czech Republic',
                                        'Second Medical Faculty, Motol Hospital, Prague, Czech Republic'
                                    ]},
    "mestska-knihovna-v-praze": {"en": "Municipal Library of Prague", "cs": "Městská knihovna v Praze"},
    "pnp": {"en": "Museum of Czech Literature", "cs": "Památník národního písemnictví"},
    "upm": {"en": "Museum of Decorative Arts in Prague", "cs": "Uměleckoprůmyslové museum"},
    "muzeum-skla-a-bizuterie-v-jablonci-nad-nisou": {"en": "Museum of Glass and Jewellery",
                                                     "cs": "Muzeum skla a bižuterie v Jablonci nad Nisou"},
    "muzeum-brnenska": {"en": "Museum of the Brno Region", "cs": "Muzeum Brněnska"},
    "zcm": {"en": "Museum of West Bohemia in Pilsen", "cs": "Západočeské muzeum v Plzni"},
    "nemocnice-na-homolce": {"en": "Na Homolce Hospital", "cs": "Nemocnice Na Homolce",
                             'other_options': [
                                 'Na Homolce Hosp, Dept Cardiol, Prague, Czech Republic',
                                 'Internal Department, Hospital Na Homolce, Prague, Czech Republic'
                             ]},
    "narodni-archiv": {"en": "National Archives", "cs": "Národní archiv"},
    "nukib": {"en": "National Cyber and Information Security Agency",
              "cs": "Národní úřad pro kybernetickou a informační bezpečnost"},
    "nfa": {"en": "National Film Archive", "cs": "Národní filmový archiv"},
    "narodni-galerie-v-praze": {"en": "National Gallery Prague", "cs": "Národní galerie v Praze"},
    "npu": {"en": "National Heritage Institute", "cs": "Národní památkový ústav"},
    "nipos": {"en": "National Information and Consulting Centre for Culture",
              "cs": "Národní informační a poradenské středisko pro kulturu"},
    "nuv": {"en": "National Institute for Education", "cs": "Národní ústav pro vzdělávání"},
    "nulk": {"en": "National Institute of Folk Culture", "cs": "Národní ústav lidové kultury"},
    "nudz": {"en": "National Institute of Mental Health", "cs": "Národní ústav duševního zdraví"},
    "szu": {"en": "National Institute of Public Health", "cs": "Státní zdravotní ústav"},
    "ntk": {"en": "National Library of Technology", "cs": "Národní technická knihovna"},
    "nk cr": {"en": "National Library of the Czech Republic", "cs": "Národní knihovna ČR"},
    "nlk": {"en": "National Medical Library", "cs": "Národní lékařská knihovna"},
    "narodni-muzeum": {"en": "National Museum", "cs": "Národní muzeum"},
    "narodni-zemedelske-muzeum": {"en": "National Museum of Agriculture", "cs": "Národní zemědělské muzeum"},
    "narodni-muzeum-v-prirode": {"en": "National Open-Air Museum", "cs": "Národní muzeum v přírodě"},
    "npmk": {"en": "National Pedagogical Museum and Library of J. A. Comenius",
             "cs": "Národní pedagogické muzeum a knihovna J. A. Komenského"},
    "suro": {"en": "National Radiation Protection Institute", "cs": "Státní ústav radiační ochrany"},
    "narodni-hrebcin-kladruby-nad-labem": {"en": "National Stud at Kladruby nad Labem",
                                           "cs": "Národní hřebčín Kladruby nad Labem"},
    "ntm": {"en": "National Technical Museum", "cs": "Národní technické muzeum"},
    "umk": {"en": "Nicolaus Copernicus University", "cs": ""},
    "severoceske-muzeum-v-liberci": {"en": "North Bohemian Museum in Liberec", "cs": "Severočeské muzeum v Liberci"},
    "norwegian-forest-and-landscape-institute": {"en": "Norwegian Forest and Landscape Institute", "cs": ""},
    "ustav-jaderne-fyziky-av-cr": {"en": "Nuclear Physics Institute of the CAS", "cs": "Ústav jaderné fyziky AV ČR"},
    "ujv-rez": {"en": "Nuclear Research Institute Rez", "cs": "Ústav Jaderného Výzkumu Řež, a. s."},
    "vubp": {"en": "Occupational Safety Research Institute", "cs": "Výzkumný ústav bezpečnosti práce"},
    "urad-vlady-cr": {"en": "Office of the Government of the Czech Republic", "cs": "Úřad vlády České republiky"},
    "vedecka-knihovna-v-olomouci": {"en": "Olomouc Research Library", "cs": "Vědecká knihovna v Olomouci"},
    "fnol": {"en": "Olomouc University Hospital", "cs": "Fakultní nemocnice Olomouc",
             'other_options': [
                 'University Hospital Olomouc, Olomouc, Czech Republic',
                 'First Internal Cardiology Clinic, University Hospital Olomouc, Czech Republic',
             ]},
    "orientalni-ustav-av-cr": {"en": "Oriental Institute of the CAS", "cs": "Orientální ústav AV ČR"},
    "oseva": {"en": "OSEVA Development and Research", "cs": "OSEVA vývoj a výzkum"},
    "univerzita-palackeho-v-olomouci": {"en": "Palacký University Olomouc", "cs": "Univerzita Palackého v Olomouci",
                                        'other_options': [
                                            'Palacky University Hospital, Olomouc , Czech Republic',
                                            'Palacky University Hospital'
                                            'Department of Internal Medicine I,  Cardiology, University Hospital Olomouc and Palacký University, Olomouc, Czech Republic'
                                            'Palacky Univ, Fac Med & Dent, Dept Internal Med Cardiol 1, Olomouc, Czech Republic',
                                            'University  Hospital Olomouc and Palacký University, Olomouc, Czech  Republic',

                                            'Medical and Dentistry School, Palacký University, Olomouc, Czech Republic'
                                            'Department of Internal Medicine I, Cardiology, University Hospital Olomouc and Palacky University, Olomouc, Czech Republic',

                                            'Department of Pharmacology, Faculty of Medicine and Dentistry, Palacky University, Olomouc, Czech',
                                            'Faculty of Medicine and Dentistry, Palacký University, Olomouc, Czech Republic',
                                            'Department of Internal Medicine I, Cardiology, University  Hospital Olomouc and Palacký University, Olomouc, Czech  Republic'
                                        ]},
    "panevropska-univerzita": {"en": "Pan-European University", "cs": "Panevropská univerzita"},
    "krajska-knihovna-v-pardubicich": {"en": "Pardubice Regional Library", "cs": "Krajská knihovna v Pardubicích"},
    "pi": {"en": "Parliamentary Institute", "cs": "Parlamentní institut"},
    "clovek-v-tisni": {"en": "People in Need Czech Republic", "cs": "Člověk v tísni"},
    "osobni-archiv-ing-arch-jana-moucky": {"en": "Personal archive of Jan Moučka",
                                           "cs": "Osobní archiv Ing. arch. Jana Moučky"},
    "osobni-archiv-doc-rndr-jiriho-souceka-drsc-": {"en": "Personal archive of Jiří Souček",
                                                    "cs": "Osobní archiv doc. RNDr. Jiřího Součka, DrSc."},
    "policejni-akademie-ceske-republiky-v-praze": {"en": "Police Academy of the Czech Republic in Prague",
                                                   "cs": "Policejní akademie České republiky v Praze"},
    "polytechnique-montreal": {"en": "Polytechnique Montréal", "cs": "Polytechnique Montréal"},
    "vyzkumny-ustav-bramborarsky-havlickuv-brod": {"en": "Potato Research Institute Havlíčkův Brod",
                                                   "cs": "Výzkumný ústav bramborářský Havlíčkův Brod"},
    "prague-city-university": {"en": "Prague City University", "cs": ""},
    "prague-film-school": {"en": "Prague Film School", "cs": "Prague Film School"},
    "vse": {"en": "Prague University of Economics and Business", "cs": "Vysoká škola ekonomická v Praze"},
    "vysoka-skola-prigo": {"en": "PRIGO University", "cs": "Vysoká škola PRIGO"},
    "psychiatricka-nemocnice-bohnice-lekarska-knihovna": {"en": "Psychiatric Hospital Bohnice - Medical Library",
                                                          "cs": "Psychiatrická nemocnice Bohnice - Lékařská knihovna"},
    "qub": {"en": "Queen's University Belfast", "cs": ""},
    "krajska-zdravotni": {"en": "Regional Health Corporation", "cs": "Krajská zdravotní"},
    "krajska-vedecka-knihovna-v-liberci": {"en": "Regional Research Library in Liberec",
                                           "cs": "Krajská vědecká knihovna v Liberci"},
    "vyzkumny-a-slechtitelsky-ustav-ovocnarsky-holovousy": {
        "en": "Research and Breeding Institute of Pomology Holovousy",
        "cs": "Výzkumný a šlechtitelský ústav ovocnářský Holovousy"},
    "centrum-vyzkumu-rez": {"en": "Research Centre Řež", "cs": "Centrum výzkumu Řež"},
    "vyzkumny-ustav-picninarsky": {"en": "Research Institute for Fodder Crops", "cs": "Výzkumný ústav pícninářský"},
    "vupsv": {"en": "Research Institute for Labour and Social Affairs", "cs": "Výzkumný ústav práce a sociálních věcí"},
    "vumop": {"en": "Research Institute for Soil and Water Conservation",
              "cs": "Výzkumný ústav meliorací a ochrany půdy"},
    "vyzkumny-ustav-pivovarsky-a-sladarsky": {"en": "Research Institute od Brewing and Malting",
                                              "cs": "Výzkumný ústav pivovarský a sladařský"},
    "vugtk": {"en": "Research Institute of Geodesy, Topography and Cartography",
              "cs": "Výzkumný ústav geodetický, topografický a kartografický"},
    "studijni-a-vedecka-knihovna-v-hradci-kralove": {"en": "Research Library in Hradec Králové",
                                                     "cs": "Studijní a vědecká knihovna v Hradci Králové"},
    "jihoceska-vedecka-knihovna-v-ceskych-budejovicich": {"en": "Research Library of South Bohemia in České Budějovice",
                                                          "cs": "Jihočeská vědecká knihovna v Českých Budějovicích"},
    "stfc": {"en": "Science and Technology Facilities Council", "cs": ""},
    "slezske-zemske-muzeum": {"en": "Silesian Museum", "cs": "Slezské zemské muzeum"},
    "slezska-univerzita-v-opave": {"en": "Silesian University in Opava", "cs": "Slezská univerzita v Opavě"},
    "vyzkumny-ustav-silva-taroucy-pro-krajinu-a-okrasne-zahradnictvi": {
        "en": "Silva Tarouca Research Institute for Landscape and Ornamental Gardening",
        "cs": "Výzkumný ústav Silva Taroucy pro krajinu a okrasné zahradnictví"},
    "siriri": {"en": "SIRIRI", "cs": "SIRIRI"},
    "savs": {"en": "ŠKODA AUTO University", "cs": "ŠKODA AUTO Vysoká škola"},
    "nscc": {"en": "Slovak National Supercomputing Centre", "cs": ""},
    "stu": {"en": "Slovak University of Technology in Bratislava", "cs": ""},
    "jihomoravske-muzeum-ve-znojme": {"en": "South Moravian Museum in Znojmo", "cs": "Jihomoravské muzeum ve Znojmě"},
    "fakultni-nemocnice-u-sv.anny-v-brne": {"en": "St. Anne's University Hospital Brno",
                                            "cs": "Fakultní nemocnice u sv. Anny v Brně"},
    "sukl": {"en": "State Institute for Drug Control", "cs": "Státní ústav pro kontrolu léčiv"},
    "suip": {"en": "State Labour Inspection Office", "cs": "Státní úřad inspekce práce"},
    "statni-oblastni-archiv-v-plzni": {"en": "State Regional Archive in Plzeň", "cs": "Státní oblastní archiv v Plzni"},
    "vyzkumny-ustav-vodohospodarsky-t-g-masaryka": {"en": "T. G. Masaryk Water Research Institute",
                                                    "cs": "Výzkumný ústav vodohospodářský T. G. Masaryka"},
    "tmb": {"en": "Technical Museum in Brno", "cs": "Technické muzeum v Brně"},
    "tul": {"en": "Technical University of Liberec", "cs": "Technická univerzita v Liberci"},
    "tum": {"en": "Technical University of Munich", "cs": ""},
    "ta cr": {"en": "Technology Agency of the Czech Republic", "cs": "Technologická agentura České republiky"},
    "technologicke-centrum-av-cr": {"en": "Technology Centre of the CAS", "cs": "Technologické centrum AV ČR"},
    "eli-eric": {"en": "The Extreme Light Infrastructure ERIC (only facility Dolní Břežany, CZ)",
                 "cs": "The Extreme Light Infrastructure ERIC"},
    "fakultni-thomayerova-nemocnice": {"en": "Thomayer University Hospital", "cs": "Fakultní Thomayerova nemocnice"},
    "vyzkumny-a-vyvojovy-ustav-drevarsky-praha": {"en": "Timber Research and Development Institute, Prague",
                                                  "cs": "Výzkumný a vývojový ústav dřevařský, Praha"},
    "utb": {"en": "Tomas Bata University in Zlín", "cs": "Univerzita Tomáše Bati ve Zlíně"},
    "cdv": {"en": "Transport Research Centre", "cs": "Centrum dopravního výzkumu"},
    "fnbrno": {"en": "University Hospital Brno", "cs": "Fakultní nemocnice Brno",
               'other_options': [
                   'St Annes Univ Hosp, Brno, Czech Republic'
               ]},
    "fakultni-nemocnice-hradec-kralove": {"en": "University Hospital Hradec Králové",
                                          "cs": "Fakultní nemocnice Hradec Králové",
                                          'other_options': [
                                              'Univ Hosp Hradec Kralove, Dept Med Cardioangiol 1, Hradec Kralove, Czech Republic',
                                              'University Hospital Hradec KraloveDept Histol & EmbryolHRADEC KRALOVE, CZECH REPUBLIC'
                                          ]},
    "fakultni-nemocnice-ostrava": {"en": "University Hospital in Ostrava", "cs": "Fakultní nemocnice Ostrava",
                                   'other_options': [
                                       'Univ Hosp Ostrava, Cardiovasc Dept, Ostrava, Czech Republic',
                                       'Cardiovascular Department, University Hospital Ostrava, Czech Republic',
                                       'Department of Oncology, University Hospital Ostrava and Ostrava University Medical School, 17. listopadu 1790/5, 70800 Ostrava, Czech Republic'
                                   ]},
    "fakultni-nemocnice-plzen": {"en": "University Hospital in Pilsen", "cs": "Fakultní nemocnice Plzeň"},
    "fakultni-nemocnice-kralovske-vinohrady": {"en": "University Hospital Kralovske Vinohrady",
                                               "cs": "Fakultní nemocnice Královské Vinohrady"},
    "uni-bayreuth": {"en": "University of Bayreuth", "cs": ""},
    "uni-bergen": {"en": "University of Bergen", "cs": ""},
    "vscht": {"en": "University of Chemistry and Technology, Prague",
              "cs": "Vysoká škola chemicko-technologická v Praze",
              'other_options': [
                  'Department of Biochemistry and Microbiology, University of Chemistry and Technology Prague, Technicka 5, 166 28, Prague, Czech Republic',
                  'Department of Biochemistry andMicrobiology, University of Chemistry andTechnology, Prague, Czech Republic',
                  'Department of Biochemistry and Microbiology, University of Chemistry and Technology Prague, Technicka 5, 166 28 Prague, Czech Republic'
              ]},
    "univerzita-obrany": {"en": "University of Defence in Brno", "cs": "Univerzita obrany"},
    "vysoka-skola-financni-a-spravni": {"en": "University of Finance and Administration",
                                        "cs": "Vysoká škola finanční a správní"},
    "univerzita-hradec-kralove": {"en": "University of Hradec Králové", "cs": "Univerzita Hradec Králové"},
    "uni-manchester": {"en": "University of Manchester", "cs": ""},
    "uni-minnesota": {"en": "University of Minnesota", "cs": "University of Minnesota"},
    "ostravska-univerzita": {"en": "University of Ostrava", "cs": "Ostravská univerzita"},
    "upce": {"en": "University of Pardubice", "cs": "Univerzita Pardubice",
             'other_options': [
                 'Pardubice Hosp, Dept Cardiol, Pardubice, Czech Republic',

             ]},
    "jcu": {"en": "University of South Bohemia in České Budějovice",
            "cs": "Jihočeská univerzita v Českých Budějovicích"},
    "uni-toronto": {"en": "University of Toronto", "cs": ""},
    "vfu": {"en": "University of Veterinary and Pharmaceutical Sciences Brno",
            "cs": "Veterinární a farmaceutická univerzita Brno"},
    "zcu": {"en": "University of West Bohemia", "cs": "Západočeská univerzita v Plzni"},
    "knihovna-usteckeho-kraje": {"en": "Ústí Regional Library", "cs": "Knihovna Ústeckého kraje"},
    "vyzkumny-ustav-veterinarniho-lekarstvi": {"en": "Veterinary Research Institute",
                                               "cs": "Výzkumný ústav veterinárního lékařství"},
    "vu": {"en": "Vrije Universiteit Amsterdam", "cs": ""},
    "vsb-tuo": {"en": "VSB - Technical University of Ostrava",
                "cs": "Vysoká škola báňská - Technická univerzita Ostrava"},
    "vuts-technicka-knihovna": {"en": "VUTS, JSC - Technical Library",
                                "cs": "Výzkumný ústav textilních strojů - technická knihovna"},
    "krajska-knihovna-vysociny": {"en": "Vysočina Regional Library", "cs": "Krajská knihovna Vysočiny"},
    "wigner": {"en": "Wigner Research Centre for Physics", "cs": ""},
    "wipo": {"en": "World Intellectual Property Organization", "cs": "Světová organizace duševního vlastnictví"},
    "xmu": {"en": "Xiamen University", "cs": ""},
    "woodexpert": {"en": "", "cs": "WOODEXPERT"},
    "ceitec": {"en": "", "cs": "CEITEC"},
    "comtes-fht": {"en": "", "cs": "COMTES FHT"},
    "unyp": {"en": "", "cs": "University of New York in Prague"},
    "cog-cz": {"en": "", "cs": "COG-CZ"},
    "cesnet": {"en": "", "cs": "CESNET"},
    "tescan": {"en": "", "cs": "TESCAN GROUP"},
    "atelier-krejcirikovi": {"en": "", "cs": "Ateliér Krejčiříkovi, s.r.o."},
    "hnuti-duha": {"en": "", "cs": "Hnutí DUHA - Friends of the Earth Czech Republic"},
    "kroupalide": {"en": "", "cs": "KROUPALIDÉ advokátní kancelář s.r.o."},
    "sociofactor": {"en": "", "cs": "SocioFactor s.r.o."},
    "jihomoravske-dobrovolnicke-centrum": {"en": "", "cs": "Jihomoravské dobrovolnické centrum z.s."},
    "dcul": {"en": "", "cs": "Dobrovolnické centrum, z. s."},
    "nidm": {"en": "", "cs": "Národní institut dětí a mládeže MŠMT"},
    "infodatasys": {"en": "", "cs": "Ing. Karel MATĚJKA, CSc.-IDS"},
    "staatsbetrieb-sachsenforst": {"en": "", "cs": "Staatsbetrieb Sachsenforst"},
    "cs-ustav-pro-vyzkum-verejneho-mineni": {"en": "", "cs": "Československý ústav pro výzkum veřejného mínění"},
    "iuf": {"en": "", "cs": ""},
    "avss-agritec-plant-research": {"en": "", "cs": "Agritec Plant Research"},
    "agrotest-fyto": {"en": "", "cs": "Agrotest fyto"},
    "prague-college": {"en": "", "cs": "Prague College"},
    "iure": {"en": "", "cs": "Iuridicum Remedium"},
}


def map_affiliation_by_name(zenodo_affiliation, database_affiliations=None):
    if database_affiliations is None:
        database_affiliations = aff_vocab

    matched_id = None
    matched_title = None

    for db_id, db_affiliation in database_affiliations.items():
        if db_affiliation['en'] and re.search(re.escape(db_affiliation['en']), zenodo_affiliation, re.IGNORECASE):
            matched_id = db_id
            matched_title = db_affiliation['en']
            break
        elif db_affiliation['cs'] and re.search(re.escape(db_affiliation['cs']), zenodo_affiliation, re.IGNORECASE):
            matched_id = db_id
            matched_title = db_affiliation['cs']
            break
        elif 'other_options' in db_affiliation:
            for option in db_affiliation['other_options']:
                if re.search(re.escape(option), zenodo_affiliation, re.IGNORECASE):
                    matched_id = db_id
                    matched_title = option
                    break
            if matched_id:
                break

    if matched_id:
        return {'id': matched_id, 'title': matched_title}
    else:
        return {'id': None, 'title': None}  # if nothing just return none, it will raise error during import

import json
import warnings
from collections import ChainMap
from json import JSONDecodeError
import uuid
from invenio_communities import current_communities
from invenio_search.engine import dsl
from invenio_access.permissions import system_identity
from datacite import DataCiteRESTClient
from datacite.errors import (
    DataCiteError,
    DataCiteNoContentError,
    DataCiteNotFoundError,
    DataCiteServerError,
)
from invenio_db import db
from invenio_pidstore.providers.base import BaseProvider
import requests
from oarepo_runtime.datastreams.utils import get_record_service_for_record

from marshmallow.exceptions import ValidationError
from flask import current_app

from invenio_pidstore.models import PIDStatus

from invenio_rdm_records.services.pids.providers.base import PIDProvider
from invenio_access.permissions import system_identity
from invenio_vocabularies.proxies import current_service as vocabulary_service

from babel_edtf import parse_edtf
from oarepo_runtime.i18n import lazy_gettext as _

# class OarepoDataCiteClient:
#     """DataCite Client."""
#
#     def __init__(self, name, config_prefix=None, config_overrides=None, **kwargs):
#         """Constructor."""
#         self.name = name
#         self._config_prefix = config_prefix or "DATACITE"
#         self._config_overrides = config_overrides or {}
#         self._api = None
#
#     def cfgkey(self, key):
#         """Generate a configuration key."""
#         return f"{self._config_prefix}_{key.upper()}"
#
#     def cfg(self, key, default=None):
#         """Get a application config value."""
#         config = ChainMap(self._config_overrides, current_app.config)
#         return config.get(self.cfgkey(key), default)
#
#     def generate_doi(self, record):
#         """Generate a DOI."""
#         pass
#
#     def check_credentials(self, **kwargs):
#         """Returns if the client has the credentials properly set up.
#
#         If the client is running on test mode the credentials are not required.
#         """
#         if not (self.cfg("username") and self.cfg("password") and self.cfg("prefix")):
#             warnings.warn(
#                 f"The {self.__class__.__name__} is misconfigured. Please "
#                 f"set {self.cfgkey('username')}, {self.cfgkey('password')}"
#                 f" and {self.cfgkey('prefix')} in your configuration.",
#                 UserWarning,
#             )
#
#     @property
#     def api(self):
#         """DataCite REST API client instance."""
#         if self._api is None:
#             self.check_credentials()
#             self._api = DataCiteRESTClient(
#                 self.cfg("username"),
#                 self.cfg("password"),
#                 self.cfg("prefix"),
#                 self.cfg("test_mode", True),
#             )
#         return self._api
# from invenio_rdm_records.services.pids.providers import DataCiteClient
from oarepo_doi.services.provider import OarepoDataCitePIDProvider
class NRDocsDataCitePIDProvider(OarepoDataCitePIDProvider):
    def create_datacite_payload(self, data):
        # mandatory
        metadata = data["metadata"]
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
        payload["url"] = data["links"]["self_html"]

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

    def validate(self, record, identifier=None, provider=None, **kwargs):
        """Validate the attributes of the identifier."""

        return True, []

    def metadata_check(self, record, schema=None, provider=None, **kwargs):
        missing_data_message = _("Missing data for required field.")

        errors = {}
        data = record["metadata"]
        if "creators" not in data:
            errors["metadata.creators"] = [missing_data_message]
        else:
            for i, creator in enumerate(data["creators"]):
                if "name" not in creator["person_or_org"]:
                    errors[f"metadata.creators.{i}.person_or_org.name"] = [missing_data_message]
                if "identifiers" in creator["person_or_org"]:
                    for j, id in enumerate(creator["person_or_org"]["identifiers"]):
                        if "scheme" not in id:
                            errors[
                                f"metadata.creators.{i}.person_or_org.name.identifiers.{j}.scheme"
                            ] = [missing_data_message]
        if "publishers" not in data:
            errors["metadata.publishers"] = [missing_data_message]
        if "contributors" in data:
            for i, contributor in enumerate(data["contributors"]):
                if "name" not in contributor["person_or_org"]:
                    errors[f"metadata.contributors.person_or_org.{i}.name"] = [
                        missing_data_message
                    ]
                if "identifiers" in contributor["person_or_org"]:
                    for j, id in enumerate(contributor["person_or_org"]["identifiers"]):
                        if "scheme" not in id:
                            errors[
                                f"metadata.contributors.{i}.person_or_org.identifiers.{j}.scheme"
                            ] = [missing_data_message]
        if "title" not in data:
            errors["metadata.title"] = [missing_data_message]
        if "resourceType" not in data:
            errors["metadata.resourceType"] = [missing_data_message]
        if "dateIssued" not in data:
            errors["metadata.dateIssued"] = [missing_data_message]
        if "relatedItems" in data:
            for i, item in enumerate(data["relatedItems"]):
                if "itemTitle" not in item:
                    errors[f"metadata.relatedItems.{i}.itemTitle"] = [
                        missing_data_message
                    ]
                if "itemRelationType" not in item:
                    errors[f"metadata.relatedItems.{i}.itemRelationType"] = [
                        missing_data_message
                    ]
                if "itemResourceType" not in item:
                    errors[f"metadata.relatedItems.{i}.itemResourceType"] = [
                        missing_data_message
                    ]

        return errors
# class OarepoDataCitePIDProvider(PIDProvider):
#     """DataCite Provider class.
#
#     Note that DataCite is only contacted when a DOI is reserved or
#     registered, or any action posterior to it. Its creation happens
#     only at PIDStore level.
#     """
#
#     def __init__(
#         self,
#         id_,
#         client=None,
#         serializer=None,
#         pid_type="doi",
#         default_status=PIDStatus.NEW,
#         **kwargs,
#     ):
#         """Constructor."""
#         super().__init__(
#             id_,
#             client=(client or DataCiteClient("datacite", config_prefix="DATACITE")),
#             pid_type=pid_type,
#             default_status=default_status,
#         )
#         self.serializer = serializer
#         self.username = None
#         self.password = None
#         self.prefix = None
#
#     @property
#     def mode(self):
#         return current_app.config.get("DATACITE_MODE")
#
#     @property
#     def url(self):
#         return current_app.config.get("DATACITE_URL")
#
#     @property
#     def specified_doi(self):
#         return current_app.config.get("DATACITE_SPECIFIED_ID")
#
#     def credentials(self, record):
#         slug = self.community_slug_for_credentials(
#             record.parent["communities"].get("default", None)
#         )
#         if not slug:
#             credentials = current_app.config.get(
#                 "DATACITE_CREDENTIALS_DEFAULT"
#             )
#         else:
#             credentials_def = current_app.config.get("DATACITE_CREDENTIALS")
#
#             credentials = credentials_def.get(slug, None)
#             if not credentials:
#                 credentials = current_app.config.get(
#                     "DATACITE_CREDENTIALS_DEFAULT"
#                 )
#         self.username = credentials["username"]
#         self.password = credentials["password"]
#         self.prefix = credentials["prefix"]
#
#     @staticmethod
#     def _log_errors(exception):
#         """Log errors from DataCiteError class."""
#         # DataCiteError will have the response msg as first arg
#         ex_txt = exception.args[0] or ""
#         if isinstance(exception, DataCiteNoContentError):
#             current_app.logger.error(f"No content error: {ex_txt}")
#         elif isinstance(exception, DataCiteServerError):
#             current_app.logger.error(f"DataCite internal server error: {ex_txt}")
#         else:
#             # Client error 4xx status code
#             try:
#                 ex_json = json.loads(ex_txt)
#             except JSONDecodeError:
#                 current_app.logger.error(f"Unknown error: {ex_txt}")
#                 return
#
#             # the `errors` field is only available when a 4xx error happened (not 500)
#             for error in ex_json.get("errors", []):
#                 reason = error["title"]
#                 field = error.get("source")  # set when missing/wrong required field
#                 error_prefix = f"Error in `{field}`: " if field else "Error: "
#                 current_app.logger.error(f"{error_prefix}{reason}")
#
#     def generate_id(self, record, **kwargs):
#         """Generate a unique DOI."""
#         pass #this is done on the datacite level
#
#     @classmethod
#     def is_enabled(cls, app):
#         """Determine if datacite is enabled or not."""
#         return True
#
#     def can_modify(self, pid, **kwargs):
#         """Checks if the PID can be modified."""
#         return not pid.is_registered() and not pid.is_reserved()
#
#     def register(self, pid, record, **kwargs):
#         """Register a DOI via the DataCite API.
#
#         :param pid: the PID to register.
#         :param record: the record metadata for the DOI.
#         :returns: `True` if is registered successfully.
#         """
#         pass
#
#     def community_slug_for_credentials(self, value):
#         if not value:
#             return None
#         id_value = None
#         slug = None
#         try:
#             id_value = uuid.UUID(value, version=4)
#         except:
#             slug = value
#         if not slug:
#             search = current_communities.service._search(
#                 "search",
#                 system_identity,
#                 {},
#                 None,
#                 extra_filter=dsl.Q("term", **{"id": value}),
#             )
#             community = search.execute()
#             c = list(community.hits.hits)[0]
#             return c._source.slug
#         return slug
#
#     def get_doi_value(self, record):
#         """Extracts DOI from the record."""
#
#         pids = record.get('pids', {})
#         if pids is None:
#             pids = {}
#         doi = None
#         if 'doi' in pids:
#             doi = pids['doi']['identifier']
#         return doi
#
#     def add_doi_value(self, record, data, doi_value):
#         """Adds a DOI to the record."""
#         pids = record.get('pids', {})
#         if pids is None:
#             pids = {}
#         pids["doi"] = {"provider": "datacite", "identifier": doi_value}
#         # try:
#         data.pids = pids
#         # except:
#         #     data["pids"] = pids
#         # try:
#         data.parent.pids = pids
#         # except:
#         #     data.parent["pids"] = pids
#
#         record.update(data)
#
#         record.parent.commit()
#         record.commit()
#
#     def remove_doi_value(self, record):
#         """Removes DOI from the record."""
#         pids = record.get('pids', {})
#         if pids is None:
#             pids = {}
#         if "doi" in pids:
#             pids.pop("doi")
#         record.commit()
#
#     def create(self, record, **kwargs):
#         pass
#
#     def create_and_reserve(self, record, **kwargs):
#         """Create and reserve a DOI for the given record, and update the record with the reserved DOI."""
#         doi_value = self.get_doi_value(record)
#         if doi_value:
#             raise ValidationError(
#                 message="DOI already associated with the record."
#             )
#         self.credentials(record)
#         errors = self.metadata_check(record)
#         record_service = get_record_service_for_record(record)
#         record["links"] = record_service.links_item_tpl.expand(system_identity, record)
#
#         if len(errors) > 0:
#             raise ValidationError(
#                 message=errors
#             )
#         request_metadata = {"data": {"type": "dois", "attributes": {}}}
#
#         payload = self.create_datacite_payload(record)
#         request_metadata["data"]["attributes"] = payload
#         if self.specified_doi:
#             doi = f"{self.prefix}/{record['id']}"
#             request_metadata["data"]["attributes"]["doi"] = doi
#         if "event" in kwargs:
#             # publish!!
#             request_metadata["data"]["attributes"]["event"] = kwargs["event"]
#
#         # request_metadata["data"]["attributes"]["event"] = "publish"
#         request_metadata["data"]["attributes"]["prefix"] = str(self.prefix)
#
#         request = requests.post(
#             url=self.url,
#             json=request_metadata,
#             headers={"Content-type": "application/vnd.api+json"},
#             auth=(self.username, self.password),
#         )
#
#         if request.status_code != 201:
#             raise requests.ConnectionError(
#                 "Expected status code 201, but got {}".format(request.status_code)
#             )
#
#         content = request.content.decode("utf-8")
#         json_content = json.loads(content)
#         doi_value = json_content["data"]["id"]
#         self.add_doi_value(record, record, doi_value)
#         if "event" in kwargs:
#             pid_status = 'R'  # registred
#         else:
#             pid_status = 'K'  # reserved
#         BaseProvider.create('doi', doi_value, 'rec', record.id, pid_status)
#         db.session.commit()
#
#     def update(self, record, url=None, **kwargs):
#
#
#         doi_value = self.get_doi_value(record)
#         if doi_value:
#             self.credentials(record)
#             errors = self.metadata_check(record)
#             record_service = get_record_service_for_record(record)
#             record["links"] = record_service.links_item_tpl.expand(system_identity, record)
#             if len(errors) > 0:
#                 raise ValidationError(
#                     message=errors
#                 )
#             if not self.url.endswith("/"):
#                 url = self.url + "/"
#             else:
#                 url = self.url
#             url = url + doi_value.replace("/", "%2F")
#
#             request_metadata = {"data": {"type": "dois", "attributes": {}}}
#             payload = self.create_datacite_payload(record)
#             request_metadata["data"]["attributes"] = payload
#
#             if "event" in kwargs:
#                request_metadata["data"]["attributes"]["event"] = kwargs["event"]
#
#             request = requests.put(
#                 url=url,
#                 json=request_metadata,
#                 headers={"Content-type": "application/vnd.api+json"},
#                 auth=(self.username, self.password),
#             )
#
#             if request.status_code != 200:
#                 raise requests.ConnectionError(
#                     "Expected status code 200, but got {}".format(request.status_code)
#                 )
#
#     def restore(self, pid, **kwargs):
#         """Restore previously deactivated DOI."""
#         pass
#
#     def delete(self, record, **kwargs):
#         """Delete/unregister a registered DOI.
#
#         If the PID has not been reserved then it's deleted only locally.
#         Otherwise, also it's deleted also remotely.
#         :returns: `True` if is deleted successfully.
#         """
#         doi_value = self.get_doi_value(record)
#
#         if not self.url.endswith("/"):
#             url = self.url + "/"
#         else:
#             url = self.url
#         url = url + doi_value.replace("/", "%2F")
#
#         headers = {
#             "Content-Type": "application/vnd.api+json"
#         }
#
#         self.credentials(record)
#
#         response = requests.delete(url=url, headers=headers, auth=(self.username, self.password))
#
#         if response.status_code != 204:
#             raise requests.ConnectionError(
#                 "Expected status code 204, but got {}".format(response.status_code)
#             )
#         else:
#             self.remove_doi_value(record)
#
#     def create_datacite_payload(self, data):
#         # mandatory
#         metadata = data["metadata"]
#         creators = creatibutor(metadata, "creators")
#         titles = title(metadata)
#         publishers = publisher(metadata)
#
#         dc_resource_type = resource_type(metadata)
#
#         payload = {}
#         payload["creators"] = creators
#         payload["titles"] = titles
#         payload["publisher"] = publishers
#         payload["types"] = {}
#         payload["types"]["resourceTypeGeneral"] = dc_resource_type
#
#         # optional
#         if "subjects" in metadata:
#             dc_subjects = subjects(metadata)
#             payload["subjects"] = dc_subjects
#         if "contributors" in metadata:
#             dc_contributors = creatibutor(metadata, "contributors")
#             payload["contributors"] = dc_contributors
#
#         date_obj = parse_edtf(metadata["dateIssued"])
#
#         year = date_obj.year
#
#         payload["publicationYear"] = year
#         payload["url"] = data["links"]["self_html"]
#
#         dc_dates = []
#         if "dateAvailable" in metadata:
#             dc_dates.append(
#                 {"date": metadata["dateAvailable"], "dateType": "Available"}
#             )
#         if "dateModified" in metadata:
#             dc_dates.append({"date": metadata["dateModified"], "dateType": "Updated"})
#         if "dateIssued" in metadata:
#             dc_dates.append({"date": metadata["dateIssued"], "dateType": "Issued"})
#         if len(dc_dates) > 0:
#             payload["dates"] = dc_dates
#
#         if "rights" in metadata:
#             dc_rights = []
#             right = metadata["rights"]
#             dc_rights.append(
#                 {"rights": right["title"], "rightsIdentifier": right["id"]}
#             )
#             if len(dc_rights) > 0:
#                 payload["rightsList"] = dc_rights
#         if "abstract" in metadata:
#             dc_descriptions = []
#             for abstr in metadata["abstract"]:
#                 dc_descriptions.append(
#                     {
#                         "lang": abstr["lang"],
#                         "description": abstr["value"],
#                         "descriptionType": "Abstract",
#                     }
#                 )
#             if len(dc_descriptions) > 0:
#                 payload["descriptions"] = dc_descriptions
#
#         if "funders" in metadata:
#             payload["fundingReferences"] = funder(metadata)
#
#         if "relatedItems" in metadata:
#             payload["relatedItems"], payload["relatedIdentifiers"] = related_items(
#                 metadata
#             )
#
#         if "languages" in metadata:
#             payload["language"] = metadata["languages"][0]["id"]
#
#         return payload
#
#     def validate(self, record, identifier=None, provider=None, **kwargs):
#         """Validate the attributes of the identifier."""
#
#         return True, []
#
#     def metadata_check(self, record, schema=None, provider=None, **kwargs):
#         missing_data_message = _("Missing data for required field.")
#
#         errors = {}
#         data = record["metadata"]
#         if "creators" not in data:
#             errors["metadata.creators"] = [missing_data_message]
#         else:
#             for i, creator in enumerate(data["creators"]):
#                 if "name" not in creator["person_or_org"]:
#                     errors[f"metadata.creators.{i}.person_or_org.name"] = [missing_data_message]
#                 if "identifiers" in creator["person_or_org"]:
#                     for j, id in enumerate(creator["person_or_org"]["identifiers"]):
#                         if "scheme" not in id:
#                             errors[
#                                 f"metadata.creators.{i}.person_or_org.name.identifiers.{j}.scheme"
#                             ] = [missing_data_message]
#         if "publishers" not in data:
#             errors["metadata.publishers"] = [missing_data_message]
#         if "contributors" in data:
#             for i, contributor in enumerate(data["contributors"]):
#                 if "name" not in contributor["person_or_org"]:
#                     errors[f"metadata.contributors.person_or_org.{i}.name"] = [
#                         missing_data_message
#                     ]
#                 if "identifiers" in contributor["person_or_org"]:
#                     for j, id in enumerate(contributor["person_or_org"]["identifiers"]):
#                         if "scheme" not in id:
#                             errors[
#                                 f"metadata.contributors.{i}.person_or_org.identifiers.{j}.scheme"
#                             ] = [missing_data_message]
#         if "title" not in data:
#             errors["metadata.title"] = [missing_data_message]
#         if "resourceType" not in data:
#             errors["metadata.resourceType"] = [missing_data_message]
#         if "dateIssued" not in data:
#             errors["metadata.dateIssued"] = [missing_data_message]
#         if "relatedItems" in data:
#             for i, item in enumerate(data["relatedItems"]):
#                 if "itemTitle" not in item:
#                     errors[f"metadata.relatedItems.{i}.itemTitle"] = [
#                         missing_data_message
#                     ]
#                 if "itemRelationType" not in item:
#                     errors[f"metadata.relatedItems.{i}.itemRelationType"] = [
#                         missing_data_message
#                     ]
#                 if "itemResourceType" not in item:
#                     errors[f"metadata.relatedItems.{i}.itemResourceType"] = [
#                         missing_data_message
#                     ]
#
#         return errors
#
#     def validate_restriction_level(self, record, identifier=None, **kwargs):
#         """Remove the DOI if the record is restricted."""
#         if record["access"]["record"] == "restricted":
#             return False


def publisher(data):
    if "publishers" in data:
        return {"name" :data["publishers"][0]}


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

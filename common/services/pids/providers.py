from invenio_access.permissions import system_identity
from invenio_vocabularies.proxies import current_service as vocabulary_service

from babel_edtf import parse_edtf
from oarepo_runtime.i18n import lazy_gettext as _
from oarepo_doi.services.provider import OarepoDataCitePIDProvider

class NRDocsDataCitePIDProvider(OarepoDataCitePIDProvider):

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
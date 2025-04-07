import json
import warnings
from collections import ChainMap
from json import JSONDecodeError

from datacite import DataCiteRESTClient
from datacite.errors import (
    DataCiteError,
    DataCiteNoContentError,
    DataCiteNotFoundError,
    DataCiteServerError,
)
from flask import current_app
from invenio_i18n import lazy_gettext as _
from invenio_pidstore.models import PIDStatus

from invenio_rdm_records.services.pids.providers.base import PIDProvider

class OarepoDataCiteClient:
    """DataCite Client."""

    def __init__(self, name, config_prefix=None, config_overrides=None, **kwargs):
        """Constructor."""
        self.name = name
        self._config_prefix = config_prefix or "DATACITE"
        self._config_overrides = config_overrides or {}
        self._api = None

    def cfgkey(self, key):
        """Generate a configuration key."""
        return f"{self._config_prefix}_{key.upper()}"

    def cfg(self, key, default=None):
        """Get a application config value."""
        config = ChainMap(self._config_overrides, current_app.config)
        return config.get(self.cfgkey(key), default)

    def generate_doi(self, record):
        """Generate a DOI."""
        self.check_credentials()
        prefix = self.cfg("prefix")
        if not prefix:
            raise RuntimeError("Invalid DOI prefix configured.")
        doi_format = self.cfg("format", "{prefix}/{id}")
        if callable(doi_format):
            return doi_format(prefix, record)
        else:
            return doi_format.format(prefix=prefix, id=record.pid.pid_value)

    def check_credentials(self, **kwargs):
        """Returns if the client has the credentials properly set up.

        If the client is running on test mode the credentials are not required.
        """
        if not (self.cfg("username") and self.cfg("password") and self.cfg("prefix")):
            warnings.warn(
                f"The {self.__class__.__name__} is misconfigured. Please "
                f"set {self.cfgkey('username')}, {self.cfgkey('password')}"
                f" and {self.cfgkey('prefix')} in your configuration.",
                UserWarning,
            )

    @property
    def api(self):
        """DataCite REST API client instance."""
        if self._api is None:
            self.check_credentials()
            self._api = DataCiteRESTClient(
                self.cfg("username"),
                self.cfg("password"),
                self.cfg("prefix"),
                self.cfg("test_mode", True),
            )
        return self._api


class OarepoDataCitePIDProvider(PIDProvider):
    """DataCite Provider class.

    Note that DataCite is only contacted when a DOI is reserved or
    registered, or any action posterior to it. Its creation happens
    only at PIDStore level.
    """

    def __init__(
        self,
        id_,
        client=None,
        serializer=None,
        pid_type="doi",
        default_status=PIDStatus.NEW,
        **kwargs,
    ):
        """Constructor."""
        super().__init__(
            id_,
            client=(client or OarepoDataCiteClient("datacite", config_prefix="DATACITE")),
            pid_type=pid_type,
            default_status=default_status,
        )
        self.serializer = serializer

    @staticmethod
    def _log_errors(exception):
        """Log errors from DataCiteError class."""
        # DataCiteError will have the response msg as first arg
        ex_txt = exception.args[0] or ""
        if isinstance(exception, DataCiteNoContentError):
            current_app.logger.error(f"No content error: {ex_txt}")
        elif isinstance(exception, DataCiteServerError):
            current_app.logger.error(f"DataCite internal server error: {ex_txt}")
        else:
            # Client error 4xx status code
            try:
                ex_json = json.loads(ex_txt)
            except JSONDecodeError:
                current_app.logger.error(f"Unknown error: {ex_txt}")
                return

            # the `errors` field is only available when a 4xx error happened (not 500)
            for error in ex_json.get("errors", []):
                reason = error["title"]
                field = error.get("source")  # set when missing/wrong required field
                error_prefix = f"Error in `{field}`: " if field else "Error: "
                current_app.logger.error(f"{error_prefix}{reason}")

    def generate_id(self, record, **kwargs):
        """Generate a unique DOI."""
        pass #this is done on the datacite level

    @classmethod
    def is_enabled(cls, app):
        """Determine if datacite is enabled or not."""
        return True

    def can_modify(self, pid, **kwargs):
        """Checks if the PID can be modified."""
        return not pid.is_registered() and not pid.is_reserved()

    def register(self, pid, record, **kwargs):
        """Register a DOI via the DataCite API.

        :param pid: the PID to register.
        :param record: the record metadata for the DOI.
        :returns: `True` if is registered successfully.
        """
        pass

    def update(self, pid, record, url=None, **kwargs):
        """Update metadata associated with a DOI.

        This can be called before/after a DOI is registered.
        :param pid: the PID to register.
        :param record: the record metadata for the DOI.
        :returns: `True` if is updated successfully.
        """
        pass

    def restore(self, pid, **kwargs):
        """Restore previously deactivated DOI."""
        pass

    def delete(self, pid, **kwargs):
        """Delete/unregister a registered DOI.

        If the PID has not been reserved then it's deleted only locally.
        Otherwise, also it's deleted also remotely.
        :returns: `True` if is deleted successfully.
        """
        try:
            if pid.is_reserved():  # Delete only works for draft DOIs
                self.client.api.delete_doi(pid.pid_value)
            elif pid.is_registered():
                self.client.api.hide_doi(pid.pid_value)
        except DataCiteError as e:
            current_app.logger.warning(
                f"DataCite provider error when deleting DOI for {pid.pid_value}"
            )
            self._log_errors(e)

            return False

        return super().delete(pid, **kwargs)

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

    def validate_restriction_level(self, record, identifier=None, **kwargs):
        """Remove the DOI if the record is restricted."""
        if identifier and record["access"]["record"] == "restricted":
            pid = self.get(identifier)
            if pid.status in [PIDStatus.NEW]:
                self.delete(pid)
                del record["pids"][self.pid_type]

    def create_and_reserve(self, record, **kwargs):
        """Create and reserve a DOI for the given record, and update the record with the reserved DOI."""
        if "doi" not in record.pids:
            pid = self.create(record)
            self.reserve(pid, record=record)
            pid_attrs = {"identifier": pid.pid_value, "provider": self.name}
            if self.client:
                pid_attrs["client"] = self.client.name
            record.pids["doi"] = pid_attrs

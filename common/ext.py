import re
from io import StringIO
from typing import Union

import yaml
from flask_principal import identity_loaded
from oarepo_oaipmh_harvester import cli  # noqa
from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.oai_harvester.records.api import OaiHarvesterRecord
from oarepo_runtime.datastreams.datastreams import Signature, SignatureKind

from . import (
    config,
)
from .cli import documents as documents_cli
from . import extension_registry # noqa

class OaiS3HarvesterExt(object):
    """extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.app = app
        app.extensions["oai_s3_harvester"] = self
        self.load_config(app)
        app.cli.add_command(documents_cli)

    def run(
        self,
        harvester_or_code: Union[str, OaiHarvesterRecord],
        all_records=False,
        on_background=False,
        identifiers=None,
        datestamp_from=None,
        datestamp_until=None,
    ):
        harvest(
            harvester_or_code=harvester_or_code,
            all_records=all_records,
            on_background=on_background,
            identifiers=identifiers,
            datestamp_from=datestamp_from,
            datestamp_until=datestamp_until,
        )

    def get_parser_signature(self, parser_name, **kwargs) -> Signature:
        parser_name, args = split_processor_name(parser_name)
        return Signature(
            kind=SignatureKind.READER, name=parser_name, kwargs={**args, **kwargs}
        )

    def get_transformer_signature(self, transformer, **kwargs) -> Signature:
        transformer, args = split_processor_name(transformer)
        return Signature(
            kind=SignatureKind.TRANSFORMER, name=transformer, kwargs={**args, **kwargs}
        )

    def get_writer_signature(self, writer, **kwargs) -> Signature:
        writer, args = split_processor_name(writer)
        return Signature(
            kind=SignatureKind.WRITER, name=writer, kwargs={**args, **kwargs}
        )

    def load_config(self, app):
        app.config.setdefault("DATASTREAMS_READERS", {}).update(
            config.DATASTREAMS_READERS
        )
        app.config.setdefault("DATASTREAMS_WRITERS", {}).update(
            config.DATASTREAMS_WRITERS
        )


def split_processor_name(processor):
    if "{" not in processor:
        return processor, {}
    processor, rest = processor.split("{", maxsplit=1)
    rest = "{" + rest
    rest = re.sub(r"([^\\])=", r"\1: ", rest)
    rest = re.sub(r"\\(.)", r"\1", rest)
    args = yaml.safe_load(StringIO(rest))
    return processor, args


class ActionPermissionsExt:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.extensions["action_permissions"] = self

        identity_loaded.connect_via(app)(load_action_permissions)


def load_action_permissions(sender, identity):
    # TODO: need to have a deeper look at this
    from flask_principal import ActionNeed
    from invenio_access.models import ActionUsers

    user_id = identity.id
    if user_id is None:
        return

    for au in ActionUsers.query.filter_by(user_id=user_id, exclude=False).all():
        identity.provides.add(ActionNeed(au.action))

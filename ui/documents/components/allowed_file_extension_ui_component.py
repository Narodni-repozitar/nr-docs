from typing import Dict

from flask import current_app
from flask_principal import Identity
from oarepo_ui.resources.components.base import UIResourceComponent


class AllowedFileExtensionUIComponent(UIResourceComponent):
    def form_config(
        self,
        *,
        data: Dict = None,
        identity: Identity,
        form_config: Dict,
        ui_links: Dict = None,
        extra_context: Dict = None,
        **kwargs,
    ):

        try:
            form_config["allowed_file_extensions"] = tuple(
                current_app.config["ALLOWED_DOCUMENT_FILE_EXTENSIONS"]
            )
        except KeyError:
            raise ValueError(
                "ALLOWED_DOCUMENT_FILE_EXTENSIONS not properly set in the invenio.cfg."
            )

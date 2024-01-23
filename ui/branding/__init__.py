from pathlib import Path

from flask import Blueprint
from flask_menu import current_menu
from oarepo_runtime.i18n import lazy_gettext as _

def create_blueprint(app):
    """Register blueprint for this resource."""
    template_folder = Path(__file__).parent.joinpath("templates").resolve()

    blueprint = Blueprint(
        "branding",
        __name__,
        url_prefix="/",
        template_folder=str(template_folder),
    )

    @blueprint.before_app_first_request
    def init_menu():
        """Initialize menu before first request."""
        current_menu.submenu("plus.create").register(
            "documents.create",
            _("New upload"),
            order=1,
        )

    # Add URL rules
    return blueprint
from pathlib import Path

from flask import Blueprint
from flask_menu import current_menu
from oarepo_runtime.i18n import lazy_gettext as _
from oarepo_ui.utils import can_view_deposit_page


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
        # session.clear()
        print(app.kvsession_store, "session_store", flush=True)
        print("before_first_request", flush=True)
        """Initialize menu before first request."""
        current_menu.submenu("plus.create").register(
            "documents.create",
            _("New upload"),
            order=1,
            # TODO: create function that checks if user has any permissions and as optimalization cache it in session
            visible_when=can_view_deposit_page,
        )

    # Add URL rules
    return blueprint

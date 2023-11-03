"""Additional views."""

from flask import Blueprint
from flask_menu import current_menu
from flask_babelex import lazy_gettext as _

#
# Registration
#
def create_blueprint(app):
    """Register blueprint routes on app."""
    blueprint = Blueprint(
        "nr_docs",
        __name__,
        template_folder="./templates",
    )

    @blueprint.before_app_first_request
    def init_menu():
        """Initialize menu before first request."""
        current_menu.submenu("plus.create").register(
            "docs-app.create",
            _("New upload"),
            order=1,
        )

    # Add URL rules
    return blueprint

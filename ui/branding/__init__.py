from pathlib import Path
from flask import Blueprint
from flask_menu import current_menu
from oarepo_runtime.i18n import lazy_gettext as _
from flask import g, session
from invenio_records_resources.proxies import current_service_registry

view_deposit_page_permission_key = f"view_deposit_page_permission"

def check_permissions():
    print(session, flush=True)
    print("check_permissions_menu", flush=True)

    if view_deposit_page_permission_key in session:
        return session[view_deposit_page_permission_key]
    else:
        documents_service = current_service_registry.get("documents")
        permission_to_create = documents_service.check_permission(
            g.identity, "view_deposit_page", record=None
        )
        session[view_deposit_page_permission_key] = permission_to_create

        print(permission_to_create, "documents_service", flush=True)

        return permission_to_create
    # documents_service = current_service_registry.get("documents")
    # permission_to_create = documents_service.check_permission(
    #     g.identity, "view_deposit_page", record=None
    # )
    # session["can_view_deposit_page"] = permission_to_create
    # print(permission_to_create, "documents_service", flush=True)

    # return permission_to_create

def clear_cached_permissions(*args, **kwargs):
    print("Clearing cached permissions", flush=True)
    session.pop(view_deposit_page_permission_key, None)


from flask_login import user_logged_in, user_logged_out
user_logged_in.connect(clear_cached_permissions)
user_logged_out.connect(clear_cached_permissions)


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
            visible_when=check_permissions,
        )
        # hide the /admin from the user dropdown (maximum recursion depth exceeded menu)
        current_menu.submenu("settings.admin").register(
            "admin.index",
            visible_when=lambda: False,
            order=100,
        )

    # Add URL rules
    return blueprint
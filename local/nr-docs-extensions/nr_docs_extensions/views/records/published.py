from flask import Blueprint
from nr_docs_extensions.services.published_service import get_published_service

def create_blueprint(app):
    blueprint = Blueprint("nr_documents_published", __name__, url_prefix="")
    blueprint.record_once(init_create_blueprint)
    return blueprint


def init_create_blueprint(state):
    """Init app."""
    app = state.app

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(
        get_published_service(), service_id="nr_documents_published"
    )
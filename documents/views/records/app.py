from flask import Blueprint


def create_app_blueprint(app):
    with app.app_context():
        blueprint = Blueprint("documents_app", __name__, url_prefix="/docs/")
        blueprint.record_once(init_create_app_blueprint)

        # calls record_once for all other functions starting with "init_addons_"
        # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
        funcs = globals()
        funcs = [
            v
            for k, v in funcs.items()
            if k.startswith("init_addons_documents") and callable(v)
        ]
        for func in funcs:
            blueprint.record_once(func)

    return blueprint


def init_create_app_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["documents"]

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(
        ext.service_records, service_id=ext.service_records.config.service_id
    )

    # Register indexer
    if hasattr(ext.service_records, "indexer"):
        iregistry = app.extensions["invenio-indexer"].registry
        iregistry.register(
            ext.service_records.indexer,
            indexer_id=ext.service_records.config.service_id,
        )


def init_addons_documents_requests(state):
    app = state.app
    requests = app.extensions["invenio-requests"]

    from documents import config

    for er in getattr(config, "DOCUMENTS_ENTITY_RESOLVERS", []):
        requests.entity_resolvers_registry.register_type(er)

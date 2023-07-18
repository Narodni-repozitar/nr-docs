def create_api_blueprint(app):
    """Create NrDocumentsRecord blueprint."""
    blueprint = app.extensions["nr_documents"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_nr_documents") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_documents"]

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


def init_addons_nr_documents_requests(state):
    app = state.app
    requests = app.extensions["invenio-requests"]

    from nr_documents import config as config

    for rt in getattr(config, "REQUESTS_REGISTERED_TYPES", []):
        requests.request_type_registry.register_type(rt)

    for er in getattr(config, "REQUESTS_ENTITY_RESOLVERS", []):
        requests.entity_resolvers_registry.register_type(er)


def create_api_blueprint(app):
    """Create NrDocumentsRecord blueprint."""
    blueprint = app.extensions["nr_documents"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_nr_documents") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_documents"]

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


def create_api_blueprint(app):
    """Create NrDocumentsRecord blueprint."""
    blueprint = app.extensions["nr_documents"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_nr_documents") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_documents"]

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


def create_api_blueprint(app):
    """Create NrDocumentsRecord blueprint."""
    blueprint = app.extensions["nr_documents"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_nr_documents") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_documents"]

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


def create_api_blueprint(app):
    """Create NrDocumentsRecord blueprint."""
    blueprint = app.extensions["nr_documents"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_nr_documents") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_documents"]

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


def create_api_blueprint(app):
    """Create NrDocumentsRecord blueprint."""
    blueprint = app.extensions["nr_documents"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_nr_documents") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_documents"]

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


def create_api_blueprint(app):
    """Create NrDocumentsRecord blueprint."""
    blueprint = app.extensions["nr_documents"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_nr_documents") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_documents"]

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


def create_api_blueprint(app):
    """Create NrDocumentsRecord blueprint."""
    blueprint = app.extensions["nr_documents"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_nr_documents") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_documents"]

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




def create_api_blueprint(app):
    """Create NrDocumentsRecord blueprint."""
    blueprint = app.extensions["nr_documents"].resource_records.as_blueprint()
    blueprint.record_once(init_create_api_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_nr_documents") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_api_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["nr_documents"]

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

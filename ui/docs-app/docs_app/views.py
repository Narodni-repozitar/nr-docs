from docs_app.proxies import current_ui

def create_blueprint(app):
    """Blueprint for the routes and resources provided by current ui's resource."""
    with app.app_context():
        app.extensions['oarepo_ui'].register_resource(current_ui.resource)
        return current_ui.resource.as_blueprint()

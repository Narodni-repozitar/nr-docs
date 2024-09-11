from oarepo_ui.resources.config import TemplatePageUIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource


class ComponentsResourceConfig(TemplatePageUIResourceConfig):
    url_prefix = "/"
    blueprint_name = "components"
    template_folder = "templates"


def create_blueprint(app):
    """Register blueprint for this resource."""
    blueprint = TemplatePageUIResource(ComponentsResourceConfig()).as_blueprint()

    return blueprint

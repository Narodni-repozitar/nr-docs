from oarepo_ui.resources.config import TemplatePageUIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource


class OverridablePlaygroundPageResourceConfig(TemplatePageUIResourceConfig):
    url_prefix = "/overridable-playground"
    blueprint_name = "overridable-playground"
    template_folder = "templates"
    pages = {
        "": "OverridablePlaygroundPage",
        # add a new page here. The key is the URL path, the value is the name of the template
        # then put <name>.jinja into the templates folder
    }


def create_blueprint(app):
    """Register blueprint for this resource."""
    return TemplatePageUIResource(OverridablePlaygroundPageResourceConfig()).as_blueprint()

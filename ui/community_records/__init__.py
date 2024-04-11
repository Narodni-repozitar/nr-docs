from oarepo_ui.resources.config import TemplatePageUIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource


class CommunityRecordsPageResourceConfig(TemplatePageUIResourceConfig):
    url_prefix = "/communities"
    blueprint_name = "community_records"
    template_folder = "templates"
    pages = {
        "<pid_value>": "CommunityRecordPage",
        # add a new page here. The key is the URL path, the value is the name of the template
        # then put <name>.jinja into the templates folder
    }


def create_blueprint(app):
    """Register blueprint for this resource."""
    return TemplatePageUIResource(CommunityRecordsPageResourceConfig()).as_blueprint()

from oarepo_ui.resources.config import TemplatePageUIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource


class DashboardPageResourceConfig(TemplatePageUIResourceConfig):
    url_prefix = "/me/"
    blueprint_name = "dashboard1"
    template_folder = "templates"
    pages = {
        "records": "DashboardRecordsPage",
        "communities" : "DashboardCommunitiesPage",
        "requests": "DashboardRequestsPage",
        # add a new page here. The key is the URL path, the value is the name of the template
        # then put <name>.jinja into the templates folder
    }


class DashboardPageResource(TemplatePageUIResource):
    def render_DashboardRecordsPage(self, **kwargs):
        return self.render("DashboardRecordsPage", **kwargs)
    
    def render_DashboardCommunitiesPage(self, **kwargs):
        return self.render("DashboardCommunitiesPage", **kwargs)
    
    def render_DashboardRequestsPage(self, **kwargs):
        return self.render("DashboardRequestsPage", **kwargs)
    

def create_blueprint(app):
    """Register blueprint for this resource."""
    return DashboardPageResource(DashboardPageResourceConfig()).as_blueprint()

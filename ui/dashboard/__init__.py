from oarepo_ui.resources.config import TemplatePageUIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource
from invenio_search_ui.searchconfig import FacetsConfig, SearchAppConfig, SortConfig



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
    
    
    def records_search_app_config(self, overrides={}, **kwargs):
        opts = dict(
            endpoint="/api/documents",
            headers={"Accept": "application/vnd.inveniordm.v1+json"},
            grid_view=False,
            sort=SortConfig(
            {
        "title": dict(
            title=("By Title"),
            fields=["metadata.title"],  # ES defaults to desc on `_score` field
        ),
        "bestmatch": dict(
            title=("Best match"),
            fields=["_score"],  # ES defaults to desc on `_score` field
        ),
        "newest": dict(
            title=("Newest"),
            fields=["-created"],
        ),
        "oldest": dict(
            title=("Oldest"),
            fields=["created"],
        ),
    }, {}, "oldest", "oldest"
        ),
            facets={},
            
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)


class DashboardPageResource(TemplatePageUIResource):
    def render_DashboardRecordsPage(self, **kwargs):
        search_app_config=self.config.records_search_app_config()
        return self.render("DashboardRecordsPage", search_app_config=search_app_config , **kwargs)
    
    def render_DashboardCommunitiesPage(self, **kwargs):
        return self.render("DashboardCommunitiesPage", **kwargs)
    
    def render_DashboardRequestsPage(self, **kwargs):
        return self.render("DashboardRequestsPage", **kwargs)
    

def create_blueprint(app):
    """Register blueprint for this resource."""
    return DashboardPageResource(DashboardPageResourceConfig()).as_blueprint()

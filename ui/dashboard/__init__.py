from oarepo_ui.resources.config import TemplatePageUIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource
from invenio_search_ui.searchconfig import FacetsConfig, SearchAppConfig, SortConfig



class DashboardPageResourceConfig(TemplatePageUIResourceConfig):
    url_prefix = "/me/"
    blueprint_name = "dashboard"
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
            app_id="UserDashboard.records",
            endpoint="/api/docs",
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
    }, {
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
    }, "newest", "newest"
        ),
            facets={},
            
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)
    
    def requests_search_app_config(self, overrides={}, **kwargs):
        opts = dict(
            app_id="UserDashboard.requests",
            endpoint="/api/requests",
            headers={"Accept": "application/json"},
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
    }, {
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
    }, "newest", "newest"
        ),
            facets={},
            
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)
    
    def communities_search_app_config(self, overrides={}, **kwargs):
        opts = dict(
            app_id="UserDashboard.communities",
            endpoint="/api/user/communities",
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
    }, {
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
    }, "newest", "newest"
        ),
            facets={},
            
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)


class DashboardPageResource(TemplatePageUIResource):
    def render_DashboardRecordsPage(self, **kwargs):
        search_app_config=self.config.records_search_app_config(overrides={"defaultSortingOnEmptyQueryString": {"sortBy": "newest"}})
        return self.render("DashboardRecordsPage", search_app_config=search_app_config , **kwargs)
    
    def render_DashboardCommunitiesPage(self, **kwargs):
        search_app_config=self.config.communities_search_app_config(overrides={"defaultSortingOnEmptyQueryString": {"sortBy": "newest"}})
        return self.render("DashboardCommunitiesPage", search_app_config=search_app_config, **kwargs)
    
    def render_DashboardRequestsPage(self, **kwargs):
        search_app_config=self.config.requests_search_app_config(overrides={"defaultSortingOnEmptyQueryString": {"sortBy": "newest"}})
        return self.render("DashboardRequestsPage", search_app_config=search_app_config, **kwargs)
    

def create_blueprint(app):
    """Register blueprint for this resource."""
    return DashboardPageResource(DashboardPageResourceConfig()).as_blueprint()

from oarepo_ui.resources.config import TemplatePageUIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource
from invenio_search_ui.searchconfig import FacetsConfig, SearchAppConfig, SortConfig
from invenio_records_resources.proxies import current_service_registry
from flask_menu import current_menu
from flask_babelex import lazy_gettext as _


class DashboardPageResourceConfig(TemplatePageUIResourceConfig):
    url_prefix = "/me/"
    blueprint_name = "dashboard"
    template_folder = "templates"
    pages = {
        "records": "DashboardRecordsPage",
        "communities": "DashboardCommunitiesPage",
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
                        fields=[
                            "metadata.title"
                        ],  # ES defaults to desc on `_score` field
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
                },
                {
                    "title": dict(
                        title=("By Title"),
                        fields=[
                            "metadata.title"
                        ],  # ES defaults to desc on `_score` field
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
                },
                "newest",
                "newest",
            ),
            facets={},
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)

    def requests_search_app_config(self, overrides={}, **kwargs):
        requests_service = current_service_registry.get("requests")
        requests_config = requests_service.config
        search_facets = requests_config.search.facets
        facets = self.search_facets_config(search_facets, search_facets.keys())
        opts = dict(
            app_id="UserDashboard.requests",
            endpoint="/api/requests",
            headers={"Accept": "application/json"},
            # initial_filters=[["status", "created"], ["type", "publish_draft"]],
            initial_filters=[["is_open", "true"]],
            sort=SortConfig(
                {
                    "title": dict(
                        title=("By Title"),
                        fields=[
                            "metadata.title"
                        ],  # ES defaults to desc on `_score` field
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
                },
                {
                    "title": dict(
                        title=("By Title"),
                        fields=[
                            "metadata.title"
                        ],  # ES defaults to desc on `_score` field
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
                },
                "newest",
                "newest",
            ),
            facets=facets,
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)

    def search_facets_config(self, available_facets, selected_facets=[]):
        facets_config = {}
        for facet_key, facet in available_facets.items():
            facets_config[facet_key] = {
                "facet": facet,
                "ui": {
                    "field": facet._params.get("field", facet_key),
                },
            }

        return FacetsConfig(facets_config, selected_facets)

    def communities_search_app_config(self, overrides={}, **kwargs):
        community_service = current_service_registry.get("communities")
        community_config = community_service.config
        search_facets = community_config.search.facets
        facets = self.search_facets_config(search_facets, search_facets.keys())
        opts = dict(
            app_id="UserDashboard.communities",
            endpoint="/api/user/communities",
            headers={"Accept": "application/vnd.inveniordm.v1+json"},
            grid_view=False,
            sort=SortConfig(
                {
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
                },
                {
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
                },
                "newest",
                "newest",
            ),
            facets=facets,
        )
        opts.update(kwargs)
        return SearchAppConfig.generate(opts, **overrides)


class DashboardPageResource(TemplatePageUIResource):
    def render_DashboardRecordsPage(self, **kwargs):
        search_app_config = self.config.records_search_app_config(
            overrides={"defaultSortingOnEmptyQueryString": {"sortBy": "newest"}}
        )
        return self.render(
            "DashboardRecordsPage", search_app_config=search_app_config, **kwargs
        )

    def render_DashboardCommunitiesPage(self, **kwargs):
        search_app_config = self.config.communities_search_app_config(
            overrides={"defaultSortingOnEmptyQueryString": {"sortBy": "newest"}}
        )
        return self.render(
            "DashboardCommunitiesPage", search_app_config=search_app_config, **kwargs
        )

    def render_DashboardRequestsPage(self, **kwargs):
        search_app_config = self.config.requests_search_app_config(
            overrides={"defaultSortingOnEmptyQueryString": {"sortBy": "newest"}}
        )
        return self.render(
            "DashboardRequestsPage", search_app_config=search_app_config, **kwargs
        )


def create_blueprint(app):
    """Register blueprint for this resource."""
    app_blueprint = DashboardPageResource(DashboardPageResourceConfig()).as_blueprint()

    @app_blueprint.before_app_first_request
    def init_menu():
        user_dashboard = current_menu.submenu("user_dashboard")
        user_dashboard.submenu("records").register(
            "dashboard.render_DashboardRecordsPage",
            text="Records",
            order=1,
        )

        user_dashboard.submenu("communities").register(
            "dashboard.render_DashboardCommunitiesPage",
            text="Communities",
            order=2,
        )

        user_dashboard.submenu("requests").register(
            "dashboard.render_DashboardRequestsPage",
            text="Requests",
            order=3,
        )

    return app_blueprint

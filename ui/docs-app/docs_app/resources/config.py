from oarepo_ui.resources.config import RecordsUIResourceConfig
from oarepo_ui.resources import BabelComponent, PermissionsComponent
from oarepo_vocabularies.ui.resources.components import (
    DepositVocabularyOptionsComponent,
)


class DocsAppResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/docs/"
    blueprint_name = "docs-app"
    ui_serializer_class = (
        "nr_documents.resources.records.ui.NrDocumentsUIJSONSerializer"
    )
    api_service = "nr_documents"
    layout = "nr_documents"
    components = [
        BabelComponent,
        DepositVocabularyOptionsComponent,
        PermissionsComponent,
    ]

    templates = {
        "detail": {
            "layout": "docs_app/Detail.html.jinja",
            "blocks": {
                "record_main_content": "Main",
                "record_sidebar": "Sidebar",
            },
        },
        "search": {"layout": "docs_app/search.html"},
        "edit": {"layout": "docs_app/deposit.html"},
        "create": {"layout": "docs_app/deposit.html"},
    }

    def search_active_facets(self, api_config, identity):
        return [
            k
            for k in self.search_available_facets(api_config, identity).keys()
            # TODO: replace with a more generic `item.filterable` attribute check
            if not k.startswith("metadata_abstract")
        ]

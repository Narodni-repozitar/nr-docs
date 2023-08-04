from oarepo_ui.resources.config import RecordsUIResourceConfig
from oarepo_ui.resources import BabelComponent
from oarepo_vocabularies.ui.resources.components import DepositVocabularyOptionsComponent


class DocsAppResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/docs/"
    blueprint_name = "docs-app"
    ui_serializer_class = (
        "nr_documents.resources.records.ui.NrDocumentsUIJSONSerializer"
    )
    api_service = "nr_documents"
    layout = "nr_documents"
    components = [BabelComponent, DepositVocabularyOptionsComponent]

    templates = {
        "detail": {
            "layout": "docs_app/detail.html",
            "blocks": {
                "record_main_content": "docs_app/main.html",
                "record_sidebar": "docs_app/sidebar.html",
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

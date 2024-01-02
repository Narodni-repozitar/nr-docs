from oarepo_ui.resources.config import RecordsUIResourceConfig
from oarepo_ui.resources import BabelComponent, PermissionsComponent
from oarepo_ui.resources.components import FilesComponent
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
        FilesComponent
    ]
    search_app_id = "DocsApp.Search"

    templates = {
        "detail": "docs_app.Detail",
        "search": "docs_app.Search",
        "edit": "docs_app.Deposit",
        "create": "docs_app.Deposit",
    }

    def search_active_facets(self, api_config, identity):
        return [
            k
            for k in self.search_available_facets(api_config, identity).keys()
            # TODO: replace with a more generic `item.filterable` attribute check
            if not k.startswith("metadata_abstract")
        ]


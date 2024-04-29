from oarepo_ui.resources import BabelComponent, PermissionsComponent
from oarepo_ui.resources.components import FilesComponent
from oarepo_vocabularies.ui.resources.components import (
    DepositVocabularyOptionsComponent,
)
from oarepo_ui.resources.config import RecordsUIResourceConfig
from oarepo_ui.resources.resource import RecordsUIResource


class DocumentsResourceConfig(RecordsUIResourceConfig):
    template_folder = "templates"
    url_prefix = "/docs/"
    blueprint_name = "documents"
    ui_serializer_class = "documents.resources.records.ui.DocumentsUIJSONSerializer"
    api_service = "documents"

    components = [
        BabelComponent,
        DepositVocabularyOptionsComponent,
        PermissionsComponent,
        FilesComponent,
    ]
    
    search_component = "documents/search/ResultsListItem.jsx"
    application_id = "documents"

    templates = {
        "detail": "documents.Detail",
        "search": "documents.Search",
        "edit": "documents.Deposit",
        "create": "documents.Deposit",
    }

    def search_active_facets(self, api_config, identity):
        return [
            k
            for k in self.search_available_facets(api_config, identity).keys()
            # TODO: replace with a more generic `item.filterable` attribute check
            if not k.startswith("metadata_abstract")
        ]


class DocumentsResource(RecordsUIResource):
    pass


def create_blueprint(app):
    """Register blueprint for this resource."""
    return DocumentsResource(DocumentsResourceConfig()).as_blueprint()

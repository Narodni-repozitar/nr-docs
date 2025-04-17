from oarepo_ui.resources import BabelComponent, PermissionsComponent
from oarepo_ui.resources.components import (
    AllowedCommunitiesComponent,
    AllowedHtmlTagsComponent,
    EmptyRecordAccessComponent,
    FilesComponent,
    FilesLockedComponent,
    RecordRestrictionComponent,
)
from oarepo_ui.ui.components import UIComponent
from oarepo_ui.resources.components.custom_fields import CustomFieldsComponent
from oarepo_ui.resources.config import RecordsUIResourceConfig
from oarepo_ui.resources.resource import RecordsUIResource
from oarepo_vocabularies.ui.resources.components import (
    DepositVocabularyOptionsComponent,
)

from ui.documents.components.allowed_file_extension_ui_component import (
    AllowedFileExtensionUIComponent,
)


class DocumentsUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "templates"
    url_prefix = "/docs/"
    blueprint_name = "documents"
    ui_serializer_class = "documents.resources.records.ui.DocumentsUIJSONSerializer"
    api_service = "documents"

    components = [
        AllowedHtmlTagsComponent,
        BabelComponent,
        DepositVocabularyOptionsComponent,
        PermissionsComponent,
        FilesComponent,
        AllowedCommunitiesComponent,
        CustomFieldsComponent,
        RecordRestrictionComponent,
        EmptyRecordAccessComponent,
        FilesLockedComponent,
        AllowedFileExtensionUIComponent,
    ]

    search_component = UIComponent("DocumentsResultsListItem", "@js/documents/search/ResultsListItem", "default")
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


class DocumentsUIResource(RecordsUIResource):
    pass


def create_blueprint(app):
    """Register blueprint for this resource."""
    return DocumentsUIResource(DocumentsUIResourceConfig()).as_blueprint()

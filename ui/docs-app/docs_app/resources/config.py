from oarepo_ui.resources.config import RecordsUIResourceConfig


class DocsAppResourceConfig(RecordsUIResourceConfig):
    template_folder = "../templates"
    url_prefix = "/docs/"
    blueprint_name = "docs-app"
    ui_serializer_class = (
        "nr_documents.resources.records.ui.NrDocumentsUIJSONSerializer"
    )
    api_service = "nr_documents"
    layout = "nr_documents"

    templates = {
        "detail": {
            "layout": "docs_app/detail.html",
            "blocks": {
                "record_main_content": "docs_app/main.html",
                "record_sidebar": "docs_app/sidebar.html",
            },
        },
        "search": {"layout": "docs_app/search.html"},
    }

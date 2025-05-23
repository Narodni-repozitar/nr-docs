from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "documents_search": "./js/documents/search/index.js",
                "documents_deposit_form": "./js/documents/forms/index.js",
            },
            dependencies={
                "react-dnd-test-backend": "^16.0.1",
                "@oarepo/file-manager": "^1.1.0",
            },
            devDependencies={},
            aliases={"@js/documents": "./js/documents"},
        )
    },
)

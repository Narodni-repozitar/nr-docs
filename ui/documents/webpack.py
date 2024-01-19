from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "documents_search": "./js/documents/search/index.js",
                "documents_deposit_form": "./js/documents/forms/deposit/index.js",
            },
            dependencies={
                "react-searchkit": "^2.0.0",
                "react-dnd-test-backend": "^16.0.1",
            },
            devDependencies={},
            aliases={},
        )
    },
)

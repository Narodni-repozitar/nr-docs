from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "docs_app_components": "./js/docs_app/custom-components.js"
            },
            dependencies={
            },
            devDependencies={
            },
            aliases={
            }
        )
    },
)

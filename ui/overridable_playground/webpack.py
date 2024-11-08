from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
            },
            dependencies={
            },
            devDependencies={},
        )
    },
)

"""JS/CSS Webpack bundles for Document part of the Czech National Repository."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "base-theme-nr-docs": "./js/nr_docs/theme.js",
            },
        ),
    },
)

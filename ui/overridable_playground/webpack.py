from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "shared": ['react', 'react-dom', 'redux', 'react-redux', 'react-invenio-forms', 'react-searchkit', 'react-overridable'],
                "playground": {"import": "./js/playground/index.js", "dependOn": ['mycomponents', 'shared']},
                # "playground": "./js/playground/index.js",
                "mycomponents": "./js/playground/mycomponents/index.js",
            },
            dependencies={
                "@loadable/component": "^5.16.4"
            },
            aliases={"@mycomponents": "./js/playground/mycomponents"},
            devDependencies={},
        )
    },
)

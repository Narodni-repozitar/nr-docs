from flask import current_app
from werkzeug.local import LocalProxy

current_ui = LocalProxy(lambda: current_app.extensions["docs_app"])
"""Proxy to the instantiated ui extension."""

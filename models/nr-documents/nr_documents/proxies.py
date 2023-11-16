from flask import current_app
from werkzeug.local import LocalProxy


def _ext_proxy(attr):
    return LocalProxy(lambda: getattr(current_app.extensions["nr_documents"], attr))


current_service = _ext_proxy("service_records")
current_published_service = _ext_proxy("published_service_records")


current_record_communities_service = _ext_proxy("service_record_communities")


current_community_records_service = _ext_proxy("service_community_records")
"""Proxy to the instantiated service."""
"""Proxy to the instantiated vocabulary service."""


current_resource = _ext_proxy("resource_records")


current_record_communities_resource = _ext_proxy("resource_record_communities")


current_community_records_resource = _ext_proxy("resource_community_records")
"""Proxy to the instantiated resource."""

import pytest
from invenio_communities import current_communities
from invenio_communities.communities.records.api import Community
from invenio_pidstore.errors import PIDDoesNotExistError


@pytest.fixture()
def community_owner(UserFixture, app, db):
    """Community owner."""
    u = UserFixture(
        email="community_owner@inveniosoftware.org",
        password="community_owner",
    )
    u.create(app, db)
    return u


@pytest.fixture(scope="module")
def minimal_community():
    """Minimal community metadata."""
    return {
        "access": {
            "visibility": "public",
            "record_policy": "open",
        },
        "slug": "public",
        "metadata": {
            "title": "My Community",
        },
    }


@pytest.fixture(scope="module", autouse=True)
def location(location):
    return location


@pytest.fixture(scope="module")
def app_config(app_config):
    app_config["FILES_REST_STORAGE_CLASS_LIST"] = {
        "L": "Local",
        "F": "Fetch",
        "R": "Remote",
    }
    app_config["FILES_REST_DEFAULT_STORAGE_CLASS"] = "L"

    return app_config


@pytest.fixture()
def get_or_create_community():
    def _get_or_create_community(community_dict, identity):
        """Util to get or create community, to avoid duplicate error."""
        slug = community_dict["slug"]
        try:
            c = current_communities.service.record_cls.pid.resolve(slug)
        except PIDDoesNotExistError:
            c = current_communities.service.create(
                identity,
                community_dict,
            )
            Community.index.refresh()
            c = current_communities.service.record_cls.pid.resolve(slug)
        return c

    return _get_or_create_community

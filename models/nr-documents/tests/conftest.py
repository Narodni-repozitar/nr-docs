import os
from pathlib import Path

import pytest
import yaml
from flask_security import login_user
from flask_security.utils import hash_password
from invenio_access import ActionUsers, current_access
from invenio_access.permissions import system_identity
from invenio_accounts.proxies import current_datastore
from invenio_accounts.testutils import login_user_via_session
from invenio_app.factory import create_api
from invenio_records_resources.services.uow import RecordCommitOp, UnitOfWork

from nr_documents.proxies import current_service
from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord
from nr_documents.resources.records.config import NrDocumentsResourceConfig

BASE_URLS = {
    "base_url": NrDocumentsResourceConfig.url_prefix,
    "base_html_url": "/docs/",
}

APP_CONFIG = {
    "JSONSCHEMAS_HOST": "localhost",
    "RECORDS_REFRESOLVER_CLS": "invenio_records.resolver.InvenioRefResolver",
    "RECORDS_REFRESOLVER_STORE": (
        "invenio_jsonschemas.proxies.current_refresolver_store"
    ),
    "RATELIMIT_AUTHENTICATED_USER": "200 per second",
    "SEARCH_HOSTS": [
        {
            "host": os.environ.get("OPENSEARCH_HOST", "localhost"),
            "port": os.environ.get("OPENSEARCH_PORT", "9200"),
        }
    ],
    # disable redis cache
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}


@pytest.fixture
def base_urls():
    return BASE_URLS


@pytest.fixture
def record_service():
    return current_service


@pytest.fixture(scope="function")
def sample_metadata_list():
    data_path = f"{Path(__file__).parent.parent}/data/sample_data.yaml"
    docs = list(yaml.load_all(open(data_path), Loader=yaml.SafeLoader))
    return docs


@pytest.fixture()
def input_data(sample_metadata_list):
    return sample_metadata_list[0]


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return create_api


@pytest.fixture(scope="module")
def app_config(app_config):
    for k, v in APP_CONFIG.items():
        app_config[k] = v
    return app_config


@pytest.fixture(scope="function")
def sample_record(app, db, input_data):
    # record = current_service.create(system_identity, sample_data[0])
    # return record
    with UnitOfWork(db.session) as uow:
        record = NrDocumentsRecord.create(input_data)
        uow.register(RecordCommitOp(record, current_service.indexer, True))
        uow.commit()
        return record


@pytest.fixture(scope="function")
def sample_records(app, db, sample_metadata_list):
    # record = current_service.create(system_identity, sample_data[0])
    # return record
    with UnitOfWork(db.session) as uow:
        records = []
        for sample_metadata in sample_metadata_list:
            record = NrDocumentsRecord.create(sample_metadata)
            uow.register(RecordCommitOp(record, current_service.indexer, True))
            records.append(record)
        uow.commit()
        return records


@pytest.fixture()
def user(app, db):
    """Create example user."""
    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore
        _user = datastore.create_user(
            email="info@inveniosoftware.org",
            password=hash_password("password"),
            active=True,
        )
    db.session.commit()
    return _user


@pytest.fixture()
def role(app, db):
    """Create some roles."""
    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore
        role = datastore.create_role(name="admin", description="admin role")

    db.session.commit()
    return role


@pytest.fixture()
def client_with_credentials(db, client, user, role, sample_metadata_list):
    """Log in a user to the client."""

    current_datastore.add_role_to_user(user, role)
    action = current_access.actions["superuser-access"]
    db.session.add(ActionUsers.allow(action, user_id=user.id))

    login_user(user, remember=True)
    login_user_via_session(client, email=user.email)

    return client


@pytest.fixture(scope="function")
def sample_draft(app, db, input_data):
    with UnitOfWork(db.session) as uow:
        record = NrDocumentsDraft.create(input_data)
        uow.register(RecordCommitOp(record, current_service.indexer, True))
        uow.commit()
        return record


@pytest.fixture()
def vocab_cf(app, db, cache):
    from oarepo_runtime.cf.mappings import prepare_cf_indices

    prepare_cf_indices()


@pytest.fixture
def published_record_factory(record_service):
    """Create a draft and publish it."""

    def create_record(input_data):
        draft = record_service.create(system_identity, input_data)
        published_record = record_service.publish(system_identity, draft.data["id"])
        record = NrDocumentsRecord.pid.resolve(published_record["id"])
        return record

    return create_record


@pytest.fixture
def sample_published_record(record_service, published_record_factory, input_data):
    """Create a draft and publish it."""
    return published_record_factory(input_data)

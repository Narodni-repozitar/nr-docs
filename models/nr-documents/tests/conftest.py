import json
import os
from pathlib import Path

import pytest
import yaml
from flask_security import login_user
from flask_security.utils import hash_password
from invenio_access import ActionUsers, current_access
from invenio_accounts.proxies import current_datastore
from invenio_accounts.testutils import login_user_via_session
from invenio_app.factory import create_api
from invenio_records_resources.services.uow import RecordCommitOp, UnitOfWork

from invenio_cache import current_cache

from nr_documents.proxies import current_service
from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord


@pytest.fixture
def record_service():
    return current_service


@pytest.fixture(scope="function")
def sample_metadata_list():
    data_path = f"{Path(__file__).parent}/data1.json"
    docs = [json.load(open(data_path, 'r'))]
    return docs


@pytest.fixture()
def input_data(sample_metadata_list):
    return sample_metadata_list[0]


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return create_api

# FIXME: https://github.com/inveniosoftware/pytest-invenio/issues/30
# Without this, success of test depends on the tests order
@pytest.fixture()
def cache():
    """Empty cache."""
    try:
        yield current_cache
    finally:
        current_cache.clear()

@pytest.fixture()
def vocab_cf(app, db, cache):
    from oarepo_runtime.cf.mappings import prepare_cf_indices

    prepare_cf_indices()

@pytest.fixture(scope="module")
def app_config(app_config):
    """Mimic an instance's configuration."""
    app_config["JSONSCHEMAS_HOST"] = "localhost"
    app_config["RECORDS_REFRESOLVER_CLS"] = (
        "invenio_records.resolver.InvenioRefResolver"
    )
    app_config["RECORDS_REFRESOLVER_STORE"] = (
        "invenio_jsonschemas.proxies.current_refresolver_store"
    )
    app_config["RATELIMIT_AUTHENTICATED_USER"] = "200 per second"
    app_config["SEARCH_HOSTS"] = [
        {
            "host": os.environ.get("OPENSEARCH_HOST", "localhost"),
            "port": os.environ.get("OPENSEARCH_PORT", "9200"),
        }
    ]
    # disable redis cache
    app_config["CACHE_TYPE"] = "SimpleCache"  # Flask-Caching related configs
    app_config["CACHE_DEFAULT_TIMEOUT"] = 300

    # note: This line must always be added to the invenio.cfg file
    from oarepo_vocabularies.resources.config import VocabulariesResourceConfig
    from oarepo_vocabularies.services.config import (
        VocabulariesConfig,
        VocabularyTypeServiceConfig,
    )
    from oarepo_vocabularies.services.service import VocabularyTypeService
    from oarepo_vocabularies.resources.vocabulary_type import (
        VocabularyTypeResource,
        VocabularyTypeResourceConfig
    )
    from oarepo_vocabularies.authorities.resources import (
        AuthoritativeVocabulariesResource,
        AuthoritativeVocabulariesResourceConfig
    )

    app_config["VOCABULARIES_SERVICE_CONFIG"] = VocabulariesConfig
    app_config["VOCABULARIES_RESOURCE_CONFIG"] = VocabulariesResourceConfig

    app_config["OAREPO_VOCABULARIES_TYPE_SERVICE"] = VocabularyTypeService
    app_config["OAREPO_VOCABULARIES_TYPE_SERVICE_CONFIG"] = VocabularyTypeServiceConfig

    app_config["VOCABULARY_TYPE_RESOURCE"] = VocabularyTypeResource
    app_config["VOCABULARY_TYPE_RESOURCE_CONFIG"] = VocabularyTypeResourceConfig

    app_config["VOCABULARIES_AUTHORITIES"] = AuthoritativeVocabulariesResource
    app_config["VOCABULARIES_AUTHORITIES_CONFIG"] = AuthoritativeVocabulariesResourceConfig

    from invenio_records_resources.services.custom_fields.text import KeywordCF
    from invenio_records_resources.services.custom_fields.boolean import BooleanCF

    from tests.customfields import HintCF, NonPreferredLabelsCF, RelatedURICF

    app_config["OAREPO_VOCABULARIES_CUSTOM_CF"] = [
        KeywordCF("blah"),
        RelatedURICF("relatedURI"),
        HintCF("hint"),
        NonPreferredLabelsCF("nonpreferredLabels"),
    ]

    app_config["HAS_DRAFT"] = [
        BooleanCF("has_draft")
    ]

    # disable redis cache
    app_config["CACHE_TYPE"] = "SimpleCache"  # Flask-Caching related configs
    app_config["CACHE_DEFAULT_TIMEOUT"] = 300

    app_config["INVENIO_VOCABULARY_TYPE_METADATA"] = {
        "languages": {
            "name": {
                "cs": "jazyky",
                "en": "languages",
            },
            "description": {
                "cs": "slovnikovy typ ceskeho jazyka.",
                "en": "czech language vocabulary type.",
            },
        },
        "licenses": {
            "name": {
                "cs": "license",
                "en": "licenses",
            },
            "description": {
                "cs": "slovnikovy typ licencii.",
                "en": "lincenses vocabulary type.",
            },
        },
    }

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

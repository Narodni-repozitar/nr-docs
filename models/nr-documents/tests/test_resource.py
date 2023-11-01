import copy

import pytest
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    SystemProcess,
)

# todo move to conftest
from invenio_records_resources.services.custom_fields import BooleanCF

from nr_documents.proxies import current_service
from nr_documents.records.api import NrDocumentsDraft, NrDocumentsRecord
from nr_documents.resources.records.config import NrDocumentsResourceConfig


def _get_paths(cur_path, cur_val):
    ret_paths = []
    if isinstance(cur_val, list):
        return ret_paths
    elif isinstance(cur_val, dict):
        for k, v in cur_val.items():
            ret_paths += get_paths(f"{cur_path}.{k}", v)
    else:
        if cur_path.startswith("."):
            cur_path = cur_path[1:]
        ret_paths.append(f"{cur_path}")
    return ret_paths


def get_paths(prefix, data):
    return _get_paths(prefix, data)


"""
def check_allowed(action_name):
    permission_cls = current_service.config.permission_policy_cls
    permission = permission_cls(action_name)
    identity = g.identity
    auth = permission.allows(identity)
    return auth
"""


def is_action_allowed(action_name, user_is_auth):
    permission_cls = current_service.config.permission_policy_cls
    permission = permission_cls(action_name)
    action_name = f"can_{action_name}"
    action_permissions = getattr(permission, action_name, [])
    action_can_auth = False
    action_can_any = False
    for perm in action_permissions:
        if type(perm) == AnyUser:
            action_can_any = True
            action_can_auth = True
        if type(perm) == AuthenticatedUser or type(perm) == SystemProcess:
            action_can_auth = True
    if user_is_auth:
        return action_can_auth or action_can_any
    else:
        return action_can_any


def response_code_ok(action_name, user_is_auth, response, authorized_response_code):
    action_allowed = is_action_allowed(action_name, user_is_auth)
    if action_allowed and response.status_code == authorized_response_code:
        return True
    elif not action_allowed and response.status_code == 403:
        return True
    return False


def test_read(client_with_credentials, sample_draft, search_clear, base_urls):
    non_existing = client_with_credentials.get(f"{base_urls['base_url']}yjuykyukyuk")
    assert non_existing.status_code == 404

    get_response = client_with_credentials.get(
        f"{base_urls['base_url']}{sample_draft['id']}/draft"
    )
    assert response_code_ok("read", True, get_response, 200)
    if is_action_allowed("read", True):
        assert get_response.json["metadata"] == sample_draft["metadata"]


def test_create(
    client_with_credentials, client, sample_metadata_list, app, search_clear, base_urls
):
    created_responses = []
    for sample_metadata_point in sample_metadata_list:
        created_responses.append(
            client_with_credentials.post(
                f"{base_urls['base_url']}", json=sample_metadata_point
            )
        )
        with app.test_client() as unauth_client:
            unauth_response = unauth_client.post(
                f"{base_urls['base_url']}", json=sample_metadata_point
            )
            assert response_code_ok("create", False, unauth_response, 201)
    assert all(
        [
            response_code_ok("create", True, new_response, 201)
            for new_response in created_responses
        ]
    )

    if is_action_allowed("create", True):
        for sample_metadata_point, created_response in zip(
            sample_metadata_list, created_responses
        ):
            created_response_reread = client_with_credentials.get(
                f"{base_urls['base_url']}{created_response.json['id']}/draft"
            )
            assert response_code_ok("read", True, created_response_reread, 200)
            assert (
                created_response_reread.json["metadata"]
                == sample_metadata_point["metadata"]
            )


"""
def test_create(
    client_with_credentials, client, sample_metadata_list, app, search_clear, base_urls
):
    created_responses = []
    for sample_metadata_point in sample_metadata_list:
        created_responses.append(
            client_with_credentials.post(f"{base_urls['base_url']}", json=sample_metadata_point)
        )
        with app.test_client() as unauth_client:
            unauth_response = unauth_client.post(
                f"{base_urls['base_url']}", json=sample_metadata_point
            )
            assert response_code_ok("create", False, unauth_response, 201)
    assert all([response_code_ok("create", True, new_response, 201) for new_response in created_responses])

    if is_action_allowed("create", True):
        for sample_metadata_point, created_response in zip(
            sample_metadata_list, created_responses
        ):
            created_response_reread = client_with_credentials.get(
                f"{base_urls['base_url']}{created_response.json['id']}"
            )
            assert response_code_ok("read", True, created_response_reread, 200)
            assert (
                created_response_reread.json["metadata"]
                == sample_metadata_point["metadata"]
            )
"""

"""
def test_listing( client_with_credentials, sample_records, search_clear, base_urls):
    listing_response = client_with_credentials.get(base_urls['base_url'])
    hits = listing_response.json["hits"]["hits"]
    assert len(hits) == 10
"""


def test_update(
    client_with_credentials, sample_draft, sample_metadata_list, search_clear, base_urls
):
    non_existing = client_with_credentials.put(
        f"{base_urls['base_url']}yjuykyukyuk/draft", json=sample_metadata_list[5]
    )

    old_record_read_response_json = client_with_credentials.get(
        f"{base_urls['base_url']}{ sample_draft['id']}/draft"
    ).json

    update_response = client_with_credentials.put(
        f"{base_urls['base_url']}{ sample_draft['id']}/draft",
        json=sample_metadata_list[2],
    )

    updated_record_read_response = client_with_credentials.get(
        f"{base_urls['base_url']}{ sample_draft['id']}/draft"
    )

    assert response_code_ok("read", True, updated_record_read_response, 200)
    assert response_code_ok("update", True, non_existing, 404)
    assert response_code_ok("update", True, update_response, 200)
    if is_action_allowed("update", True):
        assert old_record_read_response_json["metadata"] == sample_draft.metadata
        assert (
            update_response.json["metadata"]
            == sample_metadata_list[2]["metadata"]
            != old_record_read_response_json["metadata"]
        )
        assert (
            updated_record_read_response.json["metadata"]
            == sample_metadata_list[2]["metadata"]
        )
        assert (
            updated_record_read_response.json["revision_id"]
            == old_record_read_response_json["revision_id"] + 1
        )

    # test patch - 405 METHOD NOT ALLOWED
    # to make it work change create_url_rules in resource and allow jsonpatch in request_body_parsers in resource config
    # patch_response = client_with_credentials.patch(f"{base_urls['base_url']}{sample_record['id']}",
    #                                                              json={"path": "/metadata/title",
    #                                                              "op": "replace",
    #                                                              "value": "UPDATED!"})


def test_delete(client_with_credentials, sample_draft, app, search_clear, base_urls):
    non_existing = client_with_credentials.delete(f"{base_urls['base_url']}yjuykyukyuk")
    assert response_code_ok("delete", True, non_existing, 404)

    delete_response = client_with_credentials.delete(
        f"{base_urls['base_url']}{ sample_draft['id']}/draft"
    )
    assert response_code_ok("delete", True, delete_response, 204)

    if is_action_allowed("delete", True):
        deleted_get_response = client_with_credentials.delete(
            f"{base_urls['base_url']}{ sample_draft['id']}/draft"
        )
        assert deleted_get_response.status_code == 404


"""
def test_delete_unauth(sample_record, search_clear, app, base_urls):
    with app.test_client() as unauth_client:
        unauth_delete_response = unauth_client.delete(
            f"{base_urls['base_url']}{sample_record['id']}"
        )
        assert response_code_ok("delete", False, unauth_delete_response, 204)
"""


def assert_expected_links(
    pid_value, generated_links, base_urls, site_hostname="127.0.0.1:5000"
):
    """Compare generated links to expected links."""
    required_links = {
        "draft": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}/draft",
        "latest": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}/versions/latest",
        "latest_html": (
            f"https://{site_hostname}{base_urls['base_html_url']}{pid_value}/latest"
        ),
        "publish": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}/draft/actions/publish",
        "record": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}",
        "self": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}/draft",
        "self_html": (
            f"https://{site_hostname}{base_urls['base_html_url']}{pid_value}/edit"
        ),
        "versions": (
            f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}/versions"
        ),
    }
    assert required_links.items() <= generated_links.items()


def test_create_links(app, client_with_credentials, input_data, base_urls):
    res = client_with_credentials.post(base_urls["base_url"], json=input_data)

    pid_value = res.json["id"]
    assert_expected_links(pid_value, res.json["links"], base_urls)


def test_read_links(app, client_with_credentials, sample_draft, base_urls):
    pid_value = sample_draft["id"]
    res = client_with_credentials.get(f"{base_urls['base_url']}{pid_value}/draft")

    assert_expected_links(pid_value, res.json["links"], base_urls)


def test_update_links(
    app, client_with_credentials, sample_draft, sample_metadata_list, base_urls
):
    pid_value = sample_draft["id"]
    res = client_with_credentials.get(f"{base_urls['base_url']}{pid_value}/draft")
    res = client_with_credentials.put(
        f"{base_urls['base_url']}{pid_value}/draft", json=sample_metadata_list[1]
    )

    assert res.status_code == 200
    assert_expected_links(pid_value, res.json["links"], base_urls)


@pytest.fixture(scope="module")
def app_config(app_config):
    app_config["HAS_DRAFT"] = [BooleanCF("has_draft")]
    return app_config


def _assert_single_item_response(response):
    """Assert the fields present on a single item response."""
    response_fields = response.json.keys()
    fields_to_check = ["id", "metadata", "created", "updated", "links"]

    for field in fields_to_check:
        assert field in response_fields


#
# Operations tests
#


def _create_and_publish(client_with_credentials, input_data):
    """Create a draft and publish it."""
    # Create the draft
    response = client_with_credentials.post(
        NrDocumentsResourceConfig.url_prefix, json=input_data
    )

    assert response.status_code == 201

    recid = response.json["id"]

    # Publish it
    response = client_with_credentials.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft/actions/publish"
    )

    assert response.status_code == 202
    _assert_single_item_response(response)
    return recid


def test_publish_draft(client_with_credentials, input_data, search_clear):
    """Test draft publication of a non-existing record.

    It has to first create said draft.
    """
    recid = _create_and_publish(client_with_credentials, input_data)

    # Check draft does not exists anymore
    response = client_with_credentials.get(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft"
    )

    assert response.status_code == 404

    # Check record exists
    response = client_with_credentials.get(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}"
    )

    assert response.status_code == 200

    _assert_single_item_response(response)


def test_search_versions(
    client_with_credentials, input_data, search_clear, sample_published_record
):
    """Test search for versions."""
    recid = sample_published_record["id"]
    NrDocumentsDraft.index.refresh()

    # Check draft does not exists anymore
    res = client_with_credentials.get(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/versions"
    )
    assert res.status_code == 200


#
# Flow tests (Note that operations are tested above
# therefore these tests do not assert their output)
#


def test_create_publish_new_revision(
    client_with_credentials,
    input_data,
    search_clear,
    sample_metadata_list,
    sample_published_record,
):
    """Test draft creation of an existing record and publish it."""
    recid = sample_published_record["id"]

    # Create new draft of said record

    edited_input_data = copy.deepcopy(input_data)
    edited_input_data["metadata"] = sample_metadata_list[1]["metadata"]
    edited_metadata = edited_input_data["metadata"]
    orig_metadata = input_data["metadata"]

    response = client_with_credentials.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft"
    )

    assert response.status_code == 201
    assert response.json["revision_id"] == 5
    _assert_single_item_response(response)

    # Update that new draft
    response = client_with_credentials.put(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft", json=edited_input_data
    )

    assert response.status_code == 200

    # Check the actual record was not modified
    response = client_with_credentials.get(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}"
    )

    assert response.status_code == 200
    _assert_single_item_response(response)
    assert response.json["metadata"] == orig_metadata

    # Publish it to check the increment in reversion
    response = client_with_credentials.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft/actions/publish"
    )

    assert response.status_code == 202
    _assert_single_item_response(response)

    assert response.json["id"] == recid
    assert response.json["revision_id"] == 2
    assert response.json["metadata"] == edited_metadata

    # Check it was actually edited
    response = client_with_credentials.get(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}"
    )

    assert response.json["metadata"] == edited_metadata


def test_mutiple_edit(
    client_with_credentials, input_data, search_clear, sample_published_record
):
    """Test the revision_id when editing record multiple times.

    This tests the `edit` service method.
    """
    recid = sample_published_record["id"]

    # Create new draft of said record
    response = client_with_credentials.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft"
    )

    assert response.status_code == 201
    assert response.json["revision_id"] == 5

    # Request a second edit. Get the same draft (revision_id)
    response = client_with_credentials.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft"
    )

    assert response.status_code == 201
    assert response.json["revision_id"] == 5

    # Publish it to check the increment in version_id
    response = client_with_credentials.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft/actions/publish"
    )

    assert response.status_code == 202

    # Edit again
    response = client_with_credentials.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft"
    )

    assert response.status_code == 201
    assert response.json["revision_id"] == 8


def test_redirect_to_latest_version(
    client_with_credentials, input_data, search_clear, sample_published_record
):
    """Creates a new version of a record.

    Publishes the draft to obtain 2 versions of a record.
    """
    recid = sample_published_record["id"]

    # Create new version of said record
    response = client_with_credentials.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/versions"
    )
    recid_2 = response.json["id"]

    # NOTE: Assuming a new version should indeed have its files.enabled set to
    #       True automatically, we have to reset it to False for this test.
    client_with_credentials.put(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid_2}/draft", json=input_data
    )

    # Publish it to check the increment in version
    response = client_with_credentials.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid_2}/draft/actions/publish"
    )
    latest_version_self_link = response.json["links"]["self"]

    # Read a previous versions latest
    response = client_with_credentials.get(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/versions/latest"
    )

    assert response.status_code == 301
    assert response.headers["location"] == latest_version_self_link


def test_list_drafts(client_with_credentials, input_data, vocab_cf, search_clear):
    assert (
        len(
            client_with_credentials.get(NrDocumentsResourceConfig.url_prefix).json[
                "hits"
            ]["hits"]
        )
        == 0
    )
    assert (
        len(
            client_with_credentials.get(
                f"user{ NrDocumentsResourceConfig.url_prefix}"
            ).json["hits"]["hits"]
        )
        == 0
    )

    create_draft_response = client_with_credentials.post(
        ThesisResourceConfig.url_prefix, json=input_data
    )
    assert create_draft_response.status_code == 201
    recid = create_draft_response.json["id"]

    NrDocumentsDraft.index.refresh()
    NrDocumentsRecord.index.refresh()
    assert (
        len(
            client_with_credentials.get(NrDocumentsResourceConfig.url_prefix).json[
                "hits"
            ]["hits"]
        )
        == 0
    )
    assert (
        len(
            client_with_credentials.get(
                f"user{ NrDocumentsResourceConfig.url_prefix}"
            ).json["hits"]["hits"]
        )
        == 1
    )

    response_publish = client_with_credentials.post(
        f"{ThesisResourceConfig.url_prefix}{recid}/draft/actions/publish"
    )
    assert response_publish.status_code == 202

    NrDocumentsDraft.index.refresh()
    NrDocumentsRecord.index.refresh()
    assert (
        len(
            client_with_credentials.get(NrDocumentsResourceConfig.url_prefix).json[
                "hits"
            ]["hits"]
        )
        == 1
    )
    assert (
        len(
            client_with_credentials.get(
                f"user{ NrDocumentsResourceConfig.url_prefix}"
            ).json["hits"]["hits"]
        )
        == 0
    )


def assert_expected_links_record(
    pid_value, links, base_urls, site_hostname="127.0.0.1:5000"
):
    """Compare generated links to expected links."""
    expected_links = {
        "draft": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}/draft",
        "latest": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}/versions/latest",
        "latest_html": (
            f"https://{site_hostname}{base_urls['base_html_url']}{pid_value}/latest"
        ),
        "publish": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}/draft/actions/publish",
        "record": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}",
        "self": f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}",
        "self_html": f"https://{site_hostname}{base_urls['base_html_url']}{pid_value}",
        "versions": (
            f"https://{site_hostname}/api{base_urls['base_url']}{pid_value}/versions"
        ),
    }
    assert expected_links.items() <= links.items()


def test_read_links_record(
    app, client_with_credentials, input_data, base_urls, sample_published_record
):
    pid_value = sample_published_record["id"]
    res = client_with_credentials.get(f"{base_urls['base_url']}{pid_value}")

    assert_expected_links_record(pid_value, res.json["links"], base_urls)

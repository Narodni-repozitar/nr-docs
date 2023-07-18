import copy
import datetime

from invenio_records.dictutils import dict_lookup
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    SystemProcess,
)

from nr_documents.proxies import current_service
from nr_documents.records.api import NrDocumentsDraft
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


def _assert_single_item_response(response):
    """Assert the fields present on a single item response."""
    response_fields = response.json.keys()
    fields_to_check = ["id", "metadata", "created", "updated", "links"]

    for field in fields_to_check:
        assert field in response_fields


#
# Operations tests
#


def _create_and_publish(client, input_data):
    """Create a draft and publish it."""
    # Create the draft
    response = client.post(NrDocumentsResourceConfig.url_prefix, json=input_data)

    assert response.status_code == 201

    recid = response.json["id"]

    # Publish it
    response = client.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft/actions/publish"
    )

    assert response.status_code == 202
    _assert_single_item_response(response)
    return recid


def test_publish_draft(client, input_data, search_clear):
    """Test draft publication of a non-existing record.

    It has to first create said draft.
    """
    recid = _create_and_publish(client, input_data)

    # Check draft does not exists anymore
    response = client.get(f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft")

    assert response.status_code == 404

    # Check record exists
    response = client.get(f"{ NrDocumentsResourceConfig.url_prefix}{recid}")

    assert response.status_code == 200

    _assert_single_item_response(response)


def test_search_versions(client, input_data, search_clear):
    """Test search for versions."""
    recid = _create_and_publish(client, input_data)
    NrDocumentsDraft.index.refresh()

    # Check draft does not exists anymore
    res = client.get(f"{ NrDocumentsResourceConfig.url_prefix}{recid}/versions")
    assert res.status_code == 200


#
# Flow tests (Note that operations are tested above
# therefore these tests do not assert their output)
#


def test_create_publish_new_revision(
    client, input_data, search_clear, sample_metadata_list
):
    """Test draft creation of an existing record and publish it."""
    recid = _create_and_publish(client, input_data)

    # Create new draft of said record

    edited_input_data = copy.deepcopy(input_data)
    edited_input_data["metadata"] = sample_metadata_list[1]["metadata"]
    edited_metadata = edited_input_data["metadata"]
    orig_metadata = input_data["metadata"]

    response = client.post(f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft")

    assert response.status_code == 201
    assert response.json["revision_id"] == 5
    _assert_single_item_response(response)

    # Update that new draft
    response = client.put(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft", json=edited_input_data
    )

    assert response.status_code == 200

    # Check the actual record was not modified
    response = client.get(f"{ NrDocumentsResourceConfig.url_prefix}{recid}")

    assert response.status_code == 200
    _assert_single_item_response(response)
    assert response.json["metadata"] == orig_metadata

    # Publish it to check the increment in reversion
    response = client.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft/actions/publish"
    )

    assert response.status_code == 202
    _assert_single_item_response(response)

    assert response.json["id"] == recid
    assert response.json["revision_id"] == 2
    assert response.json["metadata"] == edited_metadata

    # Check it was actually edited
    response = client.get(f"{ NrDocumentsResourceConfig.url_prefix}{recid}")

    assert response.json["metadata"] == edited_metadata


def test_mutiple_edit(client, input_data, search_clear):
    """Test the revision_id when editing record multiple times.

    This tests the `edit` service method.
    """
    recid = _create_and_publish(client, input_data)

    # Create new draft of said record
    response = client.post(f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft")

    assert response.status_code == 201
    assert response.json["revision_id"] == 5

    # Request a second edit. Get the same draft (revision_id)
    response = client.post(f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft")

    assert response.status_code == 201
    assert response.json["revision_id"] == 5

    # Publish it to check the increment in version_id
    response = client.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft/actions/publish"
    )

    assert response.status_code == 202

    # Edit again
    response = client.post(f"{ NrDocumentsResourceConfig.url_prefix}{recid}/draft")

    assert response.status_code == 201
    assert response.json["revision_id"] == 8


def test_redirect_to_latest_version(client, input_data):
    """Creates a new version of a record.

    Publishes the draft to obtain 2 versions of a record.
    """
    recid = _create_and_publish(client, input_data)

    # Create new version of said record
    response = client.post(f"{ NrDocumentsResourceConfig.url_prefix}{recid}/versions")
    recid_2 = response.json["id"]

    # NOTE: Assuming a new version should indeed have its files.enabled set to
    #       True automatically, we have to reset it to False for this test.
    client.put(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid_2}/draft", json=input_data
    )

    # Publish it to check the increment in version
    response = client.post(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid_2}/draft/actions/publish"
    )
    latest_version_self_link = response.json["links"]["self"]

    # Read a previous versions latest
    response = client.get(
        f"{ NrDocumentsResourceConfig.url_prefix}{recid}/versions/latest"
    )

    assert response.status_code == 301
    assert response.headers["location"] == latest_version_self_link


BASE_URL = f"http://localhost{ NrDocumentsResourceConfig.url_prefix}"
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


def test_get_item(client_with_credentials, sample_record, search_clear):
    non_existing = client_with_credentials.get(f"{BASE_URL}yjuykyukyuk")
    assert non_existing.status_code == 404

    get_response = client_with_credentials.get(f"{BASE_URL}{sample_record['id']}")
    assert response_code_ok("read", True, get_response, 200)
    if is_action_allowed("read", True):
        assert get_response.json["metadata"] == sample_record["metadata"]


def test_create(
    client_with_credentials, client, sample_metadata_list, app, search_clear
):
    created_responses = []
    for sample_metadata_point in sample_metadata_list:
        created_responses.append(
            client_with_credentials.post(f"{BASE_URL}", json=sample_metadata_point)
        )
        with app.test_client() as unauth_client:
            unauth_response = unauth_client.post(
                f"{BASE_URL}", json=sample_metadata_point
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
                f"{BASE_URL}{created_response.json['id']}"
            )
            assert response_code_ok("read", True, created_response_reread, 200)
            assert (
                created_response_reread.json["metadata"]
                == sample_metadata_point["metadata"]
            )


def test_listing(client_with_credentials, sample_records, search_clear):
    listing_response = client_with_credentials.get(BASE_URL)
    hits = listing_response.json["hits"]["hits"]
    assert len(hits) == 25


def test_update(
    client_with_credentials, sample_record, sample_metadata_list, search_clear
):
    non_existing = client_with_credentials.put(
        f"{BASE_URL}yjuykyukyuk", json=sample_metadata_list[15]
    )

    old_record_read_response_json = client_with_credentials.get(
        f"{BASE_URL}{sample_record['id']}"
    ).json

    update_response = client_with_credentials.put(
        f"{BASE_URL}{sample_record['id']}", json=sample_metadata_list[2]
    )

    updated_record_read_response = client_with_credentials.get(
        f"{BASE_URL}{sample_record['id']}"
    )

    assert response_code_ok("read", True, updated_record_read_response, 200)
    assert response_code_ok("update", True, non_existing, 404)
    assert response_code_ok("update", True, update_response, 200)
    if is_action_allowed("update", True):
        assert old_record_read_response_json["metadata"] == sample_record.metadata
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
    # patch_response = client_with_credentials.patch(f"{BASE_URL}{sample_record['id']}",
    #                                                              json={"path": "/metadata/title",
    #                                                              "op": "replace",
    #                                                              "value": "UPDATED!"})


def test_delete(client_with_credentials, sample_record, app, search_clear):
    non_existing = client_with_credentials.delete(f"{BASE_URL}yjuykyukyuk")
    assert response_code_ok("delete", True, non_existing, 404)

    read_response = client_with_credentials.get(f"{BASE_URL}{sample_record['id']}")
    assert response_code_ok("read", True, read_response, 200)

    delete_response = client_with_credentials.delete(f"{BASE_URL}{sample_record['id']}")
    assert response_code_ok("delete", True, delete_response, 204)

    if is_action_allowed("delete", True):
        deleted_get_response = client_with_credentials.delete(
            f"{BASE_URL}{sample_record['id']}"
        )
        assert deleted_get_response.status_code == 410


def test_delete_unauth(sample_record, search_clear, app):
    with app.test_client() as unauth_client:
        unauth_delete_response = unauth_client.delete(
            f"{BASE_URL}{sample_record['id']}"
        )
        assert response_code_ok("delete", False, unauth_delete_response, 204)


def test_search(
    client_with_credentials, sample_records, sample_metadata_list, search_clear
):
    if is_action_allowed("search", True):
        paths = get_paths("metadata", sample_metadata_list[0]["metadata"])

        for record in sample_records:
            for path in paths:
                field_value = dict_lookup(record, path)
                path_search_results = client_with_credentials.get(
                    f'{BASE_URL}?q={path}:"{field_value}"'
                ).json["hits"]["hits"]
                assert len(path_search_results) > 0
                for field_result in [
                    dict_lookup(res, path) for res in path_search_results
                ]:
                    if field_result == field_value:
                        break
                else:
                    raise AssertionError(
                        "Queried field value not found in search results."
                    )

        res_fail = client_with_credentials.get(f"{BASE_URL}?q=wefrtghthy")
        res_created = client_with_credentials.get(
            f"{BASE_URL}?q={str(datetime.datetime.now().date())}"
        )
        res_created_fail = client_with_credentials.get(f"{BASE_URL}?q=2022-10-16")
        res_facets = client_with_credentials.get(
            f"{BASE_URL}?created={sample_records[0].created.isoformat()}"
        )

        assert len(res_fail.json["hits"]["hits"]) == 0
        assert len(res_created.json["hits"]["hits"]) == 25
        assert len(res_created_fail.json["hits"]["hits"]) == 0
        assert len(res_facets.json["hits"]["hits"]) == 1


def test_read(client_with_credentials, sample_draft, search_clear):
    non_existing = client_with_credentials.get(f"{BASE_URL}yjuykyukyuk")
    assert non_existing.status_code == 404

    get_response = client_with_credentials.get(f"{BASE_URL}{sample_draft['id']}/draft")
    assert response_code_ok("read", True, get_response, 200)
    if is_action_allowed("read", True):
        assert get_response.json["metadata"] == sample_draft["metadata"]


"""
def test_create(
    client_with_credentials, client, sample_metadata_list, app, search_clear
):
    created_responses = []
    for sample_metadata_point in sample_metadata_list:
        created_responses.append(
            client_with_credentials.post(f"{BASE_URL}", json=sample_metadata_point)
        )
        with app.test_client() as unauth_client:
            unauth_response = unauth_client.post(
                f"{BASE_URL}", json=sample_metadata_point
            )
            assert response_code_ok("create", False, unauth_response, 201)
    assert all([response_code_ok("create", True, new_response, 201) for new_response in created_responses])

    if is_action_allowed("create", True):
        for sample_metadata_point, created_response in zip(
            sample_metadata_list, created_responses
        ):
            created_response_reread = client_with_credentials.get(
                f"{BASE_URL}{created_response.json['id']}"
            )
            assert response_code_ok("read", True, created_response_reread, 200)
            assert (
                created_response_reread.json["metadata"]
                == sample_metadata_point["metadata"]
            )
"""

"""
def test_listing( client_with_credentials, sample_records, search_clear):
    listing_response = client_with_credentials.get(BASE_URL)
    hits = listing_response.json["hits"]["hits"]
    assert len(hits) == 10
"""

"""
def test_delete_unauth(sample_record, search_clear, app):
    with app.test_client() as unauth_client:
        unauth_delete_response = unauth_client.delete(
            f"{BASE_URL}{sample_record['id']}"
        )
        assert response_code_ok("delete", False, unauth_delete_response, 204)
"""

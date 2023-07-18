import datetime

from invenio_records.dictutils import dict_lookup
from invenio_records_permissions.generators import (
    AnyUser,
    AuthenticatedUser,
    SystemProcess,
)

from nr_documents.proxies import current_service
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

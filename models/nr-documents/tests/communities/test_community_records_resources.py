import pytest
from invenio_access.permissions import system_identity

from nr_documents.proxies import (
    current_community_records_service,
    current_record_communities_service,
)


@pytest.fixture
def community_records_service():
    """Get the current community records service."""
    return current_community_records_service


@pytest.fixture
def record_communities_service():
    return current_record_communities_service


@pytest.fixture
def create_record_with_community(get_or_create_community):
    def _create_record_with_community(
        record_communities_service, community_dict, identity, sample_published_record
    ):
        comm = get_or_create_community(community_dict, identity)
        record_communities_service.add_to_published_record(
            identity,
            sample_published_record["id"],
            data={"communities": [{"id": comm.slug}]},
        )
        return sample_published_record

    return _create_record_with_community


def test_list(
    record_communities_service,
    client,
    minimal_community,
    sample_published_record,
    create_record_with_community,
    base_urls,
    search_clear,
):
    create_record_with_community(
        record_communities_service,
        minimal_community,
        system_identity,
        sample_published_record,
    )
    response = client.get(
        f"{base_urls['base_community_records_url']}{minimal_community['slug']}/records",
    )
    assert len(response.json["hits"]["hits"]) == 1


def test_remove_community(
    record_communities_service,
    client,
    minimal_community,
    sample_published_record,
    create_record_with_community,
    base_urls,
    search_clear,
):
    create_record_with_community(
        record_communities_service,
        minimal_community,
        system_identity,
        sample_published_record,
    )
    res_before = client.get(
        f"{base_urls['base_community_records_url']}{minimal_community['slug']}/records",
    )
    data = {"records": [{"id": sample_published_record["id"]}]}
    assert len(res_before.json["hits"]["hits"]) == 1
    res_del = client.delete(
        f"{base_urls['base_community_records_url']}{minimal_community['slug']}/records",
        json=data,
    )
    # todo the code perhaps?
    res_after = client.get(
        f"{base_urls['base_community_records_url']}{minimal_community['slug']}/records",
    )
    assert len(res_after.json["hits"]["hits"]) == 0


"""
def test_permission_denied(
    client, uploader, test_user, record_community, headers, community, search_clear
):
    record = record_community.create_record()
    data = {"records": [{"id": record.pid.pid_value}]}

    test_user_client = test_user.login(client)

    response_403 = test_user_client.delete(
        f"{base_urls['base_community_records_url']}{community.id}/records",
        headers=headers,
        json=data,
    )
    assert response_403.status_code == 403
"""


def test_error_data(
    record_communities_service,
    client,
    minimal_community,
    sample_published_record,
    create_record_with_community,
    base_urls,
    search_clear,
):
    create_record_with_community(
        record_communities_service,
        minimal_community,
        system_identity,
        sample_published_record,
    )
    res_before = client.get(
        f"{base_urls['base_community_records_url']}{minimal_community['slug']}/records",
    )
    data = {"records": [{"id": "wrong-id"}]}
    assert len(res_before.json["hits"]["hits"]) == 1
    res_del = client.delete(
        f"{base_urls['base_community_records_url']}{minimal_community['slug']}/records",
        json=data,
    )
    assert res_del.status_code == 200
    assert res_del.json["errors"]


def test_removal_of_multiple_communities_success(
    record_communities_service,
    client,
    minimal_community,
    published_record_factory,
    input_data,
    create_record_with_community,
    base_urls,
    search_clear,
):
    """Remove multiple records from a community."""
    record1 = create_record_with_community(
        record_communities_service,
        minimal_community,
        system_identity,
        published_record_factory(input_data),
    )
    record2 = create_record_with_community(
        record_communities_service,
        minimal_community,
        system_identity,
        published_record_factory(input_data),
    )
    record3 = create_record_with_community(
        record_communities_service,
        minimal_community,
        system_identity,
        published_record_factory(input_data),
    )
    response = client.get(
        f"{base_urls['base_community_records_url']}{minimal_community['slug']}/records",
    )
    assert len(response.json["hits"]["hits"]) == 3
    data = {
        "records": [
            {"id": record1["id"]},
            {"id": record2["id"]},
            {"id": record3["id"]},
        ]
    }

    response = client.delete(
        f"{base_urls['base_community_records_url']}{minimal_community['slug']}/records",
        json=data,
    )
    assert response.status_code == 200
    assert not response.json.get("errors")
    response = client.get(
        f"{base_urls['base_community_records_url']}{minimal_community['slug']}/records",
    )
    assert len(response.json["hits"]["hits"]) == 0
    print()


"""
def test_exceeded_max_number_of_records(
    client, curator, record_community, headers, community, service
):
    client = curator.login(client)
    random_record = {"id": "random-id"}
    lots_of_records = []
    while len(lots_of_records) <= service.config.max_number_of_removals:
        lots_of_records.append(random_record)

    data = {"records": lots_of_records}
    response = client.delete(
        f"/communities/{community.id}/records",
        headers=headers,
        json=data,
    )
    assert response.status_code == 400
"""

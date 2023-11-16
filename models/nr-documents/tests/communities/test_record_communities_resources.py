from nr_documents.resources.record_communities.config import (
    NrDocumentsRecordCommunitiesResourceConfig,
)

RECORD_COMMUNITIES_BASE_URL = NrDocumentsRecordCommunitiesResourceConfig.url_prefix


def _recid_with_community(
    client_with_credentials,
    minimal_community,
    community_owner,
    sample_published_record,
    get_or_create_community,
):
    recid = sample_published_record["id"]
    community = get_or_create_community(minimal_community, community_owner.identity)
    response = client_with_credentials.get(
        f"{RECORD_COMMUNITIES_BASE_URL}{recid}/communities"
    )
    add = client_with_credentials.post(
        f"{RECORD_COMMUNITIES_BASE_URL}{recid}/communities",
        json={
            "communities": [
                {"id": minimal_community["slug"]},  # test with slug
            ]
        },
    )
    return recid


def test_add(
    client_with_credentials,
    minimal_community,
    community_owner,
    sample_published_record,
    get_or_create_community,
):
    recid = _recid_with_community(
        client_with_credentials,
        minimal_community,
        community_owner,
        sample_published_record,
        get_or_create_community,
    )
    response = client_with_credentials.get(
        f"{RECORD_COMMUNITIES_BASE_URL}{recid}/communities"
    )
    assert len(response.json["hits"]["hits"]) == 1
    assert response.json["hits"]["hits"][0]["slug"] == "public"


def test_remove(
    client_with_credentials,
    minimal_community,
    community_owner,
    search_clear,
    sample_published_record,
    get_or_create_community,
):
    recid = _recid_with_community(
        client_with_credentials,
        minimal_community,
        community_owner,
        sample_published_record,
        get_or_create_community,
    )
    id = client_with_credentials.get(
        f"{RECORD_COMMUNITIES_BASE_URL}{recid}/communities"
    ).json["hits"]["hits"][0]["id"]
    remove = client_with_credentials.delete(
        f"{RECORD_COMMUNITIES_BASE_URL}{recid}/communities",
        json={
            "communities": [
                {"id": id},  # test with slug
            ]
        },
    )
    assert (
        len(
            client_with_credentials.get(
                f"{RECORD_COMMUNITIES_BASE_URL}{recid}/communities"
            ).json["hits"]["hits"]
        )
        == 0
    )

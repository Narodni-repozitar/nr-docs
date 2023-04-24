from nr_documents.records.api import NrDocumentsDraft


def _assert_single_item_response(response):
    """Assert the fields present on a single item response."""
    response_fields = response.json.keys()
    fields_to_check = ["id", "metadata", "created", "updated", "links"]

    for field in fields_to_check:
        assert field in response_fields


#
# Operations tests
#


def test_create_draft(client, input_data, search_clear):
    """Test draft creation of a non-existing record."""
    response = client.post("/nr-documents/", json=input_data)

    assert response.status_code == 201
    _assert_single_item_response(response)


def test_read_draft(client, input_data, search_clear):
    response = client.post("/nr-documents/", json=input_data)

    assert response.status_code == 201

    recid = response.json["id"]
    response = client.get(f"/nr-documents/{recid}/draft")

    assert response.status_code == 200

    _assert_single_item_response(response)


def test_update_draft(client, input_data, search_clear, sample_metadata_list):
    response = client.post("/nr-documents/", json=input_data)

    assert response.status_code == 201
    assert response.json["metadata"] == input_data["metadata"]

    recid = response.json["id"]

    orig = input_data["metadata"]
    edited_input_data = sample_metadata_list[1]

    # Update draft content
    update_response = client.put(f"/nr-documents/{recid}/draft", json=edited_input_data)

    assert update_response.status_code == 200
    assert update_response.json["metadata"] == edited_input_data["metadata"]
    assert update_response.json["id"] == recid

    # Check the updates where saved
    update_response = client.get(f"/nr-documents/{recid}/draft")

    assert update_response.status_code == 200
    assert update_response.json["metadata"] == edited_input_data["metadata"]
    assert update_response.json["id"] == recid


def test_delete_draft(client, input_data, search_clear):
    response = client.post("/nr-documents/", json=input_data)

    assert response.status_code == 201

    recid = response.json["id"]

    update_response = client.delete(f"/nr-documents/{recid}/draft")

    assert update_response.status_code == 204

    # Check draft deletion
    update_response = client.get(f"/nr-documents/{recid}/draft")
    assert update_response.status_code == 404


def _create_and_publish(client, input_data):
    """Create a draft and publish it."""
    # Create the draft
    response = client.post("/nr-documents/", json=input_data)

    assert response.status_code == 201

    recid = response.json["id"]

    # Publish it
    response = client.post(f"/nr-documents/{recid}/draft/actions/publish")

    assert response.status_code == 202
    _assert_single_item_response(response)
    return recid


def test_publish_draft(client, input_data, search_clear):
    """Test draft publication of a non-existing record.

    It has to first create said draft.
    """
    recid = _create_and_publish(client, input_data)

    # Check draft does not exists anymore
    response = client.get(f"/nr-documents/{recid}/draft")

    assert response.status_code == 404

    # Check record exists
    response = client.get(f"/nr-documents/{recid}")

    assert response.status_code == 200

    _assert_single_item_response(response)


def test_search_versions(client, input_data, search_clear):
    """Test search for versions."""
    recid = _create_and_publish(client, input_data)
    NrDocumentsDraft.index.refresh()

    # Check draft does not exists anymore
    res = client.get(f"/nr-documents/{recid}/versions")
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

    edited_input_data = sample_metadata_list[1]
    edited_metadata = edited_input_data["metadata"]
    orig_metadata = input_data["metadata"]

    response = client.post(f"/nr-documents/{recid}/draft")

    assert response.status_code == 201
    assert response.json["revision_id"] == 5
    _assert_single_item_response(response)

    # Update that new draft
    response = client.put(f"/nr-documents/{recid}/draft", json=edited_input_data)

    assert response.status_code == 200

    # Check the actual record was not modified
    response = client.get(f"/nr-documents/{recid}")

    assert response.status_code == 200
    _assert_single_item_response(response)
    assert response.json["metadata"] == orig_metadata

    # Publish it to check the increment in reversion
    response = client.post(f"/nr-documents/{recid}/draft/actions/publish")

    assert response.status_code == 202
    _assert_single_item_response(response)

    assert response.json["id"] == recid
    assert response.json["revision_id"] == 2
    assert response.json["metadata"] == edited_metadata

    # Check it was actually edited
    response = client.get(f"/nr-documents/{recid}")

    assert response.json["metadata"] == edited_metadata


def test_mutiple_edit(client, input_data, search_clear):
    """Test the revision_id when editing record multiple times.

    This tests the `edit` service method.
    """
    recid = _create_and_publish(client, input_data)

    # Create new draft of said record
    response = client.post(f"/nr-documents/{recid}/draft")

    assert response.status_code == 201
    assert response.json["revision_id"] == 5

    # Request a second edit. Get the same draft (revision_id)
    response = client.post(f"/nr-documents/{recid}/draft")

    assert response.status_code == 201
    assert response.json["revision_id"] == 5

    # Publish it to check the increment in version_id
    response = client.post(f"/nr-documents/{recid}/draft/actions/publish")

    assert response.status_code == 202

    # Edit again
    response = client.post(f"/nr-documents/{recid}/draft")

    assert response.status_code == 201
    assert response.json["revision_id"] == 8


def test_redirect_to_latest_version(client, input_data):
    """Creates a new version of a record.

    Publishes the draft to obtain 2 versions of a record.
    """
    recid = _create_and_publish(client, input_data)

    # Create new version of said record
    response = client.post(f"/nr-documents/{recid}/versions")
    recid_2 = response.json["id"]

    # NOTE: Assuming a new version should indeed have its files.enabled set to
    #       True automatically, we have to reset it to False for this test.
    client.put(f"/nr-documents/{recid_2}/draft", json=input_data)

    # Publish it to check the increment in version
    response = client.post(f"/nr-documents/{recid_2}/draft/actions/publish")
    latest_version_self_link = response.json["links"]["self"]

    # Read a previous versions latest
    response = client.get(f"/nr-documents/{recid}/versions/latest")

    assert response.status_code == 301
    assert response.headers["location"] == latest_version_self_link

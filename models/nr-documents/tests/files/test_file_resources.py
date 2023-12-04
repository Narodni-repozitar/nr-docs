from io import BytesIO

import pytest



def test_files_api_flow(
    client_with_credentials, search_clear, headers, input_data, base_urls
):
    """Test record creation."""
    base_files_url = base_urls["base_draft_files_url"]
    res = client_with_credentials.post(
        base_urls["base_url"], headers=headers, json=input_data
    )
    assert res.status_code == 201
    id_ = res.json["id"]

    # Initialize files upload
    res = client_with_credentials.post(
        f"{base_files_url.replace('{id}', id_)}/files",
        headers=headers,
        json=[
            {"key": "test.pdf", "title": "Test file"},
        ],
    )
    assert res.status_code == 201
    res_file = res.json["entries"][0]
    assert res_file["key"] == "test.pdf"
    assert res_file["status"] == "pending"
    assert res_file["metadata"] == {"title": "Test file"}

    # Get the file metadata
    res = client_with_credentials.get(
        f"{base_files_url.replace('{id}', id_)}/files/test.pdf", headers=headers
    )
    assert res.status_code == 200
    assert res.json["key"] == "test.pdf"
    assert res.json["status"] == "pending"
    assert res.json["metadata"] == {"title": "Test file"}

    # Upload a file
    res = client_with_credentials.put(
        f"{base_files_url.replace('{id}', id_)}/files/test.pdf/content",
        headers={
            "content-type": "application/octet-stream",
            "accept": "application/json",
        },
        data=BytesIO(b"testfile"),
    )
    assert res.status_code == 200
    assert res.json["status"] == "pending"

    # Commit the uploaded file
    res = client_with_credentials.post(
        f"{base_files_url.replace('{id}', id_)}/files/test.pdf/commit", headers=headers
    )
    assert res.status_code == 200
    assert res.json["status"] == "completed"

    # Get the file metadata
    res = client_with_credentials.get(
        f"{base_files_url.replace('{id}', id_)}/files/test.pdf", headers=headers
    )
    assert res.status_code == 200
    assert res.json["key"] == "test.pdf"
    assert res.json["status"] == "completed"
    assert res.json["metadata"] == {"title": "Test file"}
    file_size = str(res.json["size"])
    assert isinstance(res.json["size"], int), "File size not integer"

    # Read a file's content
    res = client_with_credentials.get(
        f"{base_files_url.replace('{id}', id_)}/files/test.pdf/content", headers=headers
    )
    assert res.status_code == 200
    assert res.data == b"testfile"

    # Update file metadata
    res = client_with_credentials.put(
        f"{base_files_url.replace('{id}', id_)}/files/test.pdf",
        headers=headers,
        json={"title": "New title"},
    )
    assert res.status_code == 200
    assert res.json["key"] == "test.pdf"
    assert res.json["status"] == "completed"
    assert res.json["metadata"] == {"title": "New title"}

    # Get all files
    res = client_with_credentials.get(
        f"{base_files_url.replace('{id}', id_)}/files", headers=headers
    )
    assert res.status_code == 200
    assert len(res.json["entries"]) == 1
    assert res.json["entries"][0]["key"] == "test.pdf"
    assert res.json["entries"][0]["status"] == "completed"
    assert res.json["entries"][0]["metadata"] == {"title": "New title"}

    # Delete a file
    res = client_with_credentials.delete(
        f"{base_files_url.replace('{id}', id_)}/files/test.pdf", headers=headers
    )
    assert res.status_code == 204

    # Get all files
    res = client_with_credentials.get(
        f"{base_files_url.replace('{id}', id_)}/files", headers=headers
    )
    assert res.status_code == 200
    assert len(res.json["entries"]) == 0


def test_default_preview_file(
    app, client_with_credentials, search_clear, headers, input_data, base_urls
):
    base_files_url = base_urls["base_draft_files_url"]
    res = client_with_credentials.post(
        base_urls["base_url"], headers=headers, json=input_data
    )
    assert res.status_code == 201
    id_ = res.json["id"]

    # Initialize 3 file uploads
    res = client_with_credentials.post(
        f"{base_files_url.replace('{id}', id_)}/files",
        headers=headers,
        json=[
            {"key": "f1.pdf"},
            {"key": "f2.pdf"},
            {"key": "f3.pdf"},
        ],
    )
    assert res.status_code == 201
    file_entries = res.json["entries"]
    assert len(file_entries) == 3
    assert {(f["key"], f["status"]) for f in file_entries} == {
        ("f1.pdf", "pending"),
        ("f2.pdf", "pending"),
        ("f3.pdf", "pending"),
    }
    assert res.json["default_preview"] is None

    # Upload and commit the 3 files
    for f in file_entries:
        res = client_with_credentials.put(
            f"{base_files_url.replace('{id}', id_)}/files/{f['key']}/content",
            headers={
                "content-type": "application/octet-stream",
                "accept": "application/json",
            },
            data=BytesIO(b"testfile"),
        )
        assert res.status_code == 200
        assert res.json["status"] == "pending"

        res = client_with_credentials.post(
            f"{base_files_url.replace('{id}', id_)}/files/{f['key']}/commit",
            headers=headers,
        )
        assert res.status_code == 200
        assert res.json["status"] == "completed"

    # Set the default preview file
    input_data["files"]["default_preview"] = "f1.pdf"
    res = client_with_credentials.put(
        f"{base_urls['base_url']}{id_}/draft", headers=headers, json=input_data
    )
    assert res.status_code == 200
    assert res.json["files"]["default_preview"] == "f1.pdf"

    # Change the default preview file
    input_data["files"]["default_preview"] = "f2.pdf"
    res = client_with_credentials.put(
        f"{base_urls['base_url']}{id_}/draft", headers=headers, json=input_data
    )
    assert res.status_code == 200
    assert res.json["files"]["default_preview"] == "f2.pdf"

    # Unset the default preview file
    input_data["files"]["default_preview"] = None
    res = client_with_credentials.put(
        f"{base_urls['base_url']}{id_}/draft", headers=headers, json=input_data
    )
    assert res.status_code == 200
    assert res.json["files"].get("default_preview") is None

    # Empty string the default preview file
    input_data["files"]["default_preview"] = ""
    res = client_with_credentials.put(
        f"{base_urls['base_url']}{id_}/draft", headers=headers, json=input_data
    )
    assert res.status_code == 200
    assert res.json["files"].get("default_preview") is None

    # Set the default preview file
    input_data["files"]["default_preview"] = "f3.pdf"
    res = client_with_credentials.put(
        f"{base_urls['base_url']}{id_}/draft", headers=headers, json=input_data
    )
    assert res.status_code == 200
    assert res.json["files"]["default_preview"] == "f3.pdf"

    # Delete the default preview file
    res = client_with_credentials.delete(
        f"{base_files_url.replace('{id}', id_)}/files/f3.pdf", headers=headers
    )
    assert res.status_code == 204

    # Get all files and check default preview
    res = client_with_credentials.get(
        f"{base_files_url.replace('{id}', id_)}/files", headers=headers
    )
    assert res.status_code == 200
    assert len(res.json["entries"]) == 2
    assert res.json["default_preview"] is None


def test_file_api_errors(
    client_with_credentials, search_clear, headers, input_data, base_urls
):
    base_files_url = base_urls["base_draft_files_url"]

    h = headers

    # Initialize a draft
    res = client_with_credentials.post(
        base_urls["base_url"], headers=headers, json=input_data
    )
    assert res.status_code == 201
    id_ = res.json["id"]

    # Initialize files upload
    # Pass an object instead of an array
    res = client_with_credentials.post(
        f"{base_files_url.replace('{id}', id_)}/files",
        headers=headers,
        json={"key": "test.pdf"},
    )
    assert res.status_code == 400

    res = client_with_credentials.post(
        f"{base_files_url.replace('{id}', id_)}/files",
        headers=headers,
        json=[
            {"key": "test.pdf", "title": "Test file"},
        ],
    )
    assert res.status_code == 201

    # Upload a file
    res = client_with_credentials.put(
        f"{base_files_url.replace('{id}', id_)}/files/test.pdf/content",
        headers={
            "content-type": "application/octet-stream",
            "accept": "application/json",
        },
        data=BytesIO(b"testfile"),
    )
    assert res.status_code == 200
    assert res.json["status"] == "pending"

    # Commit the uploaded file
    res = client_with_credentials.post(
        f"{base_files_url.replace('{id}', id_)}/files/test.pdf/commit", headers=headers
    )
    assert res.status_code == 200
    assert res.json["status"] == "completed"

    # Initialize same file upload again
    res = client_with_credentials.post(
        f"{base_files_url.replace('{id}', id_)}/files",
        headers=headers,
        json=[
            {"key": "test.pdf", "title": "Test file"},
        ],
    )
    assert res.status_code == 400


def assert_record_file_links(
    id_, generated_links, base_urls, site_hostname="127.0.0.1:5000"
):
    """Compare generated links to expected links."""
    base_files_url = base_urls["base_draft_files_url"]

    required_links = {
        "self": (
            f"https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files"
        ),
    }
    assert required_links.items() <= generated_links.items()


def assert_file_links(id_, generated_links, base_urls, site_hostname="127.0.0.1:5000"):
    """Compare generated links to expected links."""
    base_files_url = base_urls["base_draft_files_url"]
    required_links = {
        "self": (
            f"https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files/test.pdf"
        ),
        "content": (
            f"https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files/test.pdf/content"
        ),
        "commit": (
            f"https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files/test.pdf/commit"
        ),
    }
    assert required_links.items() <= generated_links.items()


def test_record_file_links(
    app,
    client_with_credentials,
    input_data,
    headers,
    base_urls,
    site_hostname="127.0.0.1:5000",
):
    base_files_url = base_urls["base_draft_files_url"]

    res = client_with_credentials.post(base_urls["base_url"], json=input_data)

    id_ = res.json["id"]
    assert (
        f"https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files"
        == res.json["links"]["files"]
    )

    res = client_with_credentials.post(
        f"{base_files_url.replace('{id}', id_)}/files",
        headers=headers,
        json=[
            {"key": "test.pdf", "title": "Test file"},
        ],
    )
    res = client_with_credentials.get(f"{base_files_url.replace('{id}', id_)}/files")
    assert_record_file_links(id_, res.json["links"], base_urls)
    assert_file_links(id_, res.json["entries"][0]["links"], base_urls)


@pytest.fixture()
def published_id(client_with_credentials, location, headers, base_urls):
    """A published record."""
    h = headers

    # Create a draft
    res = client_with_credentials.post(
        base_urls["base_url"],
        headers=h,
        json={
            "metadata": {"title": "Test"},
        },
    )
    assert res.status_code == 201
    id_ = res.json["id"]

    # Initialize files upload
    res = client_with_credentials.post(
        f"{base_urls['base_draft_files_url'].replace('{id}', id_)}/files",
        headers=h,
        json=[{"key": "test.pdf"}],
    )
    assert res.status_code == 201
    assert res.json["entries"][0]["key"] == "test.pdf"
    assert res.json["entries"][0]["status"] == "pending"

    # Upload a file
    res = client_with_credentials.put(
        f"{base_urls['base_draft_files_url'].replace('{id}', id_)}/files/test.pdf/content",
        headers={"content-type": "application/octet-stream"},
        data=BytesIO(b"testfile"),
    )
    assert res.status_code == 200

    # Commit the file
    res = client_with_credentials.post(
        f"{base_urls['base_draft_files_url'].replace('{id}', id_)}/files/test.pdf/commit",
        headers=h,
    )
    assert res.status_code == 200
    assert res.json["key"] == "test.pdf"
    assert res.json["status"] == "completed"

    # Publish the record
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/draft/actions/publish", headers=h
    )
    assert res.status_code == 202

    return id_


def test_files_publish_flow(
    client_with_credentials, search_clear, location, headers, base_urls
):
    """Test record creation."""
    h = headers
    # Create a draft
    res = client_with_credentials.post(
        base_urls["base_url"], headers=h, json={"metadata": {"title": "Test"}}
    )
    assert res.status_code == 201
    id_ = res.json["id"]

    # Initialize files upload
    res = client_with_credentials.post(
        f"{base_urls['base_draft_files_url'].replace('{id}', id_)}/files",
        headers=h,
        json=[{"key": "test.pdf"}],
    )
    assert res.status_code == 201
    assert res.json["entries"][0]["key"] == "test.pdf"
    assert res.json["entries"][0]["status"] == "pending"

    # Upload a file
    res = client_with_credentials.put(
        f"{base_urls['base_draft_files_url'].replace('{id}', id_)}/files/test.pdf/content",
        headers={"content-type": "application/octet-stream"},
        data=BytesIO(b"testfile"),
    )
    assert res.status_code == 200

    # Commit the file
    res = client_with_credentials.post(
        f"{base_urls['base_draft_files_url'].replace('{id}', id_)}/files/test.pdf/commit",
        headers=h,
    )
    assert res.status_code == 200
    assert res.json["key"] == "test.pdf"
    assert res.json["status"] == "completed"

    # Publish the record
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/draft/actions/publish", headers=h
    )
    assert res.status_code == 202

    # Check published files
    res = client_with_credentials.get(
        f"{base_urls['base_files_url'].replace('{id}', id_)}/files", headers=h
    )
    assert res.status_code == 200
    assert res.json["entries"][0]["key"] == "test.pdf"
    assert res.json["entries"][0]["status"] == "completed"

    # Edit the record
    res = client_with_credentials.post(f"{base_urls['base_url']}{id_}/draft", headers=h)
    assert res.status_code == 201

    # Publish again
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/draft/actions/publish", headers=h
    )
    assert res.status_code == 202

    # Check published files
    res = client_with_credentials.get(
        f"{base_urls['base_files_url'].replace('{id}', id_)}/files", headers=h
    )
    assert res.status_code == 200
    assert res.json["entries"][0]["key"] == "test.pdf"
    assert res.json["entries"][0]["status"] == "completed"


def test_metadata_only_record(
    client_with_credentials, search_clear, location, headers, base_urls
):
    """Test record with files disabled."""
    h = headers
    # Create a draft
    res = client_with_credentials.post(
        base_urls["base_url"],
        headers=h,
        json={"metadata": {"title": "Test"}, "files": {"enabled": False}},
    )
    assert res.status_code == 201
    id_ = res.json["id"]

    # Publish the record
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/draft/actions/publish", headers=h
    )
    assert res.status_code == 202

    # Check published files
    res = client_with_credentials.get(
        f"{base_urls['base_files_url'].replace('{id}', id_)}/files", headers=h
    )
    assert res.status_code == 200
    assert res.json["enabled"] is False
    assert "entries" not in res.json

    # Edit the record
    res = client_with_credentials.post(f"{base_urls['base_url']}{id_}/draft", headers=h)
    assert res.status_code == 201

    # Publish again
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/draft/actions/publish", headers=h
    )
    assert res.status_code == 202

    # Check published files
    res = client_with_credentials.get(
        f"{base_urls['base_files_url'].replace('{id}', id_)}/files", headers=h
    )
    assert res.status_code == 200
    assert res.json["enabled"] is False
    assert "entries" not in res.json


def test_import_files(
    client_with_credentials, search_clear, location, headers, published_id, base_urls
):
    """Test import files from previous version."""
    h = headers
    id_ = published_id

    # New version
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/versions", headers=h
    )
    assert res.status_code == 201
    new_id = res.json["id"]

    # Check new version files
    res = client_with_credentials.get(
        f"{base_urls['base_draft_files_url'].replace('{id}', new_id)}/files", headers=h
    )
    assert res.status_code == 200
    assert len(res.json["entries"]) == 0

    # Import files from previous version
    # Import files from previous version
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{new_id}/draft/actions/files-import", headers=h
    )
    assert res.status_code == 201
    assert res.content_type == "application/json"

    # Check new version files
    res = client_with_credentials.get(
        f"{base_urls['base_draft_files_url'].replace('{id}', new_id)}/files", headers=h
    )
    assert res.status_code == 200
    assert len(res.json["entries"]) == 1


def test_import_files_metadata_only(
    client_with_credentials, search_clear, location, headers, base_urls
):
    """Test import files from previous version."""
    h = headers

    res = client_with_credentials.post(
        base_urls["base_url"],
        headers=h,
        json={"metadata": {"title": "Test"}, "files": {"enabled": False}},
    )
    assert res.status_code == 201
    id_ = res.json["id"]

    # Publish
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/draft/actions/publish", headers=h
    )
    assert res.status_code == 202

    # New version
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/versions", headers=h
    )
    assert res.status_code == 201
    new_id = res.json["id"]

    # Check new version files
    res = client_with_credentials.get(
        f"{base_urls['base_draft_files_url'].replace('{id}', new_id)}/files", headers=h
    )
    assert res.status_code == 200
    assert "entries" not in res.json

    # Import files from previous version
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{new_id}/draft/actions/files-import", headers=h
    )
    assert res.status_code == 400


def test_import_files_no_version(
    client_with_credentials, search_clear, location, headers, base_urls
):
    """Test import files from previous version."""
    h = headers

    res = client_with_credentials.post(
        base_urls["base_url"],
        headers=h,
        json={"metadata": {"title": "Test"}, "files": {"enabled": True}},
    )
    assert res.status_code == 201
    id_ = res.json["id"]

    # Cannot import files from a non-existing previous version
    res = client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/draft/actions/files-import", headers=h
    )
    assert res.status_code == 404


def assert_published_record_file_links(
    id_, generated_links, base_urls, site_hostname="127.0.0.1:5000"
):
    """Compare generated links to expected links."""
    required_links = {
        "self": (
            f"https://{site_hostname}/api{base_urls['base_files_url'].replace('{id}', id_)}/files"
        ),
    }
    assert required_links.items() <= generated_links.items()


def assert_published_file_links(
    id_, generated_links, base_urls, site_hostname="127.0.0.1:5000"
):
    """Compare generated links to expected links."""
    required_links = {
        "self": (
            f"https://{site_hostname}/api{base_urls['base_files_url'].replace('{id}', id_)}/files/test.pdf"
        ),
        "content": (
            f"https://{site_hostname}/api{base_urls['base_files_url'].replace('{id}', id_)}/files/test.pdf/content"
        ),
        "commit": (
            f"https://{site_hostname}/api{base_urls['base_files_url'].replace('{id}', id_)}/files/test.pdf/commit"
        ),
    }
    assert required_links.items() <= generated_links.items()


def test_published_links(
    app,
    client_with_credentials,
    input_data,
    headers,
    base_urls,
):
    res = client_with_credentials.post(base_urls["base_url"], json=input_data)
    id_ = res.json["id"]
    client_with_credentials.post(
        f"{base_urls['base_draft_files_url'].replace('{id}', id_)}/files",
        headers=headers,
        json=[
            {"key": "test.pdf", "title": "Test file"},
        ],
    )
    client_with_credentials.put(
        f"{base_urls['base_draft_files_url'].replace('{id}', id_)}/files/test.pdf/content",
        headers={"content-type": "application/octet-stream"},
        data=BytesIO(b"testfile"),
    )
    client_with_credentials.post(
        f"{base_urls['base_draft_files_url'].replace('{id}', id_)}/files/test.pdf/commit",
        headers=headers,
    )
    client_with_credentials.post(
        f"{base_urls['base_url']}{id_}/draft/actions/publish", headers=headers
    )
    res = client_with_credentials.get(
        f"{base_urls['base_files_url'].replace('{id}', id_)}/files", headers=headers
    )
    assert_published_record_file_links(id_, res.json["links"], base_urls)
    assert_published_file_links(id_, res.json["entries"][0]["links"], base_urls)

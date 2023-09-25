
import pytest
from invenio_access.permissions import system_identity
from invenio_pidstore.errors import PIDDoesNotExistError



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


def test_read(
    app, db, sample_draft, record_service, sample_metadata_list, search_clear
):
    with pytest.raises(PIDDoesNotExistError):
        record_service.read_draft(system_identity, "fwegthi8op")
    read_record = record_service.read_draft(system_identity, sample_draft["id"])
    assert read_record.data["metadata"] == sample_draft.metadata


def test_create(app, db, record_service, sample_metadata_list, search_clear):
    created_records = []
    for sample_metadata_point in sample_metadata_list:
        created_records.append(
            record_service.create(system_identity, sample_metadata_point)
        )
    for sample_metadata_point, created_record in zip(
        sample_metadata_list, created_records
    ):
        created_record_reread = record_service.read_draft(
            system_identity, created_record["id"]
        )
        assert (
            created_record_reread.data["metadata"] == sample_metadata_point["metadata"]
        )


def test_update(
    app, db, sample_draft, record_service, sample_metadata_list, search_clear
):
    with pytest.raises(PIDDoesNotExistError):
        record_service.update_draft(
            system_identity, "fwsegerhjtyuk754dh", sample_metadata_list[2]
        )

    old_record_data = record_service.read_draft(
        system_identity, sample_draft["id"]
    ).data
    updated_record = record_service.update_draft(
        system_identity, sample_draft["id"], sample_metadata_list[2]
    )
    updated_record_read = record_service.read_draft(system_identity, sample_draft["id"])
    assert old_record_data["metadata"] == sample_draft["metadata"]
    assert (
        updated_record.data["metadata"]
        == sample_metadata_list[2]["metadata"]
        != old_record_data["metadata"]
    )
    assert updated_record_read.data["metadata"] == updated_record.data["metadata"]
    assert (
        updated_record.data["revision_id"]
        == updated_record_read.data["revision_id"]
        == old_record_data["revision_id"] + 1
    )


def test_delete(app, db, sample_draft, record_service, search_clear):
    with pytest.raises(PIDDoesNotExistError):
        record_service.delete_draft(system_identity, "fwsegerhjtyuk754dh")

    to_delete_record = record_service.read_draft(system_identity, sample_draft["id"])
    assert to_delete_record
    record_service.delete_draft(system_identity, sample_draft["id"])
    with pytest.raises(PIDDoesNotExistError):
        record_service.read_draft(system_identity, sample_draft["id"])


def test_create_published(app, db, sample_metadata_list, search_clear):
    from nr_documents.proxies import current_published_service

    created_records = []
    for sample_metadata_point in sample_metadata_list:
        created_records.append(
            current_published_service.create(system_identity, sample_metadata_point)
        )
    for sample_metadata_point, created_record in zip(
        sample_metadata_list, created_records
    ):
        created_record_reread = current_published_service.read(
            system_identity, created_record["id"]
        )
        assert (
            created_record_reread.data["metadata"] == sample_metadata_point["metadata"]
        )


import pytest
from invenio_records_resources.resources import FileResource

from nr_documents.resources.files.config import NrDocumentsFileResourceConfig
from nr_documents.services.files.config import NrDocumentsFileServiceConfig
from nr_documents.services.files.service import NrDocumentsFileService


@pytest.fixture()
def input_data(input_data):
    input_data["files"] = {"enabled": True}
    return input_data


@pytest.fixture(scope="module")
def file_service():
    """File service shared fixture."""
    service = NrDocumentsFileService(NrDocumentsFileServiceConfig())
    return service


@pytest.fixture(scope="module")
def file_resource(file_service):
    """File Resources."""
    return FileResource(NrDocumentsFileResourceConfig(), file_service)

import importlib_metadata
from flask_resources import ResponseHandler
from invenio_drafts_resources.resources import RecordResourceConfig

from common.oai.server.serializers import dublincore_etree
from documents.resources.records.ui import DocumentsUIJSONSerializer, DocumentsDublinCoreXMLSerializer
from oarepo_runtime.resources.responses import ExportableResponseHandler, OAIExportableResponseHandler
from invenio_records_resources.resources.records.headers import etag_headers
from invenio_rdm_records.resources.serializers.dublincore import DublinCoreXMLSerializer

class DocumentsResourceConfig(RecordResourceConfig):
    """DocumentsRecord resource config."""

    blueprint_name = "documents"
    url_prefix = "/docs/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.documents.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ExportableResponseHandler(
                export_code="ui_json", name="Native UI JSON", serializer=DocumentsUIJSONSerializer()
            ),
            "application/x-dc+xml": OAIExportableResponseHandler(
                export_code="dc_xml", name="Dublin Core XML", serializer=DocumentsDublinCoreXMLSerializer(),
                headers=etag_headers, oai_code="oai_dc",
                schema="local://documents-1.0.0.json"
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }

    @property
    def error_handlers(self):
        entrypoint_error_handlers = {}
        for x in importlib_metadata.entry_points(
                group="invenio.documents_record.error_handlers"
        ):
            entrypoint_error_handlers.update(x.load())
        return {**super().error_handlers, **entrypoint_error_handlers}

    @property
    def request_body_parsers(self):
        entrypoint_request_bodyparsers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.documents_record.request_bodyparsers"
        ):
            entrypoint_request_bodyparsers.update(x.load())
        return {
            **super().request_body_parsers,
            **entrypoint_request_bodyparsers,
        }

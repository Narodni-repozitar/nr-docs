
from dcxml import simpledc
from flask import g
from invenio_rdm_records.resources.serializers import DublinCoreXMLSerializer
from invenio_rdm_records.proxies import current_rdm_records_service

from flask import current_app
from invenio_records_resources.services.base.config import ConfiguratorMixin
from invenio_base.utils import obj_or_import_string
from oarepo_runtime.resources.responses import OAIExportableResponseHandler

def get_serializer(oai_code, schema):
    for model_dict in current_app.config["RDM_MODELS"]:
        config_cls = obj_or_import_string(model_dict["api_resource_config"])
        if issubclass(config_cls, ConfiguratorMixin):
            config = config_cls.build(current_app)
        else:
            config = config_cls()

        handlers = [
            handler
            for handler in config.response_handlers.values()
            if isinstance(handler, OAIExportableResponseHandler)
        ]

        for handler in handlers:
            if handler.oai_code == oai_code and handler.schema == schema:
                return handler.serializer
    return None

def dublincore_etree(pid, record, **serializer_kwargs):
    """Get DublinCore XML etree for OAI-PMH. From invenio-rdm-records."""
    item = current_rdm_records_service.oai_result_item(g.identity, record["_source"])
    serializer = get_serializer("oai_dc", record["_source"]["$schema"])
    # TODO: DublinCoreXMLSerializer should be able to dump an etree directly
    # instead. See https://github.com/inveniosoftware/flask-resources/issues/117
    obj = serializer.dump_obj(item.to_dict()) #do we need arguments here or is this always handled in resource config
    return simpledc.dump_etree(obj)
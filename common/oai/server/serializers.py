
from dcxml import simpledc
from flask import g
from invenio_rdm_records.proxies import current_rdm_records_service
from oarepo_runtime.resources.responses import OAIExportableResponseHandler
from oarepo_rdm.proxies import current_oarepo_rdm

def get_serializer(oai_code: str, schema: str):
    for model in current_oarepo_rdm.rdm_models:
        if schema != model.api_service_config.record_cls.schema.value:
            continue
        handlers = [
            handler
            for handler in model.api_resource_config.response_handlers.values()
            if isinstance(handler, OAIExportableResponseHandler) and handler.oai_code == oai_code
        ]
        if len(handlers) == 1:
            return handlers[0].serializer
        # exception for having more handlers?

    return None

def dublincore_etree(pid, record, **serializer_kwargs):

    item = current_rdm_records_service.oai_result_item(g.identity, record["_source"])
    serializer = get_serializer("oai_dc", record["_source"]["$schema"])
    # TODO: DublinCoreXMLSerializer should be able to dump an etree directly
    # instead. See https://github.com/inveniosoftware/flask-resources/issues/117
    obj = serializer.dump_obj(item.to_dict()) #do we need arguments here or is this always handled in resource config
    return simpledc.dump_etree(obj)

from flask_resources import BaseListSchema
from invenio_records_resources.proxies import current_service_registry
from marshmallow import fields, post_dump


class FilteredUIListSchema(BaseListSchema):
    params = fields.Raw()

    @post_dump
    def after_dump(self, data, *args, **kwargs):
        service = self.context["service"]
        params = data.setdefault("params", {})
        service_config = current_service_registry.get(service).config
        search_options = service_config.search
        facets = search_options.facets
        translated_params = {}

        for k, v in params.items():
            facet = facets.get(k)
            if not facet:
                continue
            if not hasattr(facet, "value_labels"):
                translated_params[k] = [{"key": key} for key in v]
            else:
                labels = facet.value_labels(v)
                translated_params[k] = [
                    {"key": key, "label": labels.get(key, key)} for key in v
                ]
        data["filters_l10n"] = translated_params
        return data

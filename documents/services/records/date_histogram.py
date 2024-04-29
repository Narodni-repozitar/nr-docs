from invenio_search.engine import dsl
from invenio_records_resources.services.records.facets.facets import LabelledFacetMixin


class DateRangeHistogram(LabelledFacetMixin, dsl.DateHistogramFacet):
    def get_value_filter(self, filter_value):
        if "/" in filter_value:
            start, end = filter_value.split("/")
            return dsl.query.Range(
                _expand__to_dot=False,
                **{
                    self._params["field"]: {
                        "gte": start if start else "1900-01-01",
                        "lte": end if end else "2024-01-01",
                    }
                },
            )
        return super().get_value_filter(filter_value)

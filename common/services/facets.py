from invenio_records_resources.services.records.facets.facets import LabelledFacetMixin
from invenio_search.engine import dsl


class IntegerHistogramFacet(LabelledFacetMixin, dsl.Facet):
    """Histogram facet.

    .. code-block:: python

        facets = {
            'year': IntegerHistogramFacet(
                field='year',
                label=_('Year'),
                size=1000000
            )
        }
    """

    agg_type = "terms"

    def get_value_filter(self, filter_value):
        if "/" in filter_value:
            start, end = filter_value.split("/")
            return dsl.query.Range(
                _expand__to_dot=False,
                **{
                    self._params["field"]: {
                        "gte": start,
                        "lte": end,
                    }
                },
            )
        return dsl.query.Term(
            _expand__to_dot=False,
            **{
                self._params["field"]: filter_value
            },
        )

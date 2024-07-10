from invenio_records_resources.services.records.facets.facets import LabelledFacetMixin
from invenio_search.engine import dsl


class YearAutoHistogramFacet(LabelledFacetMixin, dsl.Facet):
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

    agg_type = "auto_date_histogram"

    def __init__(self, **kwargs):
        self._min_doc_count = kwargs.pop("min_doc_count", 0)
        buckets = kwargs.pop("buckets", 20)
        super().__init__(**kwargs, buckets=buckets, format="yyyy")

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

    def add_filter(self, filter_values):
        ret = super().add_filter(filter_values)
        return ret

    def get_labelled_values(self, data, filter_values):
        """Get a labelled version of a bucket."""
        interval = data.to_dict()["interval"]
        buckets = data.buckets
        if self._min_doc_count > 0:
            buckets = self._merge_small_buckets(buckets)

        out_buckets = []
        for i, bucket in enumerate(buckets):
            value = int(bucket.key_as_string.split("-")[0])

            out_buckets.append(
                {
                    **bucket.to_dict(),
                    "start": str(value),
                }
            )
            if i > 0:
                out_buckets[i-1]["end"] = str(value-1)

        return {
            "buckets": out_buckets,
            "label": str(self._label),
            "interval": interval,
        }

    def _merge_small_buckets(self, buckets):
        """
        Merges small buckets into the previous bucket. If the small bucket is the first one,
        merge it with subsequent buckets until the first non-small bucket is found.
        """
        ret = []
        initial_small_buckets = 0
        for bucket in buckets:
            if bucket.doc_count < self._min_doc_count:
                if ret:
                    ret[-1].doc_count += bucket.doc_count
                else:
                    initial_small_buckets += bucket.doc_count
            else:
                ret.append(bucket)
        if ret and initial_small_buckets:
            doc_count = ret[0].doc_count + initial_small_buckets
            ret[0] = buckets[0]
            ret[0].doc_count = doc_count

        return ret


class YearStatsFacet(LabelledFacetMixin, dsl.Facet):
    """Stats facet.

    .. code-block:: python

        facets = {
            'year_stats': StatsFacet(
                field='year',
                label=_('Year'),
            )
        }
    """

    agg_type = "stats"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_labelled_values(self, data, filter_values):
        return {
            'min': data.min_as_string[:4],
            'max': data.max_as_string[:4],
        }
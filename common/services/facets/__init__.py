import re
from typing import List, Dict

from invenio_search.engine import dsl
from invenio_records_resources.services.records.facets.facets import TermsFacet, LabelledFacetMixin

from oarepo_runtime.i18n import get_locale


class KeywordsFacet(TermsFacet):

    def get_localized_keyword_field(self):
        locale = get_locale()
        return f"{self._params['field']}.{locale}"

    def get_aggregation(self):
        """
        Return the aggregation object.
        """
        locale = get_locale()
        agg = dsl.A(self.agg_type, **{**self._params, 'field': self.get_localized_keyword_field()})
        if self._metric:
            agg.metric("metric", self._metric)
        return agg

    def add_filter(self, filter_values):
        locale = get_locale()
        if filter_values:
            return dsl.query.Terms(
                _expand__to_dot=False, **{self.get_localized_keyword_field(): filter_values}
            )


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
        # TODO: the minimum interval should be year, but opensearch does not support it yet
        super().__init__(**kwargs, buckets=buckets, format="yyyy", minimum_interval="month")

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

        # fix for opensearch bug
        data = self.fix_yearly_interval(data)

        interval = data["interval"]

        interval_in_years = int(re.sub(r"\D", "", interval))

        buckets = data["buckets"]

        for bucket in buckets:
            bucket["interval"] = interval_in_years

        if self._min_doc_count > 0:
            buckets = self._merge_small_buckets(buckets)

        out_buckets = []
        for i, bucket in enumerate(buckets):
            value = int(bucket["key_as_string"].split("-")[0])

            out_buckets.append(
                {
                    **bucket,
                    "interval": f"{bucket['interval']}y",
                    "start": str(value),
                }
            )
            if i > 0:
                out_buckets[i-1]["end"] = str(value-1)

        if out_buckets:
            out_buckets[-1]["end"] = str(int(out_buckets[-1]["start"]) + interval_in_years - 1)

        return {
            "buckets": out_buckets,
            "label": str(self._label),
            "interval": interval,
        }

    def merge_buckets(self, buckets):
        merged = {}

        for bucket in buckets:
            key = bucket["key_as_string"]
            if key not in merged:
                merged[key] = {
                    "key_as_string": key,
                    "key": bucket["key"],
                    "doc_count": 0,
                }

            merged[key]["doc_count"] += bucket["doc_count"]

        result = list(merged.values())
        return result

    def fix_yearly_interval(self, data) -> Dict:
        """
        Currently opensearch has a bug that does not allow to set minimum_interval to year.
        This function will fix the interval to be yearly if the minimum_interval is has lower value.
        """
        data = data.to_dict()

        interval = data["interval"]

        if interval.endswith("y"):
            # no need to fix the interval, as it is in years
            return data

        # make sure it is in years
        data["interval"] = "1y"

        buckets = data["buckets"]
        data["buckets"] = out_buckets = []

        by_year = {}

        # there might be several buckets returned with the same year - merge them
        for bucket in buckets:
            key = bucket["key_as_string"]
            if key not in by_year:
                by_year[key] = {
                    "key_as_string": key,
                    "key": bucket["key"],
                    "doc_count": 0,
                }
                out_buckets.append(by_year[key])

            by_year[key]["doc_count"] += bucket["doc_count"]

        return data

    def _merge_small_buckets(self, buckets: List[Dict]):
        """
        Merges small buckets into the previous bucket. If the small bucket is the first one,
        merge it with subsequent buckets until the first non-small bucket is found.
        """
        ret = []
        initial_small_buckets = 0
        initial_small_interval = 0
        for bucket in buckets:
            if bucket["doc_count"] < self._min_doc_count:
                if ret:
                    ret[-1]["doc_count"] += bucket["doc_count"]
                    ret[-1]["interval"] += bucket["interval"]
                else:
                    initial_small_buckets += bucket["doc_count"]
                    initial_small_interval += bucket["interval"]
            else:
                ret.append(bucket)

        if ret and initial_small_buckets:
            doc_count = ret[0]["doc_count"] + initial_small_buckets
            interval = ret[0]["interval"] + initial_small_interval
            ret[0] = buckets[0]
            ret[0]["doc_count"] = doc_count
            ret[0]["interval"] = interval

        return ret

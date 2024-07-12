from invenio_search.engine import dsl
from invenio_records_resources.services.records.facets.facets import TermsFacet


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
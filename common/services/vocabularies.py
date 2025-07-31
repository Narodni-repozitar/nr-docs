import logging

from invenio_records_resources.services.records.params.base import ParamInterpreter
from invenio_records_resources.services.records.params.querystr import QueryStrParam
from opensearch_dsl.query import Bool, Term

log = logging.getLogger(__name__)


class DeprecatedVocabularyParamInterpreter(ParamInterpreter):
    """Param interpreter class that always removes deprecated vocabulary items."""

    def apply(self, identity, search, params):
        """Apply the parameters."""
        return search.filter(Bool(must_not=[Term(tags="deprecated")]))


class SuggestionOnlyQueryStrParam(QueryStrParam):
    """Evaluate the 'q' or 'suggest' parameter."""

    def apply(self, identity, search, params):
        """Evaluate the query str on the search."""

        if "q" in params and "/" in params["q"] and '"' not in params["q"]:
            params["suggest"] = params.pop("q")
        return super().apply(identity, search, params)


def update_vocabulary_search_options():
    """Update search options to include deprecated items removal."""

    def remove_deprecated_from_search(search_options):
        if (
            DeprecatedVocabularyParamInterpreter
            not in search_options.params_interpreters_cls
        ):
            search_options.params_interpreters_cls.append(
                DeprecatedVocabularyParamInterpreter
            )

    def replace_querystr_with_suggestion_only(search_options):
        for idx, p in enumerate(search_options.params_interpreters_cls):
            if p is QueryStrParam:
                search_options.params_interpreters_cls[idx] = (
                    SuggestionOnlyQueryStrParam
                )

    from invenio_vocabularies.contrib.affiliations.config import (
        SearchOptions as AffiliationsSearchOptions,
    )

    remove_deprecated_from_search(AffiliationsSearchOptions)
    replace_querystr_with_suggestion_only(AffiliationsSearchOptions)

    from invenio_vocabularies.contrib.funders.config import (
        SearchOptions as FundersSearchOptions,
    )

    remove_deprecated_from_search(FundersSearchOptions)
    replace_querystr_with_suggestion_only(FundersSearchOptions)

    from invenio_vocabularies.contrib.awards.config import (
        SearchOptions as AwardsSearchOptions,
    )

    remove_deprecated_from_search(AwardsSearchOptions)
    replace_querystr_with_suggestion_only(AwardsSearchOptions)

    from oarepo_vocabularies.services.search import VocabularySearchOptions

    remove_deprecated_from_search(VocabularySearchOptions)
    replace_querystr_with_suggestion_only(VocabularySearchOptions)

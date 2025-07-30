from invenio_records_resources.services.records.params.base import ParamInterpreter
from opensearch_dsl.query import Bool, Term


class DeprecatedVocabularyParamInterpreter(ParamInterpreter):
    """Param interpreter class that always removes deprecated vocabulary items."""

    def apply(self, identity, search, params):
        """Apply the parameters."""
        return search.filter(Bool(must_not=[Term(tags="deprecated")]))


def remove_deprecated_vocabulary_items_from_search(app):
    """Add deprecated items removal to vocabulary search."""
    with app.app_context():
        from invenio_records_resources.proxies import current_service_registry
        from oarepo_vocabularies.services.search import VocabularySearchOptions

        # oarepo extensions might not have been applied at this point,
        # so we need to patch both the running service and the search options
        if (
            DeprecatedVocabularyParamInterpreter
            not in VocabularySearchOptions.params_interpreters_cls
        ):
            VocabularySearchOptions.params_interpreters_cls.append(
                DeprecatedVocabularyParamInterpreter
            )

        def remove_deprecated_from_search(service):
            search_options = service.config.search
            if (
                DeprecatedVocabularyParamInterpreter
                not in search_options.params_interpreters_cls
            ):
                search_options.params_interpreters_cls.append(
                    DeprecatedVocabularyParamInterpreter
                )

        try:
            remove_deprecated_from_search(current_service_registry.get("vocabularies"))
            remove_deprecated_from_search(current_service_registry.get("affiliations"))
            remove_deprecated_from_search(current_service_registry.get("awards"))
            remove_deprecated_from_search(current_service_registry.get("funders"))
        except KeyError:
            # If the service is not registered, it means it is not available in this context.
            pass

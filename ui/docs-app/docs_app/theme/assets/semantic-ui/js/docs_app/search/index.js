import { createSearchAppInit } from '@js/invenio_search_ui'
import {
  BucketAggregationElement,
  BucketAggregationValuesElement,
  CountElement,
  EmptyResultsElement,
  ErrorElement,
  ResultsGridItemWithState,
  ResultsListItemWithState,
  SearchAppFacets,
  SearchAppSearchbarContainer,
  SearchFiltersToggleElement,
  SortElement
} from '@js/oarepo_ui/search'
import { parametrize, overrideStore } from 'react-overridable'

const appName = 'DocsApp.Search'

const SearchAppSearchbarContainerWithConfig = parametrize(SearchAppSearchbarContainer, { appName: appName })
const ResultsListItemWithConfig = parametrize(ResultsListItemWithState, { appName: appName })
const ResultsGridItemWithConfig = parametrize(ResultsGridItemWithState, { appName: appName })

export const defaultComponents = {
  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]: BucketAggregationValuesElement,
  [`${appName}.Count.element`]: CountElement,
  [`${appName}.EmptyResults.element`]: EmptyResultsElement,
  [`${appName}.Error.element`]: ErrorElement,
  [`${appName}.ResultsGrid.item`]: ResultsGridItemWithConfig,
  [`${appName}.ResultsList.item`]: ResultsListItemWithConfig,
  [`${appName}.SearchApp.facets`]: SearchAppFacets,
  [`${appName}.SearchApp.searchbarContainer`]: SearchAppSearchbarContainerWithConfig,
  [`${appName}.SearchFilters.Toggle.element`]: SearchFiltersToggleElement,
  // [`${appName}.Sort.element`]: SortElement,
  //   [`${appName}.SearchBar.element`]: RDMRecordMultipleSearchBarElement,
}

const overriddenComponents = overrideStore.getAll()

createSearchAppInit(
  { ...defaultComponents, ...overriddenComponents },
  true,
  'invenio-search-config',
  true,
)

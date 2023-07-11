import { createSearchAppInit } from '@js/invenio_search_ui'
import {
  BucketAggregationElement,
  BucketAggregationValuesElement,
  CountElement,
  ErrorElement,
  SearchAppFacets,
  SearchAppSearchbarContainer,
  SearchFiltersToggleElement,
  SearchAppSort
} from '@js/oarepo_ui/search'
import {
  OaiRunResultsListItemWithState
} from './components'
import { parametrize, overrideStore } from 'react-overridable'

const appName = 'OaiRun.Search'

const SearchAppSearchbarContainerWithConfig = parametrize(SearchAppSearchbarContainer, { appName: appName })
const ResultsListItemWithConfig = parametrize(OaiRunResultsListItemWithState, { appName: appName })


export const defaultComponents = {
  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]: BucketAggregationValuesElement,
  [`${appName}.Count.element`]: CountElement,
  // [`${appName}.EmptyResults.element`]: EmptyResultsElement,
  [`${appName}.Error.element`]: ErrorElement,
  // [`${appName}.ResultsGrid.item`]: ResultsGridItemWithConfig,
  [`${appName}.ResultsList.item`]: ResultsListItemWithConfig,
  [`${appName}.SearchApp.facets`]: SearchAppFacets,
  [`${appName}.SearchApp.searchbarContainer`]: SearchAppSearchbarContainerWithConfig,
  [`${appName}.SearchApp.sort`]: SearchAppSort,
  [`${appName}.SearchFilters.Toggle.element`]: SearchFiltersToggleElement,
}

const overriddenComponents = overrideStore.getAll()

createSearchAppInit(
  { ...defaultComponents, ...overriddenComponents },
  true,
  'invenio-search-config',
  true,
)
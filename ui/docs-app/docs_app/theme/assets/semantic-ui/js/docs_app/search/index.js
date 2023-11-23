import * as React from 'react'
import { createSearchAppInit } from '@js/invenio_search_ui'
import {
  ActiveFiltersElement,
  BucketAggregationElement,
  BucketAggregationValuesElement,
  ErrorElement,
  SearchAppFacets,
  SearchAppLayout,
  SearchAppResults,
  SearchAppResultOptions,
  SearchAppSearchbarContainer,
  SearchFiltersToggleElement,
  SearchAppSort
} from '@js/oarepo_ui/search'
import {
  EmptyResultsElement,
  MultipleSearchBarElement,
  ResultsGridItemWithState,
  ResultsListItemWithState
} from './components'
import { parametrize } from 'react-overridable'

const appName = 'DocsApp.Search'

const SearchAppSearchbarContainerWithConfig = parametrize(SearchAppSearchbarContainer, { appName: appName })
const ResultsListItemWithConfig = parametrize(ResultsListItemWithState, { appName: appName })
const ResultsGridItemWithConfig = parametrize(ResultsGridItemWithState, { appName: appName })

export const defaultComponents = {
  [`${appName}.ActiveFilters.element`]: ActiveFiltersElement,
  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]: BucketAggregationValuesElement,
  [`${appName}.EmptyResults.element`]: EmptyResultsElement,
  [`${appName}.Error.element`]: ErrorElement,
  [`${appName}.ResultsGrid.item`]: ResultsGridItemWithConfig,
  [`${appName}.ResultsList.item`]: ResultsListItemWithConfig,
  [`${appName}.SearchApp.facets`]: SearchAppFacets,
  [`${appName}.SearchApp.layout`]: SearchAppLayout,
  [`${appName}.SearchApp.searchbarContainer`]: SearchAppSearchbarContainerWithConfig,
  [`${appName}.SearchApp.sort`]: SearchAppSort,
  [`${appName}.SearchApp.resultOptions`]: SearchAppResultOptions,
  [`${appName}.SearchApp.results`]: SearchAppResults,
  [`${appName}.SearchFilters.Toggle.element`]: SearchFiltersToggleElement,
  [`${appName}.SearchBar.element`]: MultipleSearchBarElement,
}

createSearchAppInit(
  { ...defaultComponents },
  true,
  'invenio-search-config',
  true,
)

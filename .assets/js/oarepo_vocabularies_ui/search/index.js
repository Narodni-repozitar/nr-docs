import { createSearchAppInit } from "@js/invenio_search_ui";
import {
  BucketAggregationElement,
  BucketAggregationValuesElement,
  ErrorElement,
  SearchAppFacets,
  SearchAppSearchbarContainer,
  SearchFiltersToggleElement,
  SearchAppSort,
  SearchAppResultOptions,
  SearchAppResults,
  SearchAppLayout,
  EmptyResultsElement,
} from "@js/oarepo_ui/search";
import { VocabularyResultsListItemWithState } from "./components";
import { parametrize, overrideStore } from "react-overridable";
import React from "react";
const appName = "OarepoVocabularies.Search";
const SearchAppSearchbarContainerWithConfig = parametrize(
  SearchAppSearchbarContainer,
  { appName: appName }
);
const ResultsListItemWithConfig = parametrize(
  VocabularyResultsListItemWithState,
  { appName: appName }
);

// const ResultsGridItemWithConfig = parametrize(ResultsGridItemWithState, { appName: appName })
export const defaultComponents = {
  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]:
    BucketAggregationValuesElement,
  [`${appName}.EmptyResults.element`]: EmptyResultsElement,
  [`${appName}.Error.element`]: ErrorElement,
  // [`${appName}.ResultsGrid.item`]: ResultsGridItemWithConfig,
  [`${appName}.ResultsList.item`]: ResultsListItemWithConfig,
  [`${appName}.SearchApp.facets`]: SearchAppFacets,
  [`${appName}.SearchApp.searchbarContainer`]:
    SearchAppSearchbarContainerWithConfig,
  [`${appName}.SearchApp.sort`]: SearchAppSort,
  [`${appName}.SearchFilters.Toggle.element`]: SearchFiltersToggleElement,

  [`${appName}.SearchApp.resultOptions`]: SearchAppResultOptions,
  [`${appName}.SearchApp.results`]: SearchAppResults,
  [`${appName}.SearchApp.layout`]: SearchAppLayout,
};
const overriddenComponents = overrideStore.getAll();

createSearchAppInit(
  { ...defaultComponents, ...overriddenComponents },
  true,
  "invenio-search-config",
  true
);

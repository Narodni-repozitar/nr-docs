import * as React from "react";
import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
} from "@js/oarepo_ui";
import {
  ResultsGridItemWithState,
  ResultsListItemWithState,
} from "./components";
import { EmptyResultsElement } from "@nr";
import { parametrize } from "react-overridable";
const [searchAppConfig, ...otherSearchAppConfigs] = parseSearchAppConfigs();
const { overridableIdPrefix } = searchAppConfig;

const ResultsListItemWithConfig = parametrize(ResultsListItemWithState, {
  appName: overridableIdPrefix,
});
const ResultsGridItemWithConfig = parametrize(ResultsGridItemWithState, {
  appName: overridableIdPrefix,
});

export const componentOverrides = {
  [`${overridableIdPrefix}.EmptyResults.element`]: EmptyResultsElement,
  [`${overridableIdPrefix}.ResultsGrid.item`]: ResultsGridItemWithConfig,
  [`${overridableIdPrefix}.ResultsList.item`]: ResultsListItemWithConfig,
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
};

createSearchAppsInit({ componentOverrides: componentOverrides });

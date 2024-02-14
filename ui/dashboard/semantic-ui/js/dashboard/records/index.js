import _get from "lodash/get";
import _truncate from "lodash/truncate";
import React from "react";
import { Grid, Dropdown } from "semantic-ui-react";
import { parametrize, overrideStore } from "react-overridable";
import { createSearchAppInit } from "@js/invenio_search_ui";
import {
  ActiveFiltersElement,
  BucketAggregationElement,
  BucketAggregationValuesElement,
  SearchAppResultOptions,
  SearchAppSort,
  SearchappSearchbarElement,
  EmptyResultsElement,
  ResultCountWithState,
} from "@js/oarepo_ui/search";
import { UserDashboardSearchAppLayoutHOC } from "../components/UserDashboardSearchAppLayout";
import { UserDashboardSearchAppResultView } from "../components/UserDashboardSearchAppResultView";
import { i18next } from "@translations/i18next";
import { ComputerTabletRecordsListItem } from "./ComputerTabletRecordsListItem";
import { MobileRecordsListItem } from "./MobileRecordsListItem";
const appName = "UserDashboard.records";

const languageOptions = [
  { key: "docs", text: <a href="/docs/_new">New doc</a>, value: "docs" },
  {
    key: "communities",
    text: <a href="/communities/new">New comm</a>,
    value: "communities",
  },
];

const extractAbstract = (abstract) => {
  if (!abstract) return i18next.t("No description");
  let abstractText =
    abstract?.find((a) => a.lang === i18next.language)?.value ||
    abstract[0]?.value;
  return _truncate(abstractText, { length: 350 });
};
export const UserDashboardRecordsListItem = ({ result }) => {
  const uiMetadata = {
    title: _get(result, "metadata.title", i18next.t("No title")),
    abstract: extractAbstract(_get(result, "metadata.abstract", undefined)),
    resourceType: _get(result, "metadata.resourceType", ""),
    accessRights: _get(result, "metadata.accessRights", ""),
    createdDate: _get(result, "created"),
    viewLink: _get(result, "links.self_html"),
  };

  return (
    <React.Fragment>
      <ComputerTabletRecordsListItem result={result} uiMetadata={uiMetadata} />
      <MobileRecordsListItem result={result} uiMetadata={uiMetadata} />
    </React.Fragment>
  );
};

const UserDashboardSearchAppResultViewWAppName = parametrize(
  UserDashboardSearchAppResultView,
  {
    appName: appName,
  }
);

const ExtraContent = (
  <Grid.Column textAlign="right">
    <Dropdown
      button
      className="icon"
      floating
      labeled
      icon="plus"
      options={languageOptions}
      text={i18next.t("Create new...")}
    />
  </Grid.Column>
);

export const DashboardUploadsSearchLayout = UserDashboardSearchAppLayoutHOC({
  placeholder: i18next.t("Search in my uploads..."),
  extraContent: ExtraContent,
  appName: appName,
});
export const defaultComponents = {
  [`${appName}.ActiveFilters.element`]: ActiveFiltersElement,

  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]:
    BucketAggregationValuesElement,
  [`${appName}.SearchApp.resultOptions`]: SearchAppResultOptions,
  [`${appName}.EmptyResults.element`]: EmptyResultsElement,
  [`${appName}.ResultsList.item`]: UserDashboardRecordsListItem,
  // [`${appName}.SearchApp.facets`]: ContribSearchAppFacetsWithConfig,
  [`${appName}.SearchApp.results`]: UserDashboardSearchAppResultViewWAppName,
  [`${appName}.SearchBar.element`]: SearchappSearchbarElement,
  [`${appName}.SearchApp.layout`]: DashboardUploadsSearchLayout,
  [`${appName}.SearchApp.sort`]: SearchAppSort,
};

const overriddenComponents = overrideStore.getAll();

createSearchAppInit(
  { ...defaultComponents, ...overriddenComponents },
  true,
  "invenio-search-config",
  true
);

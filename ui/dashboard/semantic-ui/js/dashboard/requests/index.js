import React from "react";
import { Button } from "semantic-ui-react";
import { parametrize, overrideStore } from "react-overridable";
import { createSearchAppInit } from "@js/invenio_search_ui";
import {
  ActiveFiltersElement,
  BucketAggregationElement,
  SearchAppResultOptions,
  SearchAppSort,
  SearchappSearchbarElement,
  BucketAggregationValuesElement,
} from "@js/oarepo_ui/search";

import { UserDashboardSearchAppLayoutHOC } from "../components/UserDashboardSearchAppLayout";
import { UserDashboardSearchAppResultView } from "../components/UserDashboardSearchAppResultView";
import { i18next } from "@translations/i18next";
// import { ComputerTabletUploadsItem } from "../components/resultitems/uploads/ComputerTabletUploadsItem";
// import { MobileUploadsItem } from "../components/resultitems/uploads/MobileUploadsItem";
const appName = "UserDashboard.requests";

const ResultListItem = ({ result }) => {
  return <div>{result?.id}</div>;
};

// export const UserDashboardResultListItem = ({ result }) => {
//   const uiMetadata = {
//     title: _get(result, "metadata.title", i18next.t("No title")),
//     // abstract: _get(result, "metadata.abstract", i18next.t("No abstract")),
//     resourceType: _get(
//       result,
//       "metadata.resourceType",
//       i18next.t("No resource type")
//     ),
//     createdDate: _get(result, "created"),
//     viewLink: _get(result, "links.self_html"),
//   };

//   return (
//     <React.Fragment>
//       <MobileUploadsItem result={result} uiMetadata={uiMetadata} />
//       <ComputerTabletUploadsItem result={result} uiMetadata={uiMetadata} />
//     </React.Fragment>
//   );
// };

const UserDashboardSearchAppResultViewWAppName = parametrize(
  UserDashboardSearchAppResultView,
  {
    appName: appName,
  }
);

export const DashboardUploadsSearchLayout = UserDashboardSearchAppLayoutHOC({
  searchBarPlaceholder: i18next.t("Search in my uploads..."),
  newBtn: (
    <Button
      positive
      icon="upload"
      href="/docs/_new"
      content={i18next.t("New upload")}
      floated="right"
    />
  ),
  appName: appName,
});
export const defaultComponents = {
  [`${appName}.ActiveFilters.element`]: ActiveFiltersElement,

  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]:
    BucketAggregationValuesElement,
  [`${appName}.SearchApp.resultOptions`]: SearchAppResultOptions,
  // [`${appName}.EmptyResults.element`]: RDMEmptyResults,
  [`${appName}.ResultsList.item`]: ResultListItem,
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

import React from "react";
import { Button, Grid } from "semantic-ui-react";
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
import { withState } from "react-searchkit";
import {
  MobileRequestItem,
  ComputerTabletRequestItem,
  RequestsSearchLayout,
  RequestsEmptyResultsWithState,
  RequestsResults,
} from "@js/invenio_requests/search";

import { UserDashboardSearchAppLayoutHOC } from "../components/UserDashboardSearchAppLayout";
import { UserDashboardSearchAppResultView } from "../components/UserDashboardSearchAppResultView";
import { i18next } from "@translations/i18next";
import { FacetsButtonGroup } from "./FacetsButtonGroup";
// import { ComputerTabletUploadsItem } from "../components/resultitems/uploads/ComputerTabletUploadsItem";
// import { MobileUploadsItem } from "../components/resultitems/uploads/MobileUploadsItem";
const appName = "UserDashboard.requests";

const ResultListItem = ({ result }) => {
  return <div>{result?.id}</div>;
};

export function RequestsResultsItemTemplateDashboard({ result }) {
  const ComputerTabletRequestsItemWithState = withState(
    ComputerTabletRequestItem
  );
  const MobileRequestsItemWithState = withState(MobileRequestItem);
  const detailsURL = `/me/requests/${result.id}`;
  return (
    <>
      <ComputerTabletRequestsItemWithState
        result={result}
        detailsURL={detailsURL}
      />
      <MobileRequestsItemWithState result={result} detailsURL={detailsURL} />
    </>
  );
}
export const ExtraContent = ({
  currentResultsState,
  currentQueryState,
  updateQueryState,
}) => {
  console.log(currentQueryState);
  return (
    <Grid.Column>
      <FacetsButtonGroup keyName="is_open" />
      <span className="rel-ml-2"></span>
      <div className="mobile only rel-mb-1"></div>
      <Button.Group size="mini">
        <Button active size="mini">
          {i18next.t("My")}
        </Button>
        <Button size="mini">{i18next.t("Others")}</Button>
      </Button.Group>
    </Grid.Column>
  );
};
console.log(typeof ExtraContent);
const ExtraContentWithState = withState(ExtraContent);
const test = () => <ExtraContentWithState />;

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
  placeholder: i18next.t("Search in my requests..."),
  extraContent: test,
  appName: appName,
});
export const defaultComponents = {
  [`${appName}.ActiveFilters.element`]: ActiveFiltersElement,

  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]:
    BucketAggregationValuesElement,
  [`${appName}.SearchApp.resultOptions`]: SearchAppResultOptions,
  // [`${appName}.EmptyResults.element`]: RDMEmptyResults,
  [`${appName}.ResultsList.item`]: RequestsResultsItemTemplateDashboard,
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

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
import { RequestsEmptyResultsWithState } from "@js/invenio_requests/search";
import { defaultContribComponents } from "@js/invenio_requests/contrib";

import { UserDashboardSearchAppLayoutHOC } from "../components/UserDashboardSearchAppLayout";
import { UserDashboardSearchAppResultView } from "../components/UserDashboardSearchAppResultView";
import { i18next } from "@translations/i18next";
import { FacetsButtonGroup } from "./FacetsButtonGroup";
import { ComputerTabletRequestsListItem } from "./ComputerTabletRequestsListItem";
import { MobileRequestsListItem } from "./MobileRequestsListItem";

const appName = "UserDashboard.requests";

export function RequestsResultsItemTemplateDashboard({ result }) {
  const ComputerTabletRequestsItemWithState = withState(
    ComputerTabletRequestsListItem
  );
  const MobileRequestsItemWithState = withState(MobileRequestsListItem);
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
const ExtraContentWithState = withState(ExtraContent);
const test = () => <ExtraContentWithState />;

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
  [`${appName}.EmptyResults.element`]: RequestsEmptyResultsWithState,
  [`${appName}.ResultsList.item`]: RequestsResultsItemTemplateDashboard,
  // [`${appName}.SearchApp.facets`]: ContribSearchAppFacetsWithConfig,
  [`${appName}.SearchApp.results`]: UserDashboardSearchAppResultViewWAppName,
  [`${appName}.SearchBar.element`]: SearchappSearchbarElement,
  [`${appName}.SearchApp.layout`]: DashboardUploadsSearchLayout,
  [`${appName}.SearchApp.sort`]: SearchAppSort,
  ...defaultContribComponents,
};

const overriddenComponents = overrideStore.getAll();

createSearchAppInit(
  { ...defaultComponents, ...overriddenComponents },
  true,
  "invenio-search-config",
  true
);

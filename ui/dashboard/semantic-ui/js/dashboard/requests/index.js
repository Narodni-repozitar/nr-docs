import React from "react";
import { Button, Grid, Icon } from "semantic-ui-react";
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
import { PropTypes } from "prop-types";
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

RequestsResultsItemTemplateDashboard.propTypes = {
  result: PropTypes.object.isRequired,
};

export const FacetButtons = (
  <React.Fragment>
    <Grid.Column only="computer" textAlign="right">
      <Button size="mini" primary className="rel-mr-2">
        <Icon name="plus" />

        {i18next.t("New request")}
      </Button>
      <FacetsButtonGroup keyName="is_open" />
      <span className="rel-ml-2"></span>
      <FacetsButtonGroup
        keyName="is_mine"
        trueButtonText={i18next.t("My")}
        falseButtonText={i18next.t("Others")}
      />
    </Grid.Column>
    <Grid.Column only="tablet" textAlign="left">
      <Button size="mini" primary>
        <Icon name="plus" />
        {i18next.t("New request")}
      </Button>
    </Grid.Column>
    <Grid.Column only="mobile tablet" textAlign="left">
      <FacetsButtonGroup keyName="is_open" />
    </Grid.Column>
    <Grid.Column only="mobile tablet" textAlign="right">
      <FacetsButtonGroup
        keyName="is_mine"
        trueButtonText={i18next.t("My")}
        falseButtonText={i18next.t("Others")}
      />
    </Grid.Column>
  </React.Fragment>
);

const UserDashboardSearchAppResultViewWAppName = parametrize(
  UserDashboardSearchAppResultView,
  {
    appName: appName,
  }
);

export const DashboardUploadsSearchLayout = UserDashboardSearchAppLayoutHOC({
  placeholder: i18next.t("Search in my requests..."),
  extraContent: FacetButtons,
  appName: appName,
  extraRow: (
    <Grid.Column>
      <Button fluid size="mini" primary>
        <Icon name="plus" />
        {i18next.t("New request")}
      </Button>
    </Grid.Column>
  ),
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

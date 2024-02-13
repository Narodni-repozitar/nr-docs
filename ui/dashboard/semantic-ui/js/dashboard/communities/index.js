import React from "react";
import { parametrize, overrideStore } from "react-overridable";
import { createSearchAppInit } from "@js/invenio_search_ui";
import {
  ActiveFiltersElement,
  BucketAggregationElement,
  BucketAggregationValuesElement,
  SearchAppResultOptions,
  SearchAppSort,
  SearchappSearchbarElement,
  ErrorElement,
} from "@js/oarepo_ui/search";
// TODO: if we wish to import some things from invenio we need to resolve translations
// in their system
import { CommunitiesEmptySearchResults } from "@js/invenio_communities/community";
import PropTypes from "prop-types";
import { ComputerTabledCommunitiesListItem } from "./ComputerTabletCommunitiesListItem";
import { MobileCommunitiesListItem } from "./MobileCommunitiesListItem";
import { UserDashboardSearchAppLayoutHOC } from "../components/UserDashboardSearchAppLayout";
import { UserDashboardSearchAppResultView } from "../components/UserDashboardSearchAppResultView";
import { i18next } from "@translations/i18next";
const appName = "UserDashboard.communities";

export const UserDashboardCommunitiesListItem = ({
  result,
  communityTypeLabelTransparent,
}) => {
  const isRestricted = result?.access?.visibility === "restricted";
  return (
    <React.Fragment>
      <ComputerTabledCommunitiesListItem
        result={result}
        communityTypeLabelTransparent={communityTypeLabelTransparent}
        isRestricted={isRestricted}
      />
      <MobileCommunitiesListItem
        result={result}
        communityTypeLabelTransparent={communityTypeLabelTransparent}
        isRestricted={isRestricted}
      />
    </React.Fragment>
  );
};

UserDashboardCommunitiesListItem.propTypes = {
  result: PropTypes.object.isRequired,
  communityTypeLabelTransparent: PropTypes.bool,
};

UserDashboardCommunitiesListItem.defaultProps = {
  communityTypeLabelTransparent: false,
};

const UserDashboardSearchAppResultViewWAppName = parametrize(
  UserDashboardSearchAppResultView,
  {
    appName: appName,
  }
);

export const DashboardUploadsSearchLayout = UserDashboardSearchAppLayoutHOC({
  placeholder: i18next.t("Search in my communities..."),
  extraContent: () => null,
  appName: appName,
});
export const defaultComponents = {
  [`${appName}.ActiveFilters.element`]: ActiveFiltersElement,

  [`${appName}.BucketAggregation.element`]: BucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]:
    BucketAggregationValuesElement,
  [`${appName}.SearchApp.resultOptions`]: SearchAppResultOptions,
  [`${appName}.EmptyResults.element`]: CommunitiesEmptySearchResults,
  [`${appName}.ResultsList.item`]: UserDashboardCommunitiesListItem,
  // [`${appName}.SearchApp.facets`]: ContribSearchAppFacetsWithConfig,
  [`${appName}.SearchApp.results`]: UserDashboardSearchAppResultViewWAppName,
  [`${appName}.Error.element`]: ErrorElement,
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

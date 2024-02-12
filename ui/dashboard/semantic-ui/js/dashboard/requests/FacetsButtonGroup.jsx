import React from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/i18next";
import { Button } from "semantic-ui-react";
import { withState } from "react-searchkit";

const FacetsButtonGroupComponent = ({
  currentQueryState,
  updateQueryState,
  keyName,
}) => {
  const currentFilter = currentQueryState.filters?.find(
    (f) => f[0] === keyName
  );
  if (!currentFilter)
    console.error("FacetsButtonGroup: No current filter found");
  const currentStatus = JSON.parse(currentFilter?.[1]);
  const handleFilterChange = (status) => {
    if (currentStatus === status) return;
    currentQueryState.filters = currentQueryState.filters.filter(
      (element) => element[0] !== keyName
    );
    currentQueryState.filters.push([keyName, status]);
    updateQueryState(currentQueryState);
  };
  return (
    <Button.Group size="mini" className="rel-mb-1">
      <Button
        onClick={() => handleFilterChange(true)}
        className="request-search-filter"
        active={currentStatus}
      >
        {i18next.t("Open")}
      </Button>
      <Button
        onClick={() => handleFilterChange(false)}
        className="request-search-filter"
        active={!currentStatus}
      >
        {i18next.t("Closed")}
      </Button>
    </Button.Group>
  );
};

FacetsButtonGroupComponent.propTypes = {
  currentResultsState: PropTypes.object.isRequired,
  currentQueryState: PropTypes.object.isRequired,
  updateQueryState: PropTypes.func.isRequired,
  keyName: PropTypes.string.isRequired,
};

export const FacetsButtonGroup = withState(FacetsButtonGroupComponent);

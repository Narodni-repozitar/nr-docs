import React, { useContext } from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/i18next";
import { Button } from "semantic-ui-react";
import { withState } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";

const FacetsButtonGroupComponent = ({
  currentResultsState,
  currentQueryState,
  updateQueryState,
  keyName,
  trueButtonText,
  falseButtonText,
  ...uiProps
}) => {
  const { initialQueryState } = useContext(SearchConfigurationContext);
  const currentFilter = currentQueryState.filters?.find(
    (f) => f[0] === keyName
  );
  if (!currentFilter)
    console.error("FacetsButtonGroup: Facet name not provided");
  const currentStatus = JSON.parse(currentFilter?.[1]);
  const handleFilterChange = (status) => {
    if (currentStatus === status) return;
    currentQueryState.filters = currentQueryState?.filters?.filter(
      (f) => f[0] !== keyName 
    );
    currentQueryState.filters.push([keyName, status]);
    updateQueryState(currentQueryState);
  };
  return (
    <Button.Group size="mini" className="rel-mb-1" {...uiProps}>
      <Button
        onClick={() => handleFilterChange(true)}
        className="request-search-filter"
        active={currentStatus}
      >
        {trueButtonText}
      </Button>
      <Button
        onClick={() => handleFilterChange(false)}
        className="request-search-filter"
        active={!currentStatus}
      >
        {falseButtonText}
      </Button>
    </Button.Group>
  );
};

FacetsButtonGroupComponent.propTypes = {
  currentQueryState: PropTypes.object.isRequired,
  updateQueryState: PropTypes.func.isRequired,
  currentResultsState: PropTypes.object.isRequired,
  keyName: PropTypes.string.isRequired,
  trueButtonText: PropTypes.string,
  falseButtonText: PropTypes.string,
};
FacetsButtonGroupComponent.defaultProps = {
  trueButtonText: i18next.t("Open"),
  falseButtonText: i18next.t("Closed"),
};
export const FacetsButtonGroup = withState(FacetsButtonGroupComponent);

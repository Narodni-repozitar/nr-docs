import React from "react";
import PropTypes from "prop-types";

export const SearchFiltersToggleElement = ({
  updateQueryFilters,
  userSelectionFilters,
  filterValue,
  label,
  title,
}) => {
  const _isChecked = (userSelectionFilters) => {
    const isFilterActive =
      userSelectionFilters.filter((filter) => filter[0] === filterValue[0])
        .length > 0;
    return isFilterActive;
  };

  const onToggleClicked = () => {
    updateQueryFilters(filterValue);
  };

  const isChecked = _isChecked(userSelectionFilters);
  return (
    <Card className="shadowless borderless facet">
      <Card.Content>
        <Card.Header as="h2">{title}</Card.Header>
      </Card.Content>
      <Card.Content>
        <Checkbox
          toggle
          label={label}
          name="toggle"
          id="toggle"
          onClick={onToggleClicked}
          checked={isChecked}
        />
      </Card.Content>
    </Card>
  );
};

SearchFiltersToggleElement.propTypes = {
  title: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  filterValue: PropTypes.array.isRequired,
  userSelectionFilters: PropTypes.array.isRequired,
  updateQueryFilters: PropTypes.func.isRequired,
};

import React from "react";
import { Label, Icon } from "semantic-ui-react";

export const ActiveFiltersElement = ({
  filters,
  removeActiveFilter,
  getLabel,
}) => (
  <Label.Group color="blue">
    {filters.map((filter, index) => {
      const { label, activeFilter } = getLabel(filter);
      return (
        // eslint-disable-next-line react/no-array-index-key
        <Label
          key={activeFilter}
          onClick={() => removeActiveFilter(activeFilter)}
        >
          <Icon name="filter" />
          {label}
          <Icon name="delete" />
        </Label>
      );
    })}
  </Label.Group>
);

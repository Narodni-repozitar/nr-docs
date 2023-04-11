import React from "react";
import { Label, Icon } from "semantic-ui-react";

export const ResultsItemAccessStatus = ({ status }) => {
  return (
    <Label size="tiny" className={`access-status ${status}`}>
      {status.icon && <Icon name={status} />}
      {status}
    </Label>
  );
};

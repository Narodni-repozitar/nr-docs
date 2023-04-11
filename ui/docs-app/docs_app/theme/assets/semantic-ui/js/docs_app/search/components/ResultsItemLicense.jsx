import React from "react";
import { Label, Icon } from "semantic-ui-react";

export const ResultsItemLicense = ({ rights = [] }) => {
  return rights.map(({ id, title }) => (
    <Label key={id} size="tiny" className={`license-rights ${id}`}>
      {title}
    </Label>
  ));
};

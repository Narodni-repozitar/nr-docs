import React from "react";
import { Sort } from "react-searchkit";

import { i18next } from "@translations/oarepo_ui/i18next";

const renderLabel = (cmp) => (
  <>
    <label className="mr-10">{i18next.t("Sort by")}</label>
    {cmp}
  </>
);

export const SearchAppSort = ({ options }) => {
  return (
    <Sort
      sortOrderDisabled
      values={options}
      ariaLabel={i18next.t("Sort")}
      label={renderLabel}
    />
  );
};

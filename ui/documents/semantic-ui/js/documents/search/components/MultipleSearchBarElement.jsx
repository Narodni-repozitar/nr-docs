import React from "react";
import { MultipleOptionsSearchBarRSK } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/i18next";

export const MultipleSearchBarElement = ({ queryString, onInputChange }) => {
  const headerSearchbar = document.getElementById("header-search-bar");
  const searchbarOptions = JSON.parse(headerSearchbar.dataset.options);

  return (
    <MultipleOptionsSearchBarRSK
      options={searchbarOptions}
      onInputChange={onInputChange}
      queryString={queryString}
      placeholder={`${i18next.t("Search")}...`}
    />
  );
};

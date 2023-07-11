import React from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

import { SearchBar } from "@js/invenio_search_ui/components";
import { buildUID } from "react-searchkit";

export const SearchAppSearchbarContainer = ({ appName }) => {
  return (
    <Overridable id={buildUID("SearchApp.searchbar", "", appName)}>
      <SearchBar buildUID={buildUID} />
    </Overridable>
  );
};

SearchAppSearchbarContainer.propTypes = {
  appName: PropTypes.string.isRequired,
};

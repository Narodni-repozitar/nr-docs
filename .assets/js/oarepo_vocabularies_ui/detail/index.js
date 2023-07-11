import React from "react";
import ReactDOM from "react-dom";
import _ from "lodash";
import { App } from "./DetailSearchApp";

document.addEventListener("DOMContentLoaded", function () {
  const searchAppElement = document.querySelectorAll(
    `[data-invenio-search-config]`
  )[0];

  const initialAppConfig = JSON.parse(
    searchAppElement.dataset[_.camelCase("invenio-search-config")]
  );

  ReactDOM.render(<App appConfig={initialAppConfig} />, searchAppElement);
});

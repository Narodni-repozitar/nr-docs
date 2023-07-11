import React from "react";
import { BucketAggregation } from "react-searchkit";
import { i18next } from "@translations/oarepo_ui/i18next";

export const SearchAppFacets = ({ aggs, appName }) => {
  return (
    <div className="facets-container">
      <div className="facets-header">
        <h2>{i18next.t("Filters")}</h2>
        <div className="ui divider"></div>
      </div>
      <div className="vertical scroll facet-list">
        {aggs.map((agg) => (
          <BucketAggregation key={agg.aggName} title={agg.title} agg={agg} />
        ))}
      </div>
    </div>
  );
};

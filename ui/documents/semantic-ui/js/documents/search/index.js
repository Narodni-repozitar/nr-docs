import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
  HistogramWSlider,
} from "@js/oarepo_ui";

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export const componentOverrides = {
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
  [`${overridableIdPrefix}.BucketAggregation.element.date_issued_histogram`]:
    HistogramWSlider,
};

createSearchAppsInit({ componentOverrides });

import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
  HistogramWSlider,
} from "@js/oarepo_ui";

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export const componentOverrides = {
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
  [`${overridableIdPrefix}.BucketAggregation.element.syntheticFields_year`]:
    HistogramWSlider,
};

createSearchAppsInit({ componentOverrides });

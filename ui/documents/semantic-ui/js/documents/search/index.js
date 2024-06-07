import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
  FoldableBucketAggregationElement,
} from "@js/oarepo_ui";

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export const componentOverrides = {
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
  [`${overridableIdPrefix}.BucketAggregation.element`]:
    FoldableBucketAggregationElement,
};

createSearchAppsInit({ componentOverrides });

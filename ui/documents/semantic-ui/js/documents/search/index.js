import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
  HistogramWSlider,
} from "@js/oarepo_ui";
import { parametrize } from "react-overridable";

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export const componentOverrides = {
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
  [`${overridableIdPrefix}.BucketAggregation.element.date_issued_histogram`]:
    parametrize(HistogramWSlider, {
      minDateAggName: "date_issued_min",
      maxDateAggName: "date_issued_max",
    }),
};

createSearchAppsInit({ componentOverrides });

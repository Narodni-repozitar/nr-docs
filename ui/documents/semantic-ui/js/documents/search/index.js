import {
  parseSearchAppConfigs,
  createSearchAppsInit,
  HistogramWSlider,
} from "@js/oarepo_ui/search";
import { parametrize } from "react-overridable";
import ResultsListItem from "./ResultsListItem";
import { SearchAppFacets } from "@js/oarepo_ui/search/SearchAppFacets";

const SearchAppFacetsWithProps = parametrize(SearchAppFacets, {
  allVersionsToggle: true,
});

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export const componentOverrides = {
  [`${overridableIdPrefix}.SearchApp.facets`]: SearchAppFacetsWithProps,
  [`${overridableIdPrefix}.ResultsList.item`]: ResultsListItem,
  [`${overridableIdPrefix}.BucketAggregation.element.syntheticFields_year`]:
    HistogramWSlider,
};

createSearchAppsInit({ componentOverrides });

import {
  createSearchAppsInit,
} from "@js/oarepo_ui/search";
import { overrideStore, parametrize } from 'react-overridable';
import { SearchAppFacets } from '@js/oarepo_ui/search/SearchAppFacets';
import DocumentsResultsListItem from './ResultsListItem';

const SearchAppFacetsWithProps = parametrize(SearchAppFacets, { allVersionsToggle: true });

overrideStore.add('Documents.Search.SearchApp.facets', SearchAppFacetsWithProps);
overrideStore.add('Documents.Search.ResultsList.item', DocumentsResultsListItem);

createSearchAppsInit();

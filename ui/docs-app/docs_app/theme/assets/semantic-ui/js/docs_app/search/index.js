import { createSearchAppInit } from '@js/invenio_search_ui'
import {
  RDMCountComponent,
  RDMEmptyResults,
  RDMErrorComponent,
  RDMRecordResultsGridItem,
  RDMRecordResultsListItemWithState,
  RDMRecordSearchBarContainer,
  RDMRecordMultipleSearchBarElement,
  RDMToggleComponent,
} from './components'
import { parametrize, overrideStore } from 'react-overridable'
import {
  ContribSearchAppFacets,
  ContribBucketAggregationElement,
  ContribBucketAggregationValuesElement,
} from '@js/invenio_search_ui/components'

const ContribSearchAppFacetsWithConfig = parametrize(ContribSearchAppFacets, {
  toogle: true,
})

const appName = 'DocsApp.Search'

const RDMRecordSearchBarContainerWithConfig = parametrize(
  RDMRecordSearchBarContainer,
  {
    appName: appName,
  },
)

const RDMRecordResultsListItemWithConfig = parametrize(
  RDMRecordResultsListItemWithState,
  {
    appName: appName,
  },
)

export const defaultComponents = {
  [`${appName}.BucketAggregation.element`]: ContribBucketAggregationElement,
  [`${appName}.BucketAggregationValues.element`]: ContribBucketAggregationValuesElement,
  [`${appName}.ResultsGrid.item`]: RDMRecordResultsGridItem,
  [`${appName}.EmptyResults.element`]: RDMEmptyResults,
  [`${appName}.ResultsList.item`]: RDMRecordResultsListItemWithConfig,
  [`${appName}.SearchApp.facets`]: ContribSearchAppFacetsWithConfig,
  [`${appName}.SearchApp.searchbarContainer`]: RDMRecordSearchBarContainerWithConfig,
  //   [`${appName}.SearchBar.element`]: RDMRecordMultipleSearchBarElement,
  [`${appName}.Count.element`]: RDMCountComponent,
  [`${appName}.Error.element`]: RDMErrorComponent,
  [`${appName}.SearchFilters.Toggle.element`]: RDMToggleComponent,
}

const overriddenComponents = overrideStore.getAll()

createSearchAppInit(
  { ...defaultComponents, ...overriddenComponents },
  true,
  'invenio-search-config',
  true,
)

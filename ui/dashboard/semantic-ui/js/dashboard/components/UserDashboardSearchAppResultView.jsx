// This file is part of InvenioRDM
// Copyright (C) 2020-2022 CERN.
// Copyright (C) 2020-2021 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
// Copyright (C) 2021 New York University.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import {
  SearchAppResultsPane,
  InvenioSearchPagination,
} from "@js/invenio_search_ui/components";
import { i18next } from "@translations/i18next";
import React from "react";
import {
  Count,
  ResultsList,
  SearchBar,
  Sort,
  buildUID,
  Pagination,
  ResultsPerPage,
} from "react-searchkit";
import { GridResponsiveSidebarColumn } from "react-invenio-forms";
import { Grid, Segment, Button } from "semantic-ui-react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import {
  SearchAppFacets,
  ResultCount,
  SearchAppSort,
  ResultsPerPageLabel,
} from "@js/oarepo_ui";

export function UserDashboardSearchAppResultView(props) {
  const { sortOptions, paginationOptions, currentResultsState, appName } =
    props;
  console.log(sortOptions);
  const { total } = currentResultsState.data;
  const { resultsPerPage } = paginationOptions;
  return (
    total && (
      <Grid className="rel-mb-2">
        <Grid.Row>
          <Grid.Column width={16}>
            <Grid>
              <Overridable
                id={buildUID("ResultView.resultHeader", "", appName)}
                sortOptions={sortOptions}
                paginationOptions={paginationOptions}
                currentResultsState={currentResultsState}
                appName={appName}
              >
                <Grid.Row
                  verticalAlign="middle"
                  className="small pt-5 pb-5 highlight-background"
                >
                  <Grid.Column width={4}>
                    <ResultCount currentResultsState={currentResultsState} />
                  </Grid.Column>
                  <Grid.Column
                    width={12}
                    textAlign="right"
                    className="padding-r-5"
                  >
                    {/* {sortOptions.length > 0 && (
                      <SearchAppSort options={sortOptions} />
                    )} */}
                  </Grid.Column>
                </Grid.Row>
              </Overridable>
              <Overridable
                id={buildUID("ResultView.resultList", "", appName)}
                sortOptions={sortOptions}
                paginationOptions={paginationOptions}
                currentResultsState={currentResultsState}
                appName={appName}
              >
                <Grid.Row>
                  <Grid.Column>
                    <ResultsList />
                  </Grid.Column>
                </Grid.Row>
              </Overridable>
            </Grid>
          </Grid.Column>
        </Grid.Row>
        <Overridable
          id={buildUID("ResultView.resultFooter", "", appName)}
          sortOptions={sortOptions}
          paginationOptions={paginationOptions}
          currentResultsState={currentResultsState}
          appName={appName}
        >
          {total > 10 && (
            <Grid.Row verticalAlign="middle">
              <Grid.Column
                className="computer tablet only"
                width={4}
              ></Grid.Column>
              <Grid.Column
                className="computer tablet only"
                width={8}
                textAlign="center"
              >
                <Pagination
                  options={{
                    size: "mini",
                    showFirst: false,
                    showLast: false,
                  }}
                />
              </Grid.Column>
              <Grid.Column
                className="mobile only"
                width={16}
                textAlign="center"
              >
                <Pagination
                  options={{
                    size: "mini",
                    boundaryRangeCount: 0,
                    showFirst: false,
                    showLast: false,
                  }}
                />
              </Grid.Column>
              <Grid.Column
                className="computer tablet only "
                textAlign="right"
                width={4}
              >
                <ResultsPerPage
                  values={resultsPerPage}
                  label={ResultsPerPageLabel}
                />
              </Grid.Column>
              <Grid.Column
                className="mobile only mt-10"
                textAlign="center"
                width={16}
              >
                <ResultsPerPage
                  values={resultsPerPage}
                  label={ResultsPerPageLabel}
                />
              </Grid.Column>
            </Grid.Row>
          )}
        </Overridable>
      </Grid>
    )
  );
}

UserDashboardSearchAppResultView.propTypes = {
  sortOptions: PropTypes.array.isRequired,
  paginationOptions: PropTypes.object.isRequired,
  currentResultsState: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

UserDashboardSearchAppResultView.defaultProps = {
  appName: "",
};

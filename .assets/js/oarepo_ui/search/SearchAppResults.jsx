import React from "react";
import { Grid } from "semantic-ui-react";
import {
  ResultsList,
  Pagination,
  ResultsPerPage,
  ResultsMultiLayout,
} from "react-searchkit";
import { i18next } from "@translations/oarepo_ui/i18next";

const resultsPerPageLabel = (cmp) => (
  <>
    {cmp} {i18next.t("resultsPerPage")}
  </>
);

export const SearchAppResults = ({ paginationOptions, layoutOptions }) => {
  const { resultsPerPage } = paginationOptions;
  const multipleLayouts = layoutOptions.listView && layoutOptions.gridView;
  const listOrGridView = layoutOptions.listView ? (
    <ResultsList />
  ) : (
    <ResultsGrid />
  );

  return (
    <Grid relaxed>
      <Grid.Row>
        <Grid.Column>
          {multipleLayouts ? <ResultsMultiLayout /> : listOrGridView}
        </Grid.Column>
      </Grid.Row>
      <Grid.Row verticalAlign="middle">
        <Grid.Column className="computer tablet only" width={4}></Grid.Column>
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
        <Grid.Column className="mobile only" width={16} textAlign="center">
          <Pagination
            options={{
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
          <ResultsPerPage values={resultsPerPage} label={resultsPerPageLabel} />
        </Grid.Column>
        <Grid.Column
          className="mobile only mt-10"
          textAlign="center"
          width={16}
        >
          <ResultsPerPage values={resultsPerPage} label={resultsPerPageLabel} />
        </Grid.Column>
      </Grid.Row>
    </Grid>
  );
};

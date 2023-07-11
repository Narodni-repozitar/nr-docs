import React, { useState } from "react";
import PropTypes from "prop-types";
import { OverridableContext } from "react-overridable";
import { Container, Grid, Button, Icon, Label } from "semantic-ui-react";
import {
  EmptyResults,
  Error,
  ReactSearchKit,
  ResultsLoader,
  withState,
  InvenioSearchApi,
} from "react-searchkit";
import { Results } from "./Results";
import { VocabularyResultsListItemWithState } from "../search/components";
import { i18next } from "@translations/oarepo_ui/i18next";

const OnResults = withState(Results);

const CountElement = ({ totalResults }) => {
  return (
    <Label size="large">
      {i18next.t("totalDescendants", { count: totalResults })}
    </Label>
  );
};

const overriddenComponents = {
  "ResultsList.item": VocabularyResultsListItemWithState,
  "Count.element": CountElement,
};

const DescendantsButton = ({
  searchAppShown,
  setSearchAppShown,
  currentResultsState,
}) => (
  <Grid>
    {!!currentResultsState.data.total && (
      <Grid.Row>
        <Button
          onClick={() =>
            setSearchAppShown((prevSearchAppShown) => !prevSearchAppShown)
          }
        >
          {`${
            searchAppShown ? i18next.t("hide") : i18next.t("show")
          } ${i18next.t("descendants")}`}{" "}
          <Icon
            name={searchAppShown ? "angle double up" : "angle double down"}
          />
        </Button>
      </Grid.Row>
    )}
  </Grid>
);

const DescendantsButtonWithState = withState(DescendantsButton);
export const App = ({ appConfig }) => {
  const [searchAppShown, setSearchAppShown] = useState(false);
  const {
    searchApi,
    initialQueryState,
    defaultSortingOnEmptyQueryString,
    sortOptions,
    paginationOptions,
  } = appConfig;
  return (
    <React.Fragment>
      <OverridableContext.Provider value={overriddenComponents}>
        <ReactSearchKit
          searchApi={new InvenioSearchApi(searchApi)}
          initialQueryState={initialQueryState}
          urlHandlerApi={{ enabled: false }}
          defaultSortingOnEmptyQueryString={defaultSortingOnEmptyQueryString}
        >
          <Container>
            <Grid relaxed centered>
              <Grid.Row>
                <Grid.Column
                  floated="left"
                  width={4}
                  style={{ padding: "2em 2.5em" }}
                >
                  <DescendantsButtonWithState
                    searchAppShown={searchAppShown}
                    setSearchAppShown={setSearchAppShown}
                  />
                </Grid.Column>
              </Grid.Row>
              <Grid.Row>
                {searchAppShown && (
                  <Grid.Column width={16}>
                    <ResultsLoader>
                      <EmptyResults />
                      <Error />
                      <OnResults
                        sortValues={sortOptions}
                        resultsPerPageValues={paginationOptions.resultsPerPage}
                        currentFacet={initialQueryState.filters}
                      />
                    </ResultsLoader>
                  </Grid.Column>
                )}
              </Grid.Row>
            </Grid>
          </Container>
        </ReactSearchKit>
      </OverridableContext.Provider>
    </React.Fragment>
  );
};

App.propTypes = {
  appConfig: PropTypes.shape({
    searchApi: PropTypes.object.isRequired,
    initialQueryState: PropTypes.shape({
      queryString: PropTypes.string,
      suggestions: PropTypes.array,
      sortBy: PropTypes.string,
      sortOrder: PropTypes.string,
      page: PropTypes.number,
      size: PropTypes.number,
      filters: PropTypes.array,
      hiddenParams: PropTypes.array,
      layout: PropTypes.oneOf(["list", "grid"]),
    }),
    defaultSortingOnEmptyQueryString: PropTypes.shape({
      sortBy: PropTypes.string,
      sortOrder: PropTypes.string,
    }),
    sortOptions: PropTypes.arrayOf(PropTypes.object),
    paginationOptions: PropTypes.shape({
      defaultValue: PropTypes.number,
      resultsPerPage: PropTypes.array,
    }),
  }).isRequired,
};

// This file is part of Invenio-RDM-Records
// Copyright (C) 2020-2023 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
// Copyright (C) 2022 data-futures.org.
//
// Invenio-RDM-Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import { Button, Form, Grid, Header, Modal, Dropdown } from "semantic-ui-react";
import { Formik } from "formik";
import * as Yup from "yup";
import { i18next } from "@translations/docs_app/i18next";
import { SelectField, RemoteSelectField } from "react-invenio-forms";

import PropTypes from "prop-types";

import { OverridableContext } from "react-overridable";
import {
  EmptyResults,
  Error,
  ReactSearchKit,
  ResultsLoader,
  SearchBar,
  InvenioSearchApi,
  Pagination,
  ResultsPerPage,
  ResultsList,
  withState,
} from "react-searchkit";

class BStateLogger extends Component {
  render() {
    return (
      <>
        <div>
          Current query state{" "}
          <pre>{JSON.stringify(this.props.currentQueryState, null, 2)}</pre>
        </div>
        <div>
          Current results state{" "}
          <pre>{JSON.stringify(this.props.currentResultsState, null, 2)}</pre>
        </div>
      </>
    );
  }
}

const StateLogger = withState(BStateLogger);

const schemeOptions = [
  //   { value: "psh", text: "PSH" },
  //   { value: "czenas", text: "Czenas" },
  { value: "institutions", text: "institutions" },
  { value: "resource-types", text: "resource-types" },
];

const MyResultsListItem = ({ result, index }) => <div>{result.title.cs}</div>;
const overriddenComponents = { "ResultsList.item": MyResultsListItem };

export const SubjectsFieldModal = ({
  initialRelatedItem,
  initialAction,
  addLabel,
  editLabel,
  onRelatedItemChange,
  trigger,
  fieldPath,
  suggestionAPIHeaders,
  //   searchAppConfig,
  open,
  closeModal,
  openModal,
  subjectScheme,
  schemeOptions,
}) => {
  // const [open, setOpen] = React.useState(false);
  const [action, setAction] = React.useState(initialAction);
  const [saveAndContinueLabel, setSaveAndContinueLabel] = React.useState(
    i18next.t("Save and add another")
  );

  const searchConfig = {
    searchApi: {
      axios: {
        headers: suggestionAPIHeaders,
        url: `/api/vocabularies/${subjectScheme}`,
        withCredentials: false,
      },
    },
    initialQueryState: {
      //   queryString: this.state.searchQuery,
      size: 10,
    },
    paginationOptions: {
      defaultValue: 10,
      resultsPerPage: [
        { text: "10", value: 10 },
        { text: "20", value: 20 },
        { text: "50", value: 50 },
      ],
    },
    layoutOptions: {
      listView: true,
      gridView: false,
    },
  };
  const changeContent = () => {
    setSaveAndContinueLabel(i18next.t("Added"));
    setTimeout(() => {
      setSaveAndContinueLabel(i18next.t("Save and add another"));
    }, 1000);
  };
  const searchApi = new InvenioSearchApi(searchConfig.searchApi);
  console.log(searchApi);
  console.log("entire modal rerender");
  return (
    <Modal
      className="related-items-modal"
      size="large"
      centered={false}
      onOpen={() => openModal()}
      open={open}
      trigger={trigger}
      onClose={() => {
        closeModal();
      }}
      closeIcon
      closeOnDimmerClick={false}
    >
      <Modal.Header as="h6">
        <Grid>
          <Grid.Column floated="left" width={8}>
            <Header as="h2">
              {schemeOptions.find((o) => o.value === subjectScheme)?.text}
            </Header>
          </Grid.Column>
        </Grid>
      </Modal.Header>
      <Modal.Content>
        <OverridableContext.Provider value={overriddenComponents}>
          <ReactSearchKit
            searchApi={searchApi}
            searchOnInit={false}
            initialQueryState={searchConfig.initialQueryState}
            urlHandlerApi={{ enabled: false }}
          >
            <Grid>
              <Grid.Row>
                <Grid.Column width={16} floated="left" verticalAlign="middle">
                  <SearchBar
                    placeholder={i18next.t("search")}
                    autofocus
                    actionProps={{
                      icon: "search",
                      content: null,
                      className: "search",
                    }}
                  />
                </Grid.Column>
              </Grid.Row>
              <Grid.Row verticalAlign="middle">
                <Grid.Column>
                  <ResultsLoader>
                    <ResultsList />
                    <EmptyResults />
                    <Error />
                  </ResultsLoader>
                </Grid.Column>
              </Grid.Row>
              <Grid.Row verticalAlign="middle">
                <Grid.Column>
                  <Pagination options={{ size: "tiny" }} />
                </Grid.Column>

                <Grid.Column floated="right" width={3}>
                  <ResultsPerPage
                    values={searchConfig?.paginationOptions.resultsPerPage}
                    // label={ResultsPerPageLabel}
                  />
                </Grid.Column>
              </Grid.Row>
              <Grid.Row>
                <StateLogger />
              </Grid.Row>
            </Grid>
          </ReactSearchKit>
        </OverridableContext.Provider>
      </Modal.Content>
      <Modal.Actions>
        <Button
          name="cancel"
          onClick={() => {
            closeModal();
          }}
          icon="remove"
          content={i18next.t("Cancel")}
          floated="left"
        />

        <Button
          onClick={() => {
            setAction("saveAndContinue");
          }}
          primary
          icon="checkmark"
          content={saveAndContinueLabel}
        />
        <Button
          name="submit"
          type="submit"
          onClick={() => {
            setAction("saveAndClose");
          }}
          primary
          icon="checkmark"
          content={i18next.t("Save")}
        />
      </Modal.Actions>
    </Modal>
  );
};

SubjectsFieldModal.propTypes = {
  initialRelatedItem: PropTypes.object,
  initialAction: PropTypes.string.isRequired,
  addLabel: PropTypes.string,
  editLabel: PropTypes.string,
  onRelatedItemChange: PropTypes.func,
  trigger: PropTypes.node,
};

SubjectsFieldModal.defaultProps = {
  initialRelatedItem: {},
};

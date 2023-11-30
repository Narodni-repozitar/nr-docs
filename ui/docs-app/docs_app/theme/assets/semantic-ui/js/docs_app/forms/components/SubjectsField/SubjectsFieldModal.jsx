// This file is part of Invenio-RDM-Records
// Copyright (C) 2020-2023 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
// Copyright (C) 2022 data-futures.org.
//
// Invenio-RDM-Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import { Button, Grid, Header, Modal, Label } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import PropTypes from "prop-types";
import { EmptyResultsElement } from "@js/oarepo_ui/search";
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
} from "react-searchkit";
import { ResultsList } from "./ResultsList";

const overriddenComponents = {
  "EmptyResults.element": EmptyResultsElement,
};

export const SubjectsFieldModal = ({
  suggestionAPIHeaders,
  open,
  closeModal,
  openModal,
  subjectScheme,
  schemeOptions,
  externalSubjects,
  handleCheckboxChange,
  handleRemove,
  handleAddSubjects,
}) => {
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

  const searchApi = new InvenioSearchApi(searchConfig.searchApi);
  return (
    <Modal
      className="related-items-modal"
      size="large"
      centered={false}
      onOpen={() => openModal()}
      open={open}
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
                <Grid.Column textAlign="left">
                  <ResultsLoader>
                    <ResultsList
                      subjectScheme={subjectScheme}
                      externalSubjects={externalSubjects}
                      handleCheckboxChange={handleCheckboxChange}
                    />
                    <EmptyResults />
                    <Error />
                  </ResultsLoader>
                </Grid.Column>
              </Grid.Row>
              <Grid.Row verticalAlign="middle">
                <Grid.Column textAlign="center" width={13}>
                  <Pagination options={{ size: "mini" }} />
                </Grid.Column>

                <Grid.Column floated="right" width={3}>
                  <ResultsPerPage
                    values={searchConfig?.paginationOptions.resultsPerPage}
                    // label={ResultsPerPageLabel}
                  />
                </Grid.Column>
              </Grid.Row>
              {/* <Grid.Row>
                <StateLogger />
              </Grid.Row> */}
            </Grid>
          </ReactSearchKit>
        </OverridableContext.Provider>
        <Header as="h3" content={i18next.t("Selected subjects")} />
        <Label.Group>
          {externalSubjects[subjectScheme]?.map((externalSubject) => (
            <Label
              key={externalSubject.classificationCode}
              icon="close"
              onClick={() => handleRemove(externalSubject)}
              content={externalSubject?.subject[0]?.value}
            />
          ))}
        </Label.Group>
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
          name="submit"
          type="submit"
          onClick={() => {
            handleAddSubjects();
            closeModal();
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
  suggestionAPIHeaders: PropTypes.object.isRequired,
  open: PropTypes.bool.isRequired,
  closeModal: PropTypes.func.isRequired,
  openModal: PropTypes.func.isRequired,
  subjectScheme: PropTypes.string.isRequired,
  schemeOptions: PropTypes.array,
  externalSubjects: PropTypes.object,
  handleCheckboxChange: PropTypes.func.isRequired,
  handleRemove: PropTypes.func.isRequired,
  handleAddSubjects: PropTypes.func.isRequired,
};

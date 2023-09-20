// This file is part of Invenio-RDM-Records
// Copyright (C) 2020-2023 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
// Copyright (C) 2022 data-futures.org.
//
// Invenio-RDM-Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component, createRef } from "react";
import PropTypes from "prop-types";
import { Button, Form, Grid, Header, Modal } from "semantic-ui-react";
import { Formik } from "formik";
import {
  Image,
  TextField,
  RadioField,
  RemoteSelectField,
} from "react-invenio-forms";
import * as Yup from "yup";
import _get from "lodash/get";
import _find from "lodash/find";
import _isEmpty from "lodash/isEmpty";
import _map from "lodash/map";
import { CreatibutorsIdentifiers } from "./CreatibutorsIdentifiers";
import { CREATIBUTOR_TYPE } from "./type";
import { i18next } from "@translations/docs_app/i18next";
import { Trans } from "react-i18next";
import { VocabularySelectField } from "@js/oarepo_vocabularies";

const ModalActions = {
  ADD: "add",
  EDIT: "edit",
};

const NamesAutocompleteOptions = {
  SEARCH: "search",
  SEARCH_ONLY: "search_only",
  OFF: "off",
};


const findField = (arrayField, key, value) => {
  const knownField = _find(arrayField, {
    [key]: value,
  });
  return knownField ? knownField : { [key]: value };
};

const makeIdEntry = (identifier) => {
  let icon = null;
  let link = null;

  if (identifier.scheme === "orcid") {
    icon = "/static/images/orcid.svg";
    link = "https://orcid.org/" + identifier.identifier;
  } else if (identifier.scheme === "gnd") {
    icon = "/static/images/gnd-icon.svg";
    link = "https://d-nb.info/gnd/" + identifier.identifier;
  } else if (identifier.scheme === "ror") {
    icon = "/static/images/ror-icon.svg";
    link = "https://ror.org/" + identifier.identifier;
  } else {
    return (
      <>
        {identifier.scehme}: {identifier.identifier}
      </>
    );
  }

  return (
    <span key={identifier.identifier}>
      <a href={link} target="_blank" rel="noopener noreferrer">
        <Image
          src={icon}
          className="inline-id-icon ml-5 mr-5"
          verticalAlign="middle"
        />
        {identifier.identifier}
      </a>
    </span>
  )
}

/**
   * Function to transform formik creatibutor state
   * back to the external format.
   */
const serializeCreatibutor = (initialCreatibutor, submittedCreatibutor) => {
  console.log('serializeCreatibutor:', submittedCreatibutor)
  const fullName = `${submittedCreatibutor.family_name}, ${submittedCreatibutor.given_name}`
  const identifiersFieldPath = "authorityIdentifiers";
  const affiliationsFieldPath = "affiliations";
  // The modal is saving only identifiers values, thus
  // identifiers with existing scheme are trimmed
  // Here we merge back the known scheme for the submitted identifiers
  const initialIdentifiers = _get(initialCreatibutor, identifiersFieldPath, []);
  const submittedIdentifiers = _get(submittedCreatibutor, identifiersFieldPath, []);
  const identifiers = submittedIdentifiers.map((identifier) => {
    return findField(initialIdentifiers, "identifier", identifier);
  });

  const submittedAffiliations = _get(submittedCreatibutor, affiliationsFieldPath, []);
  return {
    ...submittedCreatibutor,
    fullName,
    ...identifiers,
    affiliations: submittedAffiliations,
  };
};


/**
   * Function to transform creatibutor object
   * to formik initialValues.
   */
const deserializeCreatibutor = (initialCreatibutor, isCreator) => {
  const identifiersFieldPath = "authorityIdentifiers";
  const [family_name = '', given_name = ''] = _get(initialCreatibutor, "fullName", "").trim().split(',', 1)
  const result = {
    // default type to personal
    nameType: CREATIBUTOR_TYPE.PERSON,
    family_name,
    given_name,
    ...initialCreatibutor,
    authorityIdentifiers: _map(
      _get(initialCreatibutor, identifiersFieldPath, []),
      "identifier"
    ),
    affiliations: _get(initialCreatibutor, "affiliations", []),
    ...(!isCreator && { role: _get(initialCreatibutor, "role", "") })
  };
  console.log('deserializeCreatibutor:', result)
  return result
};

const serializeSuggestions = (creatibutors) => {
  let results = creatibutors.map((creatibutor) => {
    let affNames = "";
    creatibutor.affiliations.forEach((affiliation, idx) => {
      affNames += affiliation.name;
      if (idx < creatibutor.affiliations.length - 1) {
        affNames += ", ";
      }
    });

    let idString = [];
    creatibutor.identifiers.forEach((i) => {
      idString.push(this.makeIdEntry(i));
    });

    return {
      text: creatibutor.name,
      value: creatibutor.id,
      extra: creatibutor,
      key: creatibutor.id,
      content: (
        <Header>
          <Header.Content>
            {creatibutor.name} {idString.length ? <>({idString})</> : null}
          </Header.Content>
          <Header.Subheader>{affNames}</Header.Subheader>
        </Header>
      ),
    };
  })

  const { showPersonForm } = this.state;
  const { autocompleteNames } = this.props;

  const showManualEntry =
    autocompleteNames === NamesAutocompleteOptions.SEARCH_ONLY && !showPersonForm;

  if (showManualEntry) {
    results.push({
      text: "Manual entry",
      value: "Manual entry",
      extra: "Manual entry",
      key: "manual-entry",
      content: (
        <Header textAlign="center">
          <Header.Content>
            <p>
              <Trans>
                {/* eslint-disable-next-line jsx-a11y/anchor-is-valid*/}
                Couldn't find your person? You can <a>create a new entry</a>.
              </Trans>
            </p>
          </Header.Content>
        </Header>
      ),
    });
  }
  return results;
};


export const CreatibutorsModal = ({ autocompleteNames, initialCreatibutor, initialAction, addLabel, editLabel, schema, onCreatibutorChange, trigger }) => {
  const [open, setOpen] = React.useState(false)
  const [action, setAction] = React.useState(initialAction)
  const [saveAndContinueLabel, setSaveAndContinueLabel] = React.useState(i18next.t('Save and add another'))
  const [showPersonForm, setShowPersonForm] = React.useState(autocompleteNames !== NamesAutocompleteOptions.SEARCH_ONLY || !_isEmpty(initialCreatibutor))
  const namesAutocompleteRef = createRef()

  const isCreator = schema === "creators"

  const CreatorSchema = Yup.object({
    nameType: Yup.string(),
    fullName: Yup.string().required(i18next.t("Name is a required field.")),
    role: Yup.string().when("_", (_, schema) => {
      if (!isCreator) {
        return schema.required(i18next.t("Role is a required field."));
      }
    }),
  });

  const focusInput = () => { };

  const openModal = () => {
    setOpen(true)
  };

  const closeModal = () => {
    setOpen(false)
  };

  const changeContent = () => {
    setSaveAndContinueLabel(i18next.t("Added"))
    // change in 2 sec
    setTimeout(() => {
      setSaveAndContinueLabel(i18next.t("Save and add another"))
    }, 2000);
  };

  const displayActionLabel = action === ModalActions.ADD ? addLabel : editLabel;

  const onSubmit = (values, formikBag) => {
    console.log('onSubmit', values)
    onCreatibutorChange(serializeCreatibutor(values));
    formikBag.setSubmitting(false);
    formikBag.resetForm();
    switch (action) {
      case "saveAndContinue":
        closeModal();
        openModal();
        changeContent();
        break;
      case "saveAndClose":
        closeModal();
        break;
      default:
        break;
    }
  };

  const onPersonSearchChange = ({ formikProps }, selectedSuggestions) => {
    if (selectedSuggestions[0].key === "manual-entry") {
      // Empty the autocomplete's selected values
      namesAutocompleteRef.current.setState({
        suggestions: [],
        selectedSuggestions: [],
      });
      setShowPersonForm(true)
      return;
    }

    setShowPersonForm(true)
    const identifiers = selectedSuggestions[0].extra.authorityIdentifiers.map(
      (identifier) => {
        return identifier.identifier;
      }
    );
    const affiliations = selectedSuggestions[0].extra.affiliations.map(
      (affiliation) => {
        return affiliation;
      }
    );

    const personOrOrgPath = ``;
    const familyNameFieldPath = `${personOrOrgPath}family_name`;
    const givenNameFieldPath = `${personOrOrgPath}given_name`;
    const identifiersFieldPath = `${personOrOrgPath}identifiers`;
    const affiliationsFieldPath = "affiliations";

    let chosen = {
      [givenNameFieldPath]: selectedSuggestions[0].extra.given_name,
      [familyNameFieldPath]: selectedSuggestions[0].extra.family_name,
      [identifiersFieldPath]: identifiers,
      [affiliationsFieldPath]: affiliations,
    };
    Object.entries(chosen).forEach(([path, value]) => {
      formikProps.form.setFieldValue(path, value);
    });
  };
  console.log('render', initialCreatibutor)

  const ActionLabel = () => displayActionLabel;
  const personOrOrgPath = ``;
  const typeFieldPath = `${personOrOrgPath}nameType`;
  const familyNameFieldPath = `${personOrOrgPath}family_name`;
  const givenNameFieldPath = `${personOrOrgPath}given_name`;
  const nameFieldPath = `${personOrOrgPath}fullName`;
  const identifiersFieldPath = `${personOrOrgPath}authorityIdentifiers`;
  const affiliationsFieldPath = "affiliations";
  const roleFieldPath = "role";

  return (
    <Formik
      initialValues={deserializeCreatibutor(initialCreatibutor, isCreator)}
      onSubmit={onSubmit}
      enableReinitialize
      validationSchema={CreatorSchema}
      validateOnChange={false}
      validateOnBlur={false}
    >
      {({ values, resetForm, handleSubmit }) => (
        <Modal
          centered={false}
          onOpen={() => openModal()}
          open={open}
          trigger={trigger}
          onClose={() => {
            closeModal()
            resetForm()
          }}
          closeIcon
          closeOnDimmerClick={false}
        >
          <Modal.Header as="h6" className="pt-10 pb-10">
            <Grid>
              <Grid.Column floated="left" width={4}>
                <Header as="h2">
                  <ActionLabel />
                </Header>
              </Grid.Column>
            </Grid>
          </Modal.Header>
          <Modal.Content>
            <Form>
              <Form.Group>
                <RadioField
                  fieldPath={typeFieldPath}
                  label={i18next.t("Person")}
                  checked={_get(values, typeFieldPath) === CREATIBUTOR_TYPE.PERSON}
                  value={CREATIBUTOR_TYPE.PERSON}
                  onChange={({ formikProps }) => {
                    formikProps.form.setFieldValue(
                      typeFieldPath,
                      CREATIBUTOR_TYPE.PERSON
                    );
                  }}
                  optimized
                />
                <RadioField
                  fieldPath={typeFieldPath}
                  label={i18next.t("Organization")}
                  checked={
                    _get(values, typeFieldPath) === CREATIBUTOR_TYPE.ORGANIZATION
                  }
                  value={CREATIBUTOR_TYPE.ORGANIZATION}
                  onChange={({ formikProps }) => {
                    formikProps.form.setFieldValue(
                      typeFieldPath,
                      CREATIBUTOR_TYPE.ORGANIZATION
                    );
                  }}
                  optimized
                />
              </Form.Group>
              {_get(values, typeFieldPath, "") === CREATIBUTOR_TYPE.PERSON ? (
                <div>
                  {autocompleteNames !== NamesAutocompleteOptions.OFF && (
                    <RemoteSelectField
                      selectOnBlur={false}
                      selectOnNavigation={false}
                      searchInput={{
                        autoFocus: _isEmpty(initialCreatibutor),
                      }}
                      fieldPath="creators"
                      clearable
                      multiple={false}
                      allowAdditions={false}
                      placeholder={i18next.t(
                        "Search for persons by name, identifier, or affiliation..."
                      )}
                      noQueryMessage={i18next.t(
                        "Search for persons by name, identifier, or affiliation..."
                      )}
                      required={false}
                      // Disable UI-side filtering of search results
                      search={(options) => options}
                      suggestionAPIUrl="/api/names"
                      serializeSuggestions={serializeSuggestions}
                      onValueChange={onPersonSearchChange}
                      ref={namesAutocompleteRef}
                    />
                  )}
                  {showPersonForm && (
                    <div>
                      <Form.Group widths="equal">
                        <TextField
                          label={i18next.t("Family name")}
                          placeholder={i18next.t("Family name")}
                          fieldPath={familyNameFieldPath}
                          required={isCreator}
                        />
                        <TextField
                          label={i18next.t("Given names")}
                          placeholder={i18next.t("Given names")}
                          fieldPath={givenNameFieldPath}
                          required={isCreator}
                        />
                      </Form.Group>
                      <Form.Group widths="equal">
                        <CreatibutorsIdentifiers
                          fieldPath={identifiersFieldPath}
                        />
                      </Form.Group>
                    </div>
                  )}
                </div>
              ) : (
                <>
                  <TextField
                    label={i18next.t("Name")}
                    placeholder={i18next.t("Organization name")}
                    fieldPath={nameFieldPath}
                    required={isCreator}
                  />
                  <CreatibutorsIdentifiers
                    fieldPath={identifiersFieldPath}
                    placeholder={i18next.t("e.g. ROR, ISNI or GND.")}
                  />
                </>
              )}
              {(_get(values, typeFieldPath) === CREATIBUTOR_TYPE.ORGANIZATION ||
                (showPersonForm &&
                  _get(values, typeFieldPath) === CREATIBUTOR_TYPE.PERSON)) && (
                  <div>
                    <VocabularySelectField
                      label={i18next.t('Affiliations')}
                      type="institutions"
                      fieldPath={affiliationsFieldPath}
                      placeholder={i18next.t("Select one or more affiliations")}
                      multiple
                    />
                    {/* TODO: this should be LocalVocabularySelectField */}
                    <VocabularySelectField
                      type='contributor-roles'
                      fieldPath={roleFieldPath}
                      label={i18next.t("Role")}
                      placeholder={i18next.t("Select role")}
                      {...(isCreator && { clearable: true })}
                      required={!isCreator}
                      scrolling
                    />
                  </div>
                )}
            </Form>
          </Modal.Content>
          <Modal.Actions>
            <Button
              name="cancel"
              onClick={() => {
                resetForm()
                closeModal()
              }}
              icon="remove"
              content={i18next.t("Cancel")}
              floated="left"
            />
            {action === ModalActions.ADD && (
              <Button
                name="submit"
                type="submit"
                onClick={() => {
                  setAction("saveAndContinue")
                  setShowPersonForm(autocompleteNames !== NamesAutocompleteOptions.SEARCH_ONLY)
                  handleSubmit()
                }}
                primary
                icon="checkmark"
                content={saveAndContinueLabel}
              />
            )}
            <Button
              name="submit"
              type="submit"
              onClick={() => {
                setAction('saveAndClose')
                setShowPersonForm(autocompleteNames !== NamesAutocompleteOptions.SEARCH_ONLY)
                handleSubmit()
              }}
              primary
              icon="checkmark"
              content={i18next.t("Save")}
            />
          </Modal.Actions>
        </Modal>
      )}
    </Formik>
  )
}


CreatibutorsModal.propTypes = {
  schema: PropTypes.oneOf(["creators", "contributors"]).isRequired,
  initialAction: PropTypes.oneOf(["add", "edit"]).isRequired,
  addLabel: PropTypes.string.isRequired,
  autocompleteNames: PropTypes.oneOf(["search", "search_only", "off"]),
  editLabel: PropTypes.string.isRequired,
  initialCreatibutor: PropTypes.shape({
    id: PropTypes.string,
    family_name: PropTypes.string,
    given_name: PropTypes.string,
    fullName: PropTypes.string,
    authorityIdentifiers: PropTypes.arrayOf(
      PropTypes.shape({
        scheme: PropTypes.string,
        identifier: PropTypes.string,
      })
    ),
    affiliations: PropTypes.array,
    role: PropTypes.string,
  }),
  trigger: PropTypes.object.isRequired,
  onCreatibutorChange: PropTypes.func.isRequired,
  roleOptions: PropTypes.array,
};

CreatibutorsModal.defaultProps = {
  initialCreatibutor: {
    nameType: CREATIBUTOR_TYPE.PERSON,
    fullName: '',
    affiliations: [],
    identifiers: []
  },
  autocompleteNames: "search",
};

// This file is part of Invenio-RDM-Records
// Copyright (C) 2020-2023 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
// Copyright (C) 2022 data-futures.org.
//
// Invenio-RDM-Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { createRef } from "react";
import { Button, Form, Grid, Header, Modal } from "semantic-ui-react";
import { Formik } from "formik";
import * as Yup from "yup";
import { i18next } from "@translations/docs_app/i18next";
import { TextField, FieldLabel, GroupField } from "react-invenio-forms";
import { CreatibutorsField } from "../CreatibutorsField";
import { IdentifiersField, objectIdentifiersSchema } from "../IdentifiersField";
import { LocalVocabularySelectField } from "@js/oarepo_vocabularies";
import { useFormikContext } from "formik";

const FormikStateLogger = () => {
  const state = useFormikContext();
  return <pre>{JSON.stringify(state, null, 2)}</pre>;
};

export const RelatedItemsModal = ({
  autocompleteNames,
  initialCreatibutor,
  initialAction,
  addLabel,
  editLabel,
  schema,
  onCreatibutorChange,
  trigger,
}) => {
  const [open, setOpen] = React.useState(false);
  const [action, setAction] = React.useState(initialAction);
  const [saveAndContinueLabel, setSaveAndContinueLabel] = React.useState(
    i18next.t("Save and add another")
  );

  const openModal = () => {
    setOpen(true);
  };

  const closeModal = () => {
    setOpen(false);
  };

  const changeContent = () => {
    setSaveAndContinueLabel(i18next.t("Added"));
    // change in 2 sec
    setTimeout(() => {
      setSaveAndContinueLabel(i18next.t("Save and add another"));
    }, 2000);
  };

  const onSubmit = (values, formikBag) => {
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

  return (
    <Formik
      initialValues={{}}
      onSubmit={onSubmit}
      enableReinitialize
      //   validationSchema={CreatorSchema}
      validateOnChange={false}
      validateOnBlur={false}
    >
      {({ values, resetForm, handleSubmit, errors }) => (
        <Modal
          size="large"
          centered={false}
          onOpen={() => openModal()}
          open={open}
          trigger={trigger}
          onClose={() => {
            closeModal();
            resetForm();
          }}
          closeIcon
          closeOnDimmerClick={false}
        >
          <Modal.Header as="h6" className="pt-10 pb-10">
            <Grid>
              <Grid.Column floated="left" width={4}>
                <Header as="h2"></Header>
              </Grid.Column>
            </Grid>
          </Modal.Header>
          <Modal.Content>
            <Form>
              <TextField
                fieldPath="itemTitle"
                required
                label={
                  <FieldLabel
                    htmlFor={"itemTitle"}
                    icon="pencil"
                    label={i18next.t("Title")}
                  />
                }
                helpText={i18next.t("Title of the related item")}
              />
              <CreatibutorsField
                label={i18next.t("Creators")}
                labelIcon="user"
                fieldPath="itemCreators"
                schema="creators"
                autocompleteNames="off"
                required={false}
              />

              <CreatibutorsField
                label={i18next.t("Contributors")}
                addButtonLabel={i18next.t("Add contributor")}
                modal={{
                  addLabel: i18next.t("Add contributor"),
                  editLabel: i18next.t("Edit contributor"),
                }}
                labelIcon="user"
                fieldPath="itemContributors"
                schema="contributors"
                autocompleteNames="off"
              />

              <IdentifiersField
                options={objectIdentifiersSchema}
                fieldPath="itemPIDs"
                identifierLabel={i18next.t("Object identifier")}
                label={i18next.t("Object identifiers")}
                helpText={i18next.t(
                  "Persistent identifier/s of object as ISBN, DOI, etc."
                )}
              />
              <TextField
                fieldPath="itemURL"
                label={
                  <FieldLabel
                    htmlFor={"itemTitle"}
                    icon="pencil"
                    label={i18next.t("URL")}
                  />
                }
              />
              <GroupField>
                <TextField
                  width={2}
                  fieldPath="itemYear"
                  label={
                    <FieldLabel
                      htmlFor={"itemYear"}
                      icon="pencil"
                      label={i18next.t("Year")}
                    />
                  }
                />
                <TextField
                  width={2}
                  fieldPath="itemVolume"
                  label={
                    <FieldLabel
                      htmlFor={"itemVolume"}
                      icon="pencil"
                      label={i18next.t("Volume")}
                    />
                  }
                />
                <TextField
                  width={2}
                  fieldPath="itemIssue"
                  label={
                    <FieldLabel
                      htmlFor={"itemIssue"}
                      icon="pencil"
                      label={i18next.t("Issue")}
                    />
                  }
                />
                <TextField
                  width={2}
                  fieldPath="itemStartPage"
                  label={
                    <FieldLabel
                      htmlFor={"itemStartPage"}
                      icon="pencil"
                      label={i18next.t("Start page")}
                    />
                  }
                />
                <TextField
                  width={2}
                  fieldPath="itemEndPage"
                  label={
                    <FieldLabel
                      htmlFor={"itemEndPage"}
                      icon="pencil"
                      label={i18next.t("End page")}
                    />
                  }
                />
                <TextField
                  width={6}
                  fieldPath="itemPublisher"
                  label={
                    <FieldLabel
                      htmlFor={"itemPublisher"}
                      icon="pencil"
                      label={i18next.t("Publisher")}
                    />
                  }
                />
              </GroupField>
              <LocalVocabularySelectField
                fieldPath="itemRelationType"
                required
                label={
                  <FieldLabel
                    htmlFor={"itemRelationType"}
                    icon=""
                    label={i18next.t("Relation type")}
                  />
                }
                placeholder={i18next.t("Choose relation type")}
                clearable
                optionsListName="item-relation-types"
              />
            </Form>
            <FormikStateLogger />
          </Modal.Content>
          <Modal.Actions>
            <Button
              name="cancel"
              onClick={() => {
                resetForm();
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
                setAction("saveAndContinue");

                handleSubmit();
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

                handleSubmit();
              }}
              primary
              icon="checkmark"
              content={i18next.t("Save")}
            />
          </Modal.Actions>
        </Modal>
      )}
    </Formik>
  );
};

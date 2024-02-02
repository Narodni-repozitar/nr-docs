import React from "react";
import { Button, Form, Grid, Header, Modal } from "semantic-ui-react";
import { Formik } from "formik";
import * as Yup from "yup";
import { i18next } from "@translations/i18next";
import PropTypes from "prop-types";
import { MultilingualTextInput, ArrayFieldItem } from "@js/oarepo_ui";

export const SubjectsModal = ({ trigger, handleSubjectAdd, fieldPath }) => {
  const [open, setOpen] = React.useState(false);
  const [saveAndContinueLabel, setSaveAndContinueLabel] = React.useState(
    i18next.t("Save and add another")
  );
  const [action, setAction] = React.useState();

  const openModal = () => {
    setOpen(true);
  };
  const closeModal = () => {
    setOpen(false);
  };

  const changeContent = () => {
    setSaveAndContinueLabel(i18next.t("Added"));
    setTimeout(() => {
      setSaveAndContinueLabel(i18next.t("Save and add another"));
    }, 1000);
  };

  const onSubmit = (values, formikBag) => {
    const newSubject = { subjectScheme: "keyword", subject: values.keywords };
    console.log(values);
    handleSubjectAdd(newSubject);
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
      //   validationSchema={}
      validateOnChange={false}
      validateOnBlur={false}
    >
      {({ values, resetForm, handleSubmit, errors }) => (
        <Modal
          className="form-modal"
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
          <Modal.Header as="h6">
            <Grid>
              <Grid.Column floated="left" width={8}>
                <Header className="rel-pt-1 rel-pb-1" as="h2">
                  {i18next.t("Add related item")}
                </Header>
              </Grid.Column>
            </Grid>
          </Modal.Header>
          <Modal.Content>
            <Form>
              <Form.Field style={{ marginTop: 0 }} width={16}>
                <MultilingualTextInput
                  fieldPath={`keywords`}
                  lngFieldWidth={5}
                  textFieldLabel={i18next.t("Subject")}
                  required
                  showEmptyValue
                />
              </Form.Field>
            </Form>
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

SubjectsModal.propTypes = {
  trigger: PropTypes.node,
};

SubjectsModal.defaultProps = {
  initialRelatedItem: {},
};

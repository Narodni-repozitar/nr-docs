import React, { memo } from "react";
import { Button, Modal, Message, Icon, Form } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { useConfirmationModal, useDepositApiClient } from "@js/oarepo_ui";
import { TextField, FieldLabel } from "react-invenio-forms";
import PropTypes from "prop-types";

export const PublishButtonComponent = memo(({ modalMessage, modalHeader }) => {
  const {
    isOpen: isModalOpen,
    close: closeModal,
    open: openModal,
  } = useConfirmationModal();
  const { isSubmitting, publish, isPublishing } = useDepositApiClient();

  return (
    <React.Fragment>
      <Button
        name="publish"
        color="green"
        onClick={openModal}
        icon="upload"
        labelPosition="left"
        content={i18next.t("Publish")}
        type="button"
        disabled={isSubmitting}
        loading={isPublishing}
        fluid
      />
      <Modal
        className="form-modal"
        open={isModalOpen}
        onClose={closeModal}
        size="small"
        closeIcon
        closeOnDimmerClick={false}
      >
        <Modal.Header>{modalHeader}</Modal.Header>
        <Modal.Content>
          <Form>
            <TextField
              fieldPath="metadata.version"
              placeholder={i18next.t("Write the version (first, second ...).")}
              label={
                <FieldLabel
                  htmlFor={"metadata.version"}
                  icon="pencil"
                  label={i18next.t("Version")}
                />
              }
            />
          </Form>

          <Message icon size="small">
            <Icon
              name="warning sign"
              size="mini"
              style={{ fontSize: "1rem" }}
            />
            <Message.Content>{modalMessage}</Message.Content>
          </Message>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={closeModal} floated="left">
            {i18next.t("Cancel")}
          </Button>
          <Button
            name="publish"
            disabled={isSubmitting}
            loading={isPublishing}
            color="green"
            onClick={() => {
              publish();
              closeModal();
            }}
            icon="upload"
            labelPosition="left"
            content={i18next.t("Publish")}
            type="submit"
          />
        </Modal.Actions>
      </Modal>
    </React.Fragment>
  );
});

PublishButtonComponent.propTypes = {
  modalMessage: PropTypes.string,
  modalHeader: PropTypes.string,
};

PublishButtonComponent.defaultProps = {
  modalHeader: i18next.t("Are you sure you wish to publish this draft?"),
  modalMessage: i18next.t(
    "Once the record is published you will no longer be able to change the files in the upload! However, you will still be able to update the record's metadata later."
  ),
};

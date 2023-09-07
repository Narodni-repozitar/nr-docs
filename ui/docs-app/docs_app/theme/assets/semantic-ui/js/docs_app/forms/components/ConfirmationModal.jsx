import React from "react";
import { Modal, Message, Button, Icon } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import PropTypes from "prop-types";

export const ConfirmationModal = ({
  isModalOpen,
  handleCloseModal,
  modalHeader,
  modalMessage,
  actionButton: ActionButton,
}) => {
  return (
    <Modal
      open={isModalOpen}
      onClose={handleCloseModal}
      size="small"
      closeIcon
      closeOnDimmerClick={false}
    >
      <Modal.Header>{modalHeader}</Modal.Header>
      <Modal.Content>
        {modalMessage && (
          <Message visible warning>
            <p>
              <Icon name="warning sign" /> {modalMessage}
            </p>
          </Message>
        )}
      </Modal.Content>
      <Modal.Actions>
        <Button onClick={handleCloseModal} floated="left">
          {i18next.t("Cancel")}
        </Button>
        <ActionButton />
      </Modal.Actions>
    </Modal>
  );
};

ConfirmationModal.propTypes = {
  isModalOpen: PropTypes.bool.isRequired,
  handleCloseModal: PropTypes.func.isRequired,
  modalHeader: PropTypes.string.isRequired,
  modalMessage: PropTypes.string,
  actionButton: PropTypes.node.isRequired,
};

import React from "react";
import { Button, Modal, Icon, Message } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import {
  useApiClient,
  useConfirmationModal,
  useFormConfig,
  useDepositApiClient,
} from "@js/oarepo_ui";
import PropTypes from "prop-types";

export const DeleteButtonComponent = ({ modalMessage, modalHeader }) => {
  const { isModalOpen, handleCloseModal, handleOpenModal } =
    useConfirmationModal();
  // const apiClient = useApiClient();
  const {
    formConfig: { permissions },
  } = useFormConfig();
  const { values, isSubmitting, _delete } = useDepositApiClient();

  return (
    <React.Fragment>
      {values.id && permissions.can_delete_draft && (
        <Button
          name="delete"
          color="red"
          onClick={handleOpenModal}
          icon="delete"
          labelPosition="left"
          content={i18next.t("Delete")}
          type="button"
          disabled={isSubmitting}
          loading={isSubmitting}
          fluid
        />
      )}
      <Modal
        open={isModalOpen}
        onClose={handleCloseModal}
        size="small"
        closeIcon
        closeOnDimmerClick={false}
      >
        <Modal.Header>{modalHeader}</Modal.Header>
        {modalMessage && (
          <Modal.Content>
            <Message visible warning>
              <p>
                <Icon name="warning sign" /> {modalMessage}
              </p>
            </Message>
          </Modal.Content>
        )}
        <Modal.Actions>
          <Button onClick={handleCloseModal} floated="left">
            {i18next.t("Cancel")}
          </Button>
          <Button
            name="delete"
            disabled={isSubmitting}
            loading={isSubmitting}
            color="red"
            onClick={() => {
              _delete();
              handleCloseModal();
            }}
            icon="delete"
            labelPosition="left"
            content={i18next.t("Delete")}
            type="button"
          />
        </Modal.Actions>
      </Modal>
    </React.Fragment>
  );
};

DeleteButtonComponent.propTypes = {
  modalMessage: PropTypes.string,
  modalHeader: PropTypes.string,
};

DeleteButtonComponent.defaultProps = {
  modalHeader: i18next.t("Are you sure you wish delete this draft?"),
  modalMessage: i18next.t(
    "If you delete the draft, the work you have done on it will be lost"
  ),
};

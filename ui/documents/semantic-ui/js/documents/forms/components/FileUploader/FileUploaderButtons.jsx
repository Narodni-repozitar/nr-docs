import React, { useState } from "react";
import PropTypes from "prop-types";
import { Button, Icon } from "semantic-ui-react";
import FileManagementDialog from "@oarepo/file-manager";
import { FileEditWrapper, FileUploadWrapper } from "./FileUploaderWrappers";
import { useDepositFileApiClient } from "@js/oarepo_ui";
import { i18next } from "@translations/i18next";

export const EditFileButton = ({ fileName, record }) => {
  return (
    <FileEditWrapper
      preactComponent={FileManagementDialog}
      props={{
        config: { record: record },
        autoExtractImagesFromPDFs: false,
        locale: i18next.language,
        startEvent: { event: "edit-file", data: { file_key: fileName } },
        modifyExistingFiles: true,
        allowedFileTypes: ["*/*"],
      }}
    />
  );
};

EditFileButton.propTypes = {
  fileName: PropTypes.string.isRequired,
  record: PropTypes.object.isRequired,
};

export const UploadFileButton = ({ record, handleFilesUpload }) => {
  return (
    <FileUploadWrapper
      preactComponent={FileManagementDialog}
      props={{
        config: { record: record },
        autoExtractImagesFromPDFs: false,
        locale: i18next.language,
        allowedFileTypes: ["*/*"],
        startEvent: null,
        onSuccessfulUpload: (files) => {
          handleFilesUpload(files);
        },
        allowedMetaFields: [
          {
            id: "fileNote",
            defaultValue: "",
            isUserInput: true,
          },
        ],
      }}
    />
  );
};

UploadFileButton.propTypes = {
  record: PropTypes.object.isRequired,
  handleFilesUpload: PropTypes.func.isRequired,
};

export const DeleteFileButton = ({ file, handleFileDeletion }) => {
  const { _delete } = useDepositFileApiClient();
  const [isDeleting, setIsDeleting] = useState(false);
  const handleDelete = async () => {
    setIsDeleting(true);
    _delete(file)
      .then((response) => {
        setIsDeleting(false);
        if (response.status === 204) handleFileDeletion(file);
      })
      .catch(() => {
        setIsDeleting(false);
      });
  };
  return isDeleting ? (
    <Button disabled style={{ backgroundColor: "transparent" }} type="button">
      <Icon loading name="spinner" />
    </Button>
  ) : (
    <Button
      disabled={isDeleting}
      style={{ backgroundColor: "transparent" }}
      type="button"
      onClick={handleDelete}
    >
      <Icon
        aria-hidden="true"
        name="trash alternate"
        style={{ margin: 0, opacity: "1" }}
      />
    </Button>
  );
};

DeleteFileButton.propTypes = {
  file: PropTypes.object.isRequired,
  handleFileDeletion: PropTypes.func.isRequired,
};

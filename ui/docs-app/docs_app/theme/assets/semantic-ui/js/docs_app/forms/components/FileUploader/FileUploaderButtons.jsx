import React from "react";
import PropTypes from "prop-types";
import { Button, Icon } from "semantic-ui-react";
import FileManagementDialog from "@oarepo/file-manager";
import { FileEditWrapper, FileUploadWrapper } from "./FileUploaderWrappers";
import { useDepositFileApiClient } from "@js/oarepo_ui";
import { i18next } from "@translations/docs_app/i18next";

export const EditFileButton = ({ fileName, record }) => {
  return (
    <FileEditWrapper
      preactComponent={FileManagementDialog}
      props={{
        config: { record: record },
        autoExtractImagesFromPDFs: false,
        locale: i18next.language,
        startEvent: { event: "edit-file", data: { file_key: fileName } },
      }}
    />
  );
};

EditFileButton.propTypes = {
  fileName: PropTypes.string.isRequired,
  record: PropTypes.object.isRequired,
};

export const UploadFileButton = ({ record }) => {
  return (
    <FileUploadWrapper
      preactComponent={FileManagementDialog}
      props={{
        config: { record: record },
        autoExtractImagesFromPDFs: false,
        locale: i18next.language,
        startEvent: { event: "upload-file-without-edit" },
      }}
    />
  );
};

UploadFileButton.propTypes = { record: PropTypes.object.isRequired };

export const DeleteFileButton = ({ file }) => {
  const { _delete } = useDepositFileApiClient();
  return (
    <Button
      style={{ backgroundColor: "transparent" }}
      type="button"
      onClick={() => _delete(file.links.self)}
    >
      <Icon
        aria-hidden="true"
        name="trash alternate"
        style={{ margin: 0, opacity: "1" }}
      />
    </Button>
  );
};

DeleteFileButton.propTypes = { file: PropTypes.object.isRequired };

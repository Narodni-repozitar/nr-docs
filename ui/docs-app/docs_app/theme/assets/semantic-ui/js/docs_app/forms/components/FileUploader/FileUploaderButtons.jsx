import React from "react";
import PropTypes from "prop-types";
import { Button, Icon } from "semantic-ui-react";
import FileManagementDialog from "@oarepo/file-manager";
import { FileEditWrapper, FileUploadWrapper } from "./FileUploaderWrappers";
import { useDepositFileApiClient } from "@js/oarepo_ui";

export const EditFileButton = ({ key, record }) => {
  return (
    <FileEditWrapper
      preactComponent={FileManagementDialog}
      props={{
        config: { record: record },
        autoExtractImagesFromPDFs: false,
        locale: "cs_CS",
        startEvent: { event: "edit-file", data: { file_key: key } },
      }}
    />
  );
};

EditFileButton.propTypes = {
  key: PropTypes.string.isRequired,
  record: PropTypes.object.isRequired,
};

export const UploadFileButton = ({ record }) => {
  return (
    <FileUploadWrapper
      preactComponent={FileManagementDialog}
      props={{
        config: { record: record },
        autoExtractImagesFromPDFs: false,
        locale: "cs_CS",
      }}
    />
  );
};

export const DeleteFileButton = ({ file }) => {
  const { _delete } = useDepositFileApiClient();
  return (
    <Button type="button" onClick={() => _delete(file.links.self)}>
      <Icon aria-hidden="true" name="trash alternate" />
    </Button>
  );
};

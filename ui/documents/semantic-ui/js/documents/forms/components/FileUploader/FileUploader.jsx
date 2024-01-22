import React, { useState } from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/i18next";
import { Message, Icon, Button } from "semantic-ui-react";
import { FileUploaderTable } from "./FileUploaderTable";
import { UploadFileButton } from "./FileUploaderButtons";
import { useDepositApiClient } from "@js/oarepo_ui";
import { Trans } from "react-i18next";

export const FileUploader = ({ messageContent, record, recordFiles }) => {
  const [filesState, setFilesState] = useState(recordFiles?.entries || []);
  const { formik, isSubmitting, save, isSaving } = useDepositApiClient();
  const { values } = formik;
  const recordObject = record || values;

  const handleFilesUpload = (uploadedFiles) => {
    const deserializedFiles = uploadedFiles.map((file) => file.response.body);
    setFilesState((prevFiles) => [...prevFiles, ...deserializedFiles]);
  };
  const handleFileDeletion = (fileObject) => {
    const newFiles = filesState.filter(
      (file) => file.file_id !== fileObject.file_id
    );
    setFilesState(newFiles);
  };

  return (
    <React.Fragment>
      {values.id ? (
        <React.Fragment>
          {recordObject?.files?.enabled && (
            <React.Fragment>
              <FileUploaderTable
                files={filesState}
                handleFileDeletion={handleFileDeletion}
                record={recordObject}
              />
              <UploadFileButton
                record={recordObject}
                handleFilesUpload={handleFilesUpload}
              />
            </React.Fragment>
          )}
          <Message icon size="small">
            <Icon
              name="warning sign"
              size="mini"
              style={{ fontSize: "1rem" }}
            />
            <Message.Content>{messageContent}</Message.Content>
          </Message>
        </React.Fragment>
      ) : (
        <Message>
          <Icon name="info circle" size="mini" style={{ fontSize: "1rem" }} />
          <Trans>
            If you wish to upload files, you must
            <Button
              className="ml-5 mr-5"
              primary
              onClick={() => save(true)}
              loading={isSaving}
              disabled={isSubmitting}
              size="mini"
            >
              save
            </Button>
            your draft first.
          </Trans>
        </Message>
      )}
    </React.Fragment>
  );
};

FileUploader.propTypes = {
  messageContent: PropTypes.string,
  record: PropTypes.object,
  recordFiles: PropTypes.object,
};

FileUploader.defaultProps = {
  messageContent: i18next.t(
    "File addition, removal or modification are not allowed after you have published your draft."
  ),
};

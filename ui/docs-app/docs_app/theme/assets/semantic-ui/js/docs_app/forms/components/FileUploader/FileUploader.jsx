import React, { useState } from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/docs_app/i18next";
import { Message, Icon } from "semantic-ui-react";
import { FileUploaderTable } from "./FileUploaderTable";
import { UploadFileButton } from "./FileUploaderButtons";
import { useDepositFileApiClient } from "@js/oarepo_ui";

export const FileUploader = ({
  messageContent,
  record,
  files: recordFiles,
}) => {
  const [files, setFiles] = useState(recordFiles);
  const { read, formik, setFieldValue } = useDepositFileApiClient();
  const { values } = formik;
  const recordObject = record || values;
  // const { data, isLoading, error, refetch } = useQuery({
  //   retry: false,
  //   queryKey: ["files"],
  //   queryFn: () => read(recordObject),
  //   onError: (error) =>
  //     setFieldValue(
  //       "httpErrors",
  //       error?.response?.data?.message ?? error.message
  //     ),
  // });
  return (
    <React.Fragment>
      <FileUploaderTable record={recordObject} files={files} />
      <UploadFileButton record={recordObject} />
      <Message icon size="small">
        <Icon name="warning sign" size="mini" style={{ fontSize: "1rem" }} />
        <Message.Content>{messageContent}</Message.Content>
      </Message>
    </React.Fragment>
  );
};

FileUploader.propTypes = {
  messageContent: PropTypes.string,
  record: PropTypes.object,
  files: PropTypes.object,
};

FileUploader.defaultProps = {
  messageContent: i18next.t(
    "File addition, removal or modification are not allowed after you have published your draft."
  ),
};

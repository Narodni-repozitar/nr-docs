import React, { useState } from "react";
import { useFormikContext } from "formik";
import PropTypes from "prop-types";
import { i18next } from "@translations/docs_app/i18next";
import { Message, Icon } from "semantic-ui-react";
import { FileUploaderTable } from "./FileUploaderTable";
import { UploadFileButton } from "./FileUploaderButtons";
import { useQuery } from "@tanstack/react-query";
import { useDepositFileApiClient } from "@js/oarepo_ui";
import _isEmpty from "lodash/isEmpty";

export const FileUploader = ({ messageContent, record }) => {
  const { read, formik, setFieldValue } = useDepositFileApiClient();
  const [files, setFiles] = useState({});
  const { values } = formik;
  const recordObject = record || values;
  console.log("file manager");
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["files"],
    queryFn: () => {
      console.log("query");
      return read(recordObject);
    },
    onError: (error) =>
      setFieldValue(
        "httpErrors",
        error?.response?.data?.message ?? error.message
      ),
    onSuccess: (data) => {
      setFiles(data);
    },
  });
  return (
    !_isEmpty(data) &&
    !isLoading && (
      <React.Fragment>
        <FileUploaderTable
          record={recordObject}
          files={data}
          refetch={refetch}
        />
        <UploadFileButton record={recordObject} refetch={refetch} />
        <Message icon size="small">
          <Icon name="warning sign" size="mini" style={{ fontSize: "1rem" }} />
          <Message.Content>{messageContent}</Message.Content>
        </Message>
      </React.Fragment>
    )
  );
};

FileUploader.propTypes = {
  messageContent: PropTypes.string,
  record: PropTypes.object,
};

FileUploader.defaultProps = {
  messageContent: i18next.t(
    "File addition, removal or modification are not allowed after you have published your draft."
  ),
};

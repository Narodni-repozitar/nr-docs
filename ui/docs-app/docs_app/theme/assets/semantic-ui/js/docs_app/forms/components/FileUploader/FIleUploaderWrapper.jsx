import React, { useEffect, useRef } from "react";
import { h, render } from "preact";
import FileManagementDialog from "@oarepo/file-manager";
import { useFormikContext } from "formik";
import { useDepositApiClient } from "@js/oarepo_ui";
import PropTypes from "prop-types";
import { i18next } from "@translations/docs_app/i18next";
import { Message, Icon } from "semantic-ui-react";
import { FileUploaderTable } from "./FileUploaderTable";

export const UploadWrapper = ({
  preactComponent,
  wrapperClassName,
  uploadButtonClassName,
  props,
}) => {
  const { save } = useDepositApiClient();

  const preactCompRef = useRef();
  useEffect(() => {
    render(
      h(preactComponent, {
        TriggerComponent: ({ onClick, ...props }) => {
          const handleOnClick = async () => {
            // Additional functionality you want to add
            await save();
            // Execute the original onClick handler if available
            onClick?.();
          };

          return h(
            "button",
            {
              className: uploadButtonClassName,
              onClick: handleOnClick,
              ...props,
            },
            i18next.t("Upload files"),
            h("i", { "aria-hidden": "true", className: "upload icon" })
          );
        },
        ...props,
      }),
      preactCompRef.current
    );
  });

  return <div ref={preactCompRef} className={wrapperClassName} />;
};

UploadWrapper.propTypes = {
  preactComponent: PropTypes.elementType.isRequired,
  wrapperClassName: PropTypes.string,
  uploadButtonClassName: PropTypes.string,
  props: PropTypes.object,
};
UploadWrapper.defaultProps = {
  wrapperClassName: "ui container centered",
  uploadButtonClassName: "ui primary button icon left labeled",
};

export const ReactWrapperFile = ({ messageContent }) => {
  const { values } = useFormikContext();
  return (
    <React.Fragment>
      <FileUploaderTable />
      <UploadWrapper
        preactComponent={FileManagementDialog}
        props={{
          config: { record: values },
          locale: "cs_CS",
          // startEvent: {
          //   event: "upload-images-from-pdf",
          //   data: { file_key: key },
          // },
          autoExtractImagesFromPDFs: false,
          allowedMetaFields: [
            {
              id: "caption",
              defaultValue: "default_image_name",
              isUserInput: true,
            },
            { id: "featured", defaultValue: false, isUserInput: true },
          ],
        }}
      />
      <Message icon size="small">
        <Icon name="warning sign" size="mini" style={{ fontSize: "1rem" }} />
        <Message.Content>{messageContent}</Message.Content>
      </Message>
    </React.Fragment>
  );
};

ReactWrapperFile.propTypes = { messageContent: PropTypes.string };

ReactWrapperFile.defaultProps = {
  messageContent: i18next.t(
    "File addition, removal or modification are not allowed after you have published your draft."
  ),
};

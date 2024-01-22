import React, { useEffect, useRef } from "react";
import { h, render } from "preact";
import PropTypes from "prop-types";
import { i18next } from "@translations/i18next";

export const FileUploadWrapper = ({
  preactComponent,
  uploadWrapperClassName,
  uploadButtonClassName,
  props,
}) => {
  const preactCompRef = useRef();
  useEffect(() => {
    render(
      h(preactComponent, {
        TriggerComponent: ({ onClick, ...props }) => {
          return h(
            "button",
            {
              className: uploadButtonClassName,
              onClick: onClick,
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
  }, []);

  return <div ref={preactCompRef} className={uploadWrapperClassName} />;
};

FileUploadWrapper.propTypes = {
  preactComponent: PropTypes.elementType.isRequired,
  uploadWrapperClassName: PropTypes.string,
  uploadButtonClassName: PropTypes.string,
  props: PropTypes.object,
};
FileUploadWrapper.defaultProps = {
  uploadWrapperClassName: "ui container centered",
  uploadButtonClassName: "ui primary button icon left labeled",
};

export const FileEditWrapper = ({
  preactComponent,
  editWrapperClassName,
  editButtonClassName,
  props,
}) => {
  const preactCompRef = useRef();
  useEffect(() => {
    render(
      h(preactComponent, {
        TriggerComponent: ({ onClick, ...props }) => {
          return h(
            "button",
            {
              className: editButtonClassName,
              onClick: onClick,
              ...props,
              ariaLabel: i18next.t("Edit file"),
              style: { backgroundColor: "transparent" },
            },
            h("i", {
              "aria-hidden": "true",
              className: "pencil icon",
              style: { margin: "0", opacity: "1" },
            })
          );
        },
        ...props,
      }),
      preactCompRef.current
    );
  });

  return <div ref={preactCompRef} className={editWrapperClassName} />;
};

FileEditWrapper.propTypes = {
  preactComponent: PropTypes.elementType.isRequired,
  editWrapperClassName: PropTypes.string,
  editButtonClassName: PropTypes.string,
  props: PropTypes.object,
};

FileEditWrapper.defaultProps = {
  // editWrapperClassName: "ui container centered",
  editButtonClassName: "ui button",
};

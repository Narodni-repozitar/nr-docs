import React from "react";
import PropTypes from "prop-types";
import { FieldLabel, TextField } from "react-invenio-forms";
import { i18next } from "@translations/oarepo_vocabularies_ui/i18next";

export const PublicationDateField = ({
  fieldPath,
  helpText,
  label,
  labelIcon,
  placeholder,
  required,
  ...uiProps
}) => {
  return (
    <TextField
      fieldPath={fieldPath}
      helpText={helpText}
      label={<FieldLabel htmlFor={fieldPath} icon={labelIcon} label={label} />}
      placeholder={placeholder}
      required={required}
      {...uiProps}
    />
  );
};

PublicationDateField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
  label: PropTypes.string,
  labelIcon: PropTypes.string,
  placeholder: PropTypes.string,
  required: PropTypes.bool,
};

PublicationDateField.defaultProps = {
  helpText: i18next.t(
    "In case your upload was already published elsewhere, please use the date of the first publication. Format: YYYY-MM-DD, YYYY-MM, or YYYY. For intervals use DATE/DATE, e.g. 1939/1945."
  ),
  label: i18next.t("Publication date"),
  labelIcon: "calendar",
  required: undefined,
  placeholder: i18next.t(
    "YYYY-MM-DD or YYYY-MM-DD/YYYY-MM-DD for intervals. MM and DD are optional."
  ),
};

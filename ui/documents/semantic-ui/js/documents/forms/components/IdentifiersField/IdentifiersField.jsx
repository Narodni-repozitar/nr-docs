import React from "react";
import PropTypes from "prop-types";
import { ArrayField, SelectField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/i18next";
import { ArrayFieldItem } from "@js/oarepo_ui";
import { useFormikContext } from "formik";

export const objectIdentifiersSchema = [
  { value: "DOI", text: "DOI" },
  { value: "Handle", text: "Handle" },
  { value: "ISBN", text: "ISBN" },
  { value: "ISSN", text: "ISSN" },
  { value: "RIV", text: "RIV" },
];

export const authorityIdentifiersSchema = [
  { value: "orcid", text: i18next.t("ORCID") },
  { value: "scopusID", text: i18next.t("ScopusID") },
  { value: "researcherID", text: i18next.t("ResearcherID") },
  { value: "czenasAutID", text: i18next.t("CzenasAutID") },
  { value: "vedidk", text: i18next.t("vedIDK") },
  { value: "institutionalID", text: i18next.t("InstitutionalID") },
  { value: "ISNI", text: i18next.t("ISNI") },
  { value: "ROR", text: i18next.t("ROR") },
  { value: "ICO", text: i18next.t("ICO") },
  { value: "DOI", text: i18next.t("DOI") },
];

export const IdentifiersField = ({
  fieldPath,
  helpText,
  options,
  label,
  identifierLabel,
  className,
  ...uiProps
}) => {
  const { setFieldTouched } = useFormikContext();
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add identifier")}
      fieldPath={fieldPath}
      label={label}
      labelIcon="pencil"
      helpText={helpText}
      className={className}
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <ArrayFieldItem indexPath={indexPath} arrayHelpers={arrayHelpers}>
            <SelectField
              clearable
              width={4}
              fieldPath={`${fieldPathPrefix}.scheme`}
              label={i18next.t("Identifier type")}
              required
              options={options}
              onBlur={() => setFieldTouched(`${fieldPathPrefix}.scheme`)}
              {...uiProps}
            />
            <TextField
              required
              width={12}
              fieldPath={`${fieldPathPrefix}.identifier`}
              label={identifierLabel}
            />
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

IdentifiersField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
  options: PropTypes.array.isRequired,
  label: PropTypes.string,
  identifierLabel: PropTypes.string,
  className: PropTypes.string,
};

IdentifiersField.defaultProps = {
  label: i18next.t("Identifier field"),
  identifierLabel: i18next.t("Identifier"),
};

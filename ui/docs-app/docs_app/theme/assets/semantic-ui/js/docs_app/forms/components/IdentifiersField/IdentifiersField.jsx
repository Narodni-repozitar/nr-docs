import React from "react";
import PropTypes from "prop-types";
import { ArrayField, SelectField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { ArrayFieldItem } from "@js/oarepo_ui";

export const objectIdentifiersSchema = [
  { value: "DOI", text: "DOI" },
  { value: "Handle", text: "Handle" },
  { value: "ISBN", text: "ISBN" },
  { value: "ISSN", text: "ISSN" },
  { value: "RIV", text: "RIV" },
];

export const authorityIdentifiersSchema = [
  { value: "orcid", text: "ORCID" },
  { value: "scopusID", text: "ScopusID" },
  { value: "researcherID", text: "ResearcherID" },
  { value: "czenasAutID", text: "CzenasAutID" },
  { value: "vedidk", text: "vedIDK" },
  { value: "institutionalID", text: "InstitutionalID" },
  { value: "ISNI", text: "ISNI" },
  { value: "ROR", text: "ROR" },
  { value: "ICO", text: "ICO" },
  { value: "DOI", text: "DOI" },
];

export const systemIdentifiersSchema = [
  { value: "nusl", text: "nusl" },
  { value: "nuslOAI", text: "nuslOAI" },
  { value: "originalRecordOAI", text: "originalRecordOAI" },
  { value: "catalogueSysNo", text: "catalogueSysNo" },
  { value: "nrOAI", text: "nrOAI" },
];

export const IdentifiersField = ({
  fieldPath,
  helpText,
  options,
  label,
  identifierLabel,
  className,
}) => {
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
  identifierLabel: i18next.t("Object identifier"),
};

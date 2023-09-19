import React from "react";
import PropTypes from "prop-types";
import { ArrayField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { LocalVocabularySelectField } from "./LocalVocabularySelectField";
import { ArrayFieldItem } from "@js/oarepo_ui";

export const FundersField = ({ fieldPath, helpText }) => {
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add funder")}
      defaultNewValue={{}}
      fieldPath={fieldPath}
      label={i18next.t("Funding")}
      labelIcon="pencil"
      helpText={helpText}
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <ArrayFieldItem indexPath={indexPath} arrayHelpers={arrayHelpers}>
            <TextField
              width={16}
              fieldPath={`${fieldPathPrefix}.projectID`}
              label={i18next.t("Project code")}
              required
            />
            <TextField
              width={16}
              fieldPath={`${fieldPathPrefix}.projectName`}
              label={i18next.t("Project name")}
            />
            <TextField
              width={16}
              fieldPath={`${fieldPathPrefix}.fundingProgram`}
              label={i18next.t("Funding program")}
            />
            <LocalVocabularySelectField
              width={16}
              fieldPath={`${fieldPathPrefix}.funder`}
              label={i18next.t("Funder")}
              optionsListName="funders"
            />
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

FundersField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

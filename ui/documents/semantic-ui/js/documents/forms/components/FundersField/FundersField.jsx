import React from "react";
import PropTypes from "prop-types";
import { ArrayField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/i18next";
import { LocalVocabularySelectField } from "@js/oarepo_vocabularies";
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
          <ArrayFieldItem
            indexPath={indexPath}
            arrayHelpers={arrayHelpers}
            style={{ display: "block" }}
          >
            <TextField
              width={16}
              fieldPath={`${fieldPathPrefix}.projectID`}
              label={i18next.t("Project code")}
              placeholder={i18next.t("Write down project number.")}
            />
            <TextField
              className="rel-mt-1"
              width={16}
              fieldPath={`${fieldPathPrefix}.projectName`}
              label={i18next.t("Project name")}
              placeholder={i18next.t("Write down name of project.")}
            />
            <TextField
              className="rel-mt-1"
              width={16}
              fieldPath={`${fieldPathPrefix}.fundingProgram`}
              label={i18next.t("Funding program")}
              placeholder={i18next.t(
                "Write the name of research program in which the project was funded."
              )}
            />
            <LocalVocabularySelectField
              className="rel-mt-1"
              width={16}
              fieldPath={`${fieldPathPrefix}.funder`}
              label={i18next.t("Funder")}
              optionsListName="funders"
              clearable
              required
              placeholder={i18next.t(
                "Start writing the name of the provider and then choose from the list."
              )}
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

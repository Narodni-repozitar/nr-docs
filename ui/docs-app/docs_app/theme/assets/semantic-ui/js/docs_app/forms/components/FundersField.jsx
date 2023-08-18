import React from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon } from "semantic-ui-react";
import { ArrayField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { LocalVocabularySelectField } from "./LocalVocabularySelectField";
import { GroupErrorMessage } from "./GroupErrorMessage";

export const FundersField = ({ fieldPath, helpText }) => {
  return (
    <React.Fragment>
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
            <React.Fragment>
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

              <Form.Field className="rel-mt-1 rel-mb-1">
                <Button
                  aria-label={i18next.t("Remove field")}
                  className="close-btn"
                  icon
                  onClick={() => arrayHelpers.remove(indexPath)}
                >
                  <Icon name="close" />
                </Button>
              </Form.Field>
            </React.Fragment>
          );
        }}
      </ArrayField>
      <GroupErrorMessage fieldPath={fieldPath} />
    </React.Fragment>
  );
};

FundersField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

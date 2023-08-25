import React from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon } from "semantic-ui-react";
import { ArrayField, TextField, GroupField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { LocalVocabularySelectField } from "./LocalVocabularySelectField";
import { GroupErrorMessage } from "./GroupErrorMessage";
import { useHighlightState } from "../hooks";

export const FundersField = ({ fieldPath, helpText }) => {
  const { highlightedStates, handleHover, handleMouseLeave } =
    useHighlightState();
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
            <GroupField
              className={
                highlightedStates[indexPath]
                  ? "highlighted invenio-group-field"
                  : "invenio-group-field"
              }
            >
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

              <Form.Field>
                <Button
                  aria-label={i18next.t("Remove field")}
                  className="close-btn"
                  icon
                  onClick={() => {
                    arrayHelpers.remove(indexPath);
                    handleMouseLeave(indexPath);
                  }}
                  onMouseEnter={() => handleHover(indexPath)}
                  onMouseLeave={() => handleMouseLeave(indexPath)}
                >
                  <Icon name="close" />
                </Button>
              </Form.Field>
            </GroupField>
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

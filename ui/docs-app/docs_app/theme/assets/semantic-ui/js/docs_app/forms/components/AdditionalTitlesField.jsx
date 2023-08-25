import React, { useState } from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon } from "semantic-ui-react";
import { ArrayField, SelectField, GroupField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { I18nTextInputField } from "@js/oarepo_ui";
import { GroupErrorMessage } from "./GroupErrorMessage";
import { useHighlightState } from "../hooks";

// this should come from formConfig in the actual use case?
const subtitleTypes = [
  { text: "Alternative title", value: "alternativeTitle" },
  { text: "Translated title", value: "translatedTitle" },
  { text: "Subtitle", value: "subtitle" },
  { text: "Other", value: "other" },
];

export const AdditionalTitlesField = ({ fieldPath }) => {
  const { highlightedStates, handleHover, handleMouseLeave } =
    useHighlightState();

  return (
    <React.Fragment>
      <ArrayField
        addButtonLabel={i18next.t("Add additional title")}
        defaultNewValue={{}}
        fieldPath={fieldPath}
        label={i18next.t("Additional titles")}
        labelIcon="pencil"
        className="additional-titles"
      >
        {({ arrayHelpers, indexPath }) => {
          const fieldPathPrefix = `${fieldPath}.${indexPath}`;
          return (
            <GroupField
              border
              className={
                highlightedStates[indexPath]
                  ? "highlighted invenio-group-field"
                  : "invenio-group-field"
              }
            >
              <Form.Field width={13}>
                <I18nTextInputField
                  fieldPath={`${fieldPathPrefix}.title`}
                  label={i18next.t("Title")}
                  required
                />
              </Form.Field>
              <Form.Field style={{ marginTop: "1.5rem" }} width={3}>
                <SelectField
                  fieldPath={`${fieldPathPrefix}.titleType`}
                  label={i18next.t("Title type")}
                  optimized
                  options={subtitleTypes}
                  required
                />
              </Form.Field>

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

AdditionalTitlesField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};

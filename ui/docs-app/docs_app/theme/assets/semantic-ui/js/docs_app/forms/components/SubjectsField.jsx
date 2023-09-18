import React from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon } from "semantic-ui-react";
import { ArrayField, SelectField, GroupField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { MultilingualTextInput, useHighlightState } from "@js/oarepo_ui";

const options = [{ value: "keyword", text: "Keyword" }];

export const SubjectsField = ({ fieldPath, helpText }) => {
  const { highlightedStates, handleHover, handleMouseLeave } =
    useHighlightState();
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add subject")}
      fieldPath={fieldPath}
      label={i18next.t("Subjects")}
      labelIcon="pencil"
      helpText={helpText}
      className="subjects"
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <GroupField
            className={
              highlightedStates[indexPath]
                ? "subjects highlighted invenio-group-field"
                : "subjects invenio-group-field"
            }
          >
            <SelectField
              clearable
              width={4}
              fieldPath={`${fieldPathPrefix}.subjectScheme`}
              label={i18next.t("Subject scheme")}
              required
              options={options}
            />
            <Form.Field style={{ marginTop: 0 }} width={12}>
              <MultilingualTextInput
                hasHighlighting
                fieldPath={`${fieldPathPrefix}.subject`}
                label=""
                lngFieldWidth={5}
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
  );
};

SubjectsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

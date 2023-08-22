import React from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon } from "semantic-ui-react";
import { ArrayField, SelectField, GroupField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { MultilingualTextInput } from "@js/oarepo_ui";

const options = [{ value: "keyword", text: "Keyword" }];
// TODO: still not fully clear on this input

export const SubjectsField = ({ fieldPath, helpText }) => {
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
          <GroupField>
            <SelectField
              // style={{ marginTop: "0.5rem" }}
              clearable
              width={4}
              fieldPath={`${fieldPathPrefix}.subjectScheme`}
              label={i18next.t("Subject scheme")}
              required
              options={options}
            />
            <Form.Field style={{ marginTop: 0 }} width={12}>
              <MultilingualTextInput
                fieldPath={`${fieldPathPrefix}.subject`}
                label=""
              />
            </Form.Field>

            <Form.Field>
              <Button
                aria-label={i18next.t("Remove field")}
                icon
                onClick={() => arrayHelpers.remove(indexPath)}
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

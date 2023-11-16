import React from "react";
import PropTypes from "prop-types";
import { Form } from "semantic-ui-react";
import { ArrayField, SelectField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { MultilingualTextInput, ArrayFieldItem } from "@js/oarepo_ui";

const options = [{ value: "keyword", text: "Keyword" }];

export const SubjectsField = ({ fieldPath, helpText, defaultNewValue }) => {
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add subject")}
      fieldPath={fieldPath}
      label={i18next.t("Subjects")}
      labelIcon="pencil"
      helpText={helpText}
      defaultNewValue={defaultNewValue}
    >
      {({ arrayHelpers, indexPath, array }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <ArrayFieldItem
            indexPath={indexPath}
            arrayHelpers={arrayHelpers}
            className={"invenio-group-field subjects"}
          >
            <SelectField
              width={5}
              fieldPath={`${fieldPathPrefix}.subjectScheme`}
              label={i18next.t("Subject scheme")}
              required
              options={options}
            />
            <Form.Field style={{ marginTop: 0 }} width={12}>
              {array[indexPath].subjectScheme === "keyword" && (
                <MultilingualTextInput
                  fieldPath={`${fieldPathPrefix}.subject`}
                  lngFieldWidth={5}
                  textFieldLabel={i18next.t("Subject")}
                  required
                  showEmptyValue
                />
              )}
            </Form.Field>
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

SubjectsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
  defaultNewValue: PropTypes.object,
};

SubjectsField.defaultProps = {
  defaultNewValue: { subjectScheme: "keyword" },
};

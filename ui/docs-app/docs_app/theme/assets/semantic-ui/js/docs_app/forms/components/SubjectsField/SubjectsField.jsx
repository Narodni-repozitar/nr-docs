import React from "react";
import PropTypes from "prop-types";
import { Form } from "semantic-ui-react";
import { ArrayField, SelectField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { MultilingualTextInput, ArrayFieldItem } from "@js/oarepo_ui";

const options = [{ value: "keyword", text: "Keyword" }];

export const SubjectsField = ({ fieldPath, helpText }) => {
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add subject")}
      fieldPath={fieldPath}
      label={i18next.t("Subjects")}
      labelIcon="pencil"
      helpText={helpText}
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
              clearable
              width={5}
              fieldPath={`${fieldPathPrefix}.subjectScheme`}
              label={i18next.t("Subject scheme")}
              required
              options={options}
            />
            {/* TODO: I don't see a reasonable way to set default value as keyword in the select field
            even if you set it, it is not reflected in formik state, so it causes problems. I think this is a reasonable solution for now
            until we determine from what other sources we should also be offering keywords and how the input should be */}
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
};

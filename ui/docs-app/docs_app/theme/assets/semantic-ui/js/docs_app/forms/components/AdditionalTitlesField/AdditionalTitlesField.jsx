import React from "react";
import PropTypes from "prop-types";
import { Form } from "semantic-ui-react";
import { ArrayField, SelectField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { I18nTextInputField, ArrayFieldItem } from "@js/oarepo_ui";

const subtitleTypes = [
  { text: "Alternative title", value: "alternativeTitle" },
  { text: "Translated title", value: "translatedTitle" },
  { text: "Subtitle", value: "subtitle" },
  { text: "Other", value: "other" },
];

export const AdditionalTitlesField = ({ fieldPath }) => {
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add additional title")}
      defaultNewValue={{}}
      fieldPath={fieldPath}
      label={i18next.t("Additional titles")}
      labelIcon="pencil"
      className="additional-titles"
    >
      {({ arrayHelpers, indexPath, array }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <ArrayFieldItem
            indexPath={indexPath}
            array={array}
            arrayHelpers={arrayHelpers}
          >
            <Form.Field width={13}>
              <I18nTextInputField
                fieldPath={`${fieldPathPrefix}.title`}
                label={i18next.t("Title")}
                required
                lngFieldWidth={4}
                className=""
              />
            </Form.Field>
            <Form.Field width={3}>
              <SelectField
                fieldPath={`${fieldPathPrefix}.titleType`}
                label={i18next.t("Title type")}
                optimized
                options={subtitleTypes}
                required
              />
            </Form.Field>
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

AdditionalTitlesField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};
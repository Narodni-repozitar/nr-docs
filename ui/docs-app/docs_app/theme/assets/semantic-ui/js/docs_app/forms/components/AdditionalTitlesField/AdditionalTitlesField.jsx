import React from "react";
import PropTypes from "prop-types";
import { Form } from "semantic-ui-react";
import { ArrayField, SelectField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import {
  I18nTextInputField,
  ArrayFieldItem,
  useDefaultLocale,
  useFormFieldValue,
} from "@js/oarepo_ui";

const subtitleTypes = [
  { text: "Alternative title", value: "alternativeTitle" },
  { text: "Translated title", value: "translatedTitle" },
  { text: "Subtitle", value: "subtitle" },
  { text: "Other", value: "other" },
];

export const AdditionalTitlesField = ({ fieldPath }) => {
  const { defaultLocale } = useDefaultLocale();
  const initialValueObj = {
    title: {
      value: "",
    },
  };
  const { defaultNewValue } = useFormFieldValue({
    defaultValue: defaultLocale,
    fieldPath,
    subValuesPath: "title.lang",
    subValuesUnique: false,
  });

  return (
    <ArrayField
      addButtonLabel={i18next.t("Add additional title")}
      defaultNewValue={defaultNewValue(initialValueObj)}
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
            <Form.Field width={12}>
              <I18nTextInputField
                fieldPath={`${fieldPathPrefix}.title`}
                label={i18next.t("Title")}
                required
                lngFieldWidth={5}
                className=""
              />
            </Form.Field>
            <Form.Field width={4}>
              <SelectField
                fieldPath={`${fieldPathPrefix}.titleType`}
                label={i18next.t("Title type")}
                optimized
                options={subtitleTypes}
                required
                clearable
                width={16}
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

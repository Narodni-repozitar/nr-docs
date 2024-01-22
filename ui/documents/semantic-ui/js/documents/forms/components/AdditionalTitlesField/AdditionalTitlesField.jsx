import React from "react";
import PropTypes from "prop-types";
import { Form } from "semantic-ui-react";
import { ArrayField, SelectField } from "react-invenio-forms";
import { i18next } from "@translations/i18next";
import {
  I18nTextInputField,
  ArrayFieldItem,
  useDefaultLocale,
  useFormFieldValue,
} from "@js/oarepo_ui";

const subtitleTypes = [
  { text: i18next.t("Alternative title"), value: "alternativeTitle" },
  { text: i18next.t("Translated title"), value: "translatedTitle" },
  { text: i18next.t("Subtitle"), value: "subtitle" },
  { text: i18next.t("Other"), value: "other" },
];

export const AdditionalTitlesField = ({
  fieldPath,
  helpText,
  prefillLanguageWithDefaultLocale,
  defaultNewValue,
}) => {
  const { defaultLocale } = useDefaultLocale();
  const initialValueObj = {
    title: {
      value: "",
    },
  };
  const { defaultNewValue: getNewValue } = useFormFieldValue({
    defaultValue: defaultLocale,
    fieldPath,
    subValuesPath: "title.lang",
    subValuesUnique: false,
  });

  return (
    <ArrayField
      addButtonLabel={i18next.t("Add additional title")}
      defaultNewValue={
        prefillLanguageWithDefaultLocale
          ? getNewValue(initialValueObj)
          : defaultNewValue
      }
      fieldPath={fieldPath}
      label={i18next.t("Additional titles")}
      labelIcon="pencil"
      className="additional-titles"
      helpText={helpText}
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
                selectOnBlur={false}
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
  helpText: PropTypes.string,
  prefillLanguageWithDefaultLocale: PropTypes.bool,
  defaultNewValue: PropTypes.object,
};

AdditionalTitlesField.defaultProps = {
  helpText: i18next.t(
    "If the title is given in other languages, choose the type of title and corresponding language."
  ),
  prefillLanguageWithDefaultLocale: false,
  defaultNewValue: {
    title: {
      value: "",
      lang: "",
    },
    titleType: "",
  },
};

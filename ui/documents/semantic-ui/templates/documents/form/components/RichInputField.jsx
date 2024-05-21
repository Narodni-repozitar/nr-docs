import React from "react";
import PropTypes from "prop-types";
import { ArrayField } from "react-invenio-forms";
import { Form } from "semantic-ui-react";
import {
  I18nTextInputField,
  I18nRichInputField,
  ArrayFieldItem,
  useDefaultLocale,
  useFormFieldValue,
  useShowEmptyValue,
} from "@js/oarepo_ui";
import { i18next } from "@translations/oarepo_ui/i18next";
import { useFormikContext, getIn } from "formik";
import { LanguageSelectField } from "@js/oarepo_ui";
import { FieldLabel } from "react-invenio-forms";
import { RichInputField, GroupField } from "react-invenio-forms";
import { decode } from "html-entities";

export const InputSanit = ({
  fieldPath,
  label,
  labelIcon,
  required,
  defaultNewValue,
  rich,
  editorConfig,
  textFieldLabel,
  textFieldIcon,
  helpText,
  addButtonLabel,
  lngFieldWidth,
  showEmptyValue,
  prefillLanguageWithDefaultLocale,
  ...uiProps
}) => {
  const { defaultLocale } = useDefaultLocale();
  const { values } = useFormikContext();
  const { usedSubValues, defaultNewValue: getNewValue } = useFormFieldValue({
    defaultValue: defaultLocale,
    fieldPath,
    subValuesPath: "lang",
  });
  const value = getIn(values, fieldPath);
  const usedLanguages = usedSubValues(value);

  const {  setFieldValue, setFieldTouched } = useFormikContext();

  const convertHTMLToTags = (htmlString) => {
    const regex = /<(?!\/?(strong|b|div|br|p|i|li)\b)[^>]*>[^<]*<\/.*?>/gi;
    const decodedString = decode(htmlString);
    const cleanedContent = decodedString.replace(regex, "");
    const noTags = cleanedContent.replace(/<[^>]*>?/gm, "");
    return noTags;
  };

  useShowEmptyValue(fieldPath, defaultNewValue, showEmptyValue);
  return (
    <ArrayField
      addButtonLabel={addButtonLabel}
      defaultNewValue={
        prefillLanguageWithDefaultLocale
          ? getNewValue(defaultNewValue, usedLanguages)
          : defaultNewValue
      }
      fieldPath={fieldPath}
      label={
        <FieldLabel htmlFor={fieldPath} icon={labelIcon ?? ""} label={label} />
      }
      helpText={helpText}
    >
      {({ indexPath, array, arrayHelpers }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <ArrayFieldItem
            indexPath={indexPath}
            array={array}
            arrayHelpers={arrayHelpers}
          >
            <Form.Field width={16}>
              <GroupField fieldPath={fieldPath} optimized>
                <LanguageSelectField
                  fieldPath={`${fieldPath}.lang`}
                  required
                  width={lngFieldWidth}
                  usedLanguages={usedLanguages}
                />
                <Form.Field width={13}>
                  <RichInputField
                    editorConfig={editorConfig}
                    className={`${!label ? "mt-25" : ""}`}
                    fieldPath={`${fieldPath}.value`}
                    label={
                      <FieldLabel
                        htmlFor={`${fieldPathPrefix}.value`}
                        icon={labelIcon}
                        label={label}
                      />
                    }
                    required={required}
                    optimized={optimized}
                    placeholder={placeholder}
                    editor={
                      <RichEditor
                        value={fieldPathPrefix}
                        optimized
                        editorConfig={{
                          toolbar:
                            "bold italic | bullist numlist | outdent indent | undo redo",
                          valid_elements: "strong,b,div,br,p,i,li",
                          invalid_elements: "style",
                        }}
                        onBlur={async (event, editor) => {
                          const cleanedContent = await convertHTMLToTags(
                            editor.getContent()
                          );

                          const updatedAbstracts = [
                            ...values.metadata.abstract,
                          ];
                          updatedAbstracts[indexPath] = cleanedContent;

                          setFieldValue("metadata.abstract", updatedAbstracts);
                          setFieldTouched(
                            `metadata.abstract.${indexPath}`,
                            true
                          );
                        }}
                      />
                    }
                    {...uiProps}
                  />
                </Form.Field>
              </GroupField>
            </Form.Field>
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

MultilingualTextInput.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.string,
  labelIcon: PropTypes.string,
  required: PropTypes.bool,
  hasRichInput: PropTypes.bool,
  editorConfig: PropTypes.object,
  textFieldLabel: PropTypes.string,
  textFieldIcon: PropTypes.string,
  helpText: PropTypes.string,
  addButtonLabel: PropTypes.string,
  lngFieldWidth: PropTypes.number,
  rich: PropTypes.bool,
  defaultNewValue: PropTypes.object,
  showEmptyValue: PropTypes.bool,
  prefillLanguageWithDefaultLocale: PropTypes.bool,
};

MultilingualTextInput.defaultProps = {
  defaultNewValue: {
    lang: "",
    value: "",
  },
  rich: false,
  label: undefined,
  addButtonLabel: i18next.t("Add another language"),
  showEmptyValue: false,
  prefillLanguageWithDefaultLocale: false,
};

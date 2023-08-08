import React, { useEffect } from "react";
import PropTypes from "prop-types";
import {
  TextField,
  GroupField,
  ArrayField,
  FieldLabel,
  SelectField,
  RichInputField,
} from "react-invenio-forms";
import { Button, Form, Icon, Popup } from "semantic-ui-react";
import { useFormikContext, getIn } from "formik";
import _toPairs from "lodash/toPairs";
import { useFormConfig } from "@js/oarepo_ui/forms";
import { i18next } from "@translations/oarepo_ui/i18next";

const translateObjectToArray = (obj) => {
  return _toPairs(obj).map(([language, title]) => ({ language, name: title }));
};

export const transformArrayToObject = (arr) => {
  const result = {};

  arr.forEach((obj) => {
    const { language, name } = obj;
    result[language] = name;
  });

  return result;
};

const eliminateUsedLanguages = (excludeIndex, languageOptions, fieldArray) => {
  const currentlySelectedLanguage = fieldArray[excludeIndex].language;

  const excludedLanguages = fieldArray.filter(
    (item) => item.language !== currentlySelectedLanguage && item.language
  );

  const remainingLanguages = languageOptions.filter(
    (option) =>
      !excludedLanguages.map((item) => item.language).includes(option.value)
  );
  return remainingLanguages;
};

export const MultiLingualTextInput = ({
  fieldPath,
  label,
  labelIcon,
  required,
  emptyNewInput,
  newItemInitialValue,
  hasRichInput,
  editorConfig,
}) => {
  const {
    formConfig: {
      vocabularies: { languages },
    },
  } = useFormConfig();

  const placeholderFieldPath = `_${fieldPath}`;
  const { setFieldValue, values } = useFormikContext();
  useEffect(() => {
    if (!getIn(values, placeholderFieldPath)) {
      setFieldValue(
        placeholderFieldPath,
        getIn(values, fieldPath)
          ? translateObjectToArray(getIn(values, fieldPath, ""))
          : translateObjectToArray(newItemInitialValue)
      );
      return;
    }
    setFieldValue(
      fieldPath,
      transformArrayToObject(getIn(values, placeholderFieldPath))
    );
  }, [values[placeholderFieldPath]]);

  return (
    <ArrayField
      addButtonLabel="Add another language"
      defaultNewValue={emptyNewInput}
      fieldPath={placeholderFieldPath}
      label={
        <FieldLabel htmlFor={fieldPath} icon={labelIcon ?? ""} label={label} />
      }
      required={required}
    >
      {({ indexPath, array, arrayHelpers }) => {
        const fieldPathPrefix = `${placeholderFieldPath}.${indexPath}`;

        const availableOptions = eliminateUsedLanguages(
          indexPath,
          languages,
          array
        );

        return (
          <GroupField optimized>
            <Form.Field width={3}>
              <SelectField
                // necessary because otherwise other inputs are not rerendered and keep the previous state i.e. I could potentially choose two same languages in some scenarios
                key={availableOptions}
                clearable
                fieldPath={`${fieldPathPrefix}.language`}
                label="Language"
                optimized
                options={availableOptions}
                required={required}
                selectOnBlur={false}
                search
              />
              {indexPath > 0 && hasRichInput && (
                <Popup
                  basic
                  inverted
                  position="bottom center"
                  content={i18next.t("Remove description")}
                  trigger={
                    <Button
                      aria-label="remove field"
                      className="rel-mt-1"
                      icon
                      onClick={() => arrayHelpers.remove(indexPath)}
                      fluid
                    >
                      <Icon name="close" />
                    </Button>
                  }
                />
              )}
            </Form.Field>

            {hasRichInput ? (
              <Form.Field width={13}>
                <RichInputField
                  fieldPath={`${fieldPathPrefix}.name`}
                  label={i18next.t("Description")}
                  editorConfig={editorConfig}
                  optimized
                  required={required}
                />
              </Form.Field>
            ) : (
              <TextField
                fieldPath={`${fieldPathPrefix}.name`}
                label="Name"
                required={required}
                width={13}
                icon={
                  indexPath > 0 ? (
                    <Popup
                      basic
                      inverted
                      position="bottom center"
                      content={i18next.t("Remove field")}
                      trigger={
                        <Icon
                          as="button"
                          onClick={() => arrayHelpers.remove(indexPath)}
                        >
                          <Icon name="close" />
                        </Icon>
                      }
                    />
                  ) : null
                }
                iconPosition="right"
              />
            )}
          </GroupField>
        );
      }}
    </ArrayField>
  );
};

MultiLingualTextInput.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.string,
  labelIcon: PropTypes.string,
  required: PropTypes.bool,
  newItemInitialValue: PropTypes.object,
  hasRichInput: PropTypes.bool,
  editorConfig: PropTypes.object,
};

MultiLingualTextInput.defaultProps = {
  label: "Title",
  required: undefined,
  emptyNewInput: {
    language: "",
    name: "",
  },
  newItemInitialValue: { cs: "" },
  hasRichInput: false,
  editorConfig: {
    removePlugins: [
      "Image",
      "ImageCaption",
      "ImageStyle",
      "ImageToolbar",
      "ImageUpload",
      "MediaEmbed",
      "Table",
      "TableToolbar",
      "TableProperties",
      "TableCellProperties",
    ],
  },
};

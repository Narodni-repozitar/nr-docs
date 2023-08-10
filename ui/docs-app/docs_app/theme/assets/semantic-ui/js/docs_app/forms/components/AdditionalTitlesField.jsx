import React, { useEffect, useMemo } from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon } from "semantic-ui-react";
import { ArrayField, GroupField, SelectField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { useFormConfig, MultiLingualTextInput } from "@js/oarepo_ui";
import { useFormikContext, getIn } from "formik";

// the final state of the component contains array of objects and the objects also contain the _title (placeholder representation for multilingual field) and this shall
// ne removed before form submitting

export const transformArrayToObject = (arr) => {
  if (!Array.isArray(arr)) return;
  const result = {};
  arr.forEach(({ language, name }) => {
    result[language] = name;
  });

  return result;
};

// this should come from formConfig in the actual use case
const subtitleTypes = [
  { text: "Alternative title", value: "alternative-title" },
  { text: "Translated title", value: "translated-title" },
  { text: "Subtitle", value: "subtitle" },
  { text: "Other", value: "other" },
];

export const AdditionalTitlesField = ({ fieldPath }) => {
  const { values, setFieldValue } = useFormikContext();
  // as it is a nested structure, I had to use useMemo to avoid infinite rerenders
  const titlesState = useMemo(() => {
    if (!values.additionalTitles) return;
    return JSON.stringify(values.additionalTitles.map((item) => item._title));
  }, [values.additionalTitles]);

  useEffect(() => {
    if (!getIn(values, `${fieldPath}.0._title`)) return;
    setFieldValue(
      `${fieldPath}`,
      getIn(values, fieldPath, []).map(({ title, titleType, _title }) => {
        return {
          title: transformArrayToObject(_title),
          titleType,
          _title,
        };
      })
    );
  }, [titlesState]);

  return (
    <ArrayField
      addButtonLabel={i18next.t("Add additional title")}
      defaultNewValue={{}}
      fieldPath={fieldPath}
      className="additional-titles"
      label={i18next.t("Additional titles")}
      labelIcon="pencil"
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <GroupField>
            <Form.Field width={13}>
              <MultiLingualTextInput
                fieldPath={`${fieldPathPrefix}.title`}
                label=""
                textFieldLabel={i18next.t("Title")}
              />
            </Form.Field>
            <Form.Field style={{ marginTop: "0.3rem" }} width={3}>
              <SelectField
                fieldPath={`${fieldPathPrefix}.titleType`}
                label={i18next.t("Title type")}
                optimized
                options={subtitleTypes}
              />
            </Form.Field>

            <Form.Field style={{ marginTop: "2rem" }}>
              <Button
                aria-label={i18next.t("Remove field")}
                className="close-btn"
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

AdditionalTitlesField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};

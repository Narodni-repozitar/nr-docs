import React, { useEffect } from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon, Container } from "semantic-ui-react";
import {
  ArrayField,
  GroupField,
  SelectField,
  TextField,
} from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { useFormConfig, MultiLingualTextInput } from "@js/oarepo_ui";
import { useFormikContext, getIn } from "formik";

export const transformArrayToObject = (arr) => {
  const result = {};
  arr.forEach(({ language, name }) => {
    result[language] = name;
  });

  return result;
};

const subtitleTypes = [
  { text: "Alternative title", value: "alternative-title" },
  { text: "Translated title", value: "translated-title" },
  { text: "Subtitle", value: "subtitle" },
  { text: "Other", value: "other" },
];

export const AdditionalTitlesField = ({ fieldPath, options }) => {
  const { values, setFieldValue } = useFormikContext();

  useEffect(() => {
    setFieldValue(
      fieldPath,
      getIn(values, `_${fieldPath}`, []).map(({ title, titleType }) => ({
        title: transformArrayToObject(title),
        titleType: titleType,
      }))
    );
  }, [values[`_${fieldPath}`]]);

  return (
    <ArrayField
      addButtonLabel={i18next.t("Add titles")}
      defaultNewValue={{}}
      fieldPath={fieldPath}
      className="additional-titles"
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        console.log(fieldPathPrefix);
        return (
          <GroupField>
            <Form.Field width={13}>
              <MultiLingualTextInput
                fieldPath={`${fieldPathPrefix}.title`}
                label="Additional title"
                required
              />
            </Form.Field>
            <Form.Field width={3}>
              <SelectField
                style={{ marginTop: "2rem" }}
                fieldPath={`_${fieldPathPrefix}.titleType`}
                label="Type"
                optimized
                options={subtitleTypes}
                required
              />
            </Form.Field>

            <Form.Field style={{ marginTop: "3.5rem" }}>
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
  options: PropTypes.shape({
    type: PropTypes.arrayOf(
      PropTypes.shape({
        icon: PropTypes.string,
        text: PropTypes.string,
        value: PropTypes.string,
      })
    ),
    lang: PropTypes.arrayOf(
      PropTypes.shape({
        text: PropTypes.string,
        value: PropTypes.string,
      })
    ),
  }),
  recordUI: PropTypes.object,
};

AdditionalTitlesField.defaultProps = {
  options: undefined,
  recordUI: undefined,
};

// <ArrayField
// addButtonLabel={i18next.t("Add titles")}
// defaultNewValue={{}}
// fieldPath={fieldPath}
// className="additional-titles"
// >
// {({ arrayHelpers, indexPath }) => {
//   const fieldPathPrefix = `${fieldPath}.${indexPath}`;

//   return (
//     <GroupField fieldPath={fieldPath} optimized>
//       <MultiLingualTextInput
//         fieldPath={`${fieldPathPrefix}.title`}
//         label="Additional title"
//         required
//         width={10}
//       />
//       <SelectField
//         fieldPath={`${fieldPathPrefix}.type`}
//         label="Type"
//         optimized
//         options={subtitleTypes}
//         required
//         width={3}
//       />

//       <Form.Field>
//         <Button
//           aria-label={i18next.t("Remove field")}
//           className="close-btn"
//           icon
//           onClick={() => arrayHelpers.remove(indexPath)}
//         >
//           <Icon name="close" />
//         </Button>
//       </Form.Field>
//     </GroupField>
//   );
// }}
// </ArrayField>

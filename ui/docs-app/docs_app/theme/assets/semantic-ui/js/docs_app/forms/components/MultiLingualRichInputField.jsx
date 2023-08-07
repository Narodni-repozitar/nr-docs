import React, { useEffect } from "react";
import PropTypes from "prop-types";
import {
  ArrayField,
  FieldLabel,
  SelectField,
  RichInputField,
} from "react-invenio-forms";
import { i18next } from "@translations/oarepo_ui/i18next";
import { useFormikContext, getIn } from "formik";
import { Form, Button, Icon, Grid } from "semantic-ui-react";
import _toPairs from "lodash/toPairs";
import _get from "lodash/get";

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

export const MultiLingualRichInputField = ({
  fieldPath,
  label,
  required,
  options,
  editorConfig,
  newItemInitialValue,
  addButtonLabel,
  helpText,
  labelIcon,
}) => {
  const placeholderFieldPath = `_${fieldPath}`;
  const { setFieldValue, values } = useFormikContext();
  const abstractValue = _get(values, placeholderFieldPath);

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
  }, [abstractValue]);

  return (
    <ArrayField
      addButtonLabel={addButtonLabel}
      fieldPath={placeholderFieldPath}
      label={label}
      required={required}
      helpText={helpText}
      labelIcon={labelIcon}
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${placeholderFieldPath}.${indexPath}`;

        return (
          <Grid>
            <Grid.Row stretched>
              <Grid.Column width={12}>
                <RichInputField
                  fieldPath={`${fieldPathPrefix}.name`}
                  label={i18next.t("Description")}
                  editorConfig={editorConfig}
                  optimized
                  required
                />
              </Grid.Column>
              <Grid.Column width={3}>
                <SelectField
                  clearable
                  fieldPath={`${fieldPathPrefix}.language`}
                  label={i18next.t("Language")}
                  options={options.languages}
                  required
                />
                <Form.Field>
                  {indexPath > 0 && (
                    <Button
                      fluid
                      style={{ marginTop: "1.75rem" }}
                      aria-label="remove field"
                      className="close-btn"
                      icon
                      onClick={() => arrayHelpers.remove(indexPath)}
                    >
                      <Icon name="close" />
                    </Button>
                  )}
                </Form.Field>
              </Grid.Column>
            </Grid.Row>
          </Grid>
        );
      }}
    </ArrayField>
  );
};

MultiLingualRichInputField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  options: PropTypes.shape({
    languages: PropTypes.arrayOf(
      PropTypes.shape({
        key: PropTypes.string,
        text: PropTypes.string,
        value: PropTypes.string,
      })
    ).isRequired,
  }).isRequired,
  editorConfig: PropTypes.object.isRequired,
  newItemInitialValue: PropTypes.object,
  addButtonLabel: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  helpText: PropTypes.string,
  labelIcon: PropTypes.string,
};

MultiLingualRichInputField.defaultProps = {
  addButtonLabel: i18next.t("Add description in another language"),
  newItemInitialValue: { cs: "" },
  labelIcon: "pencil square",
};

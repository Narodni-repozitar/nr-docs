import React, { useEffect } from "react";
import PropTypes from "prop-types";
import { ArrayField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/oarepo_ui/i18next";
import { useFormikContext, getIn } from "formik";
import { Form, Button, Icon, Grid } from "semantic-ui-react";
import _toPairs from "lodash/toPairs";
import _get from "lodash/get";

const arrayToArrayOfObjects = (arr) => {
  return arr.map((item) => ({ note: item }));
};

export const transformArrayToObject = (arr) => {
  return arr.map((item) => item.note);
};

export const NotesField = ({
  fieldPath,
  label,
  required,
  newItemInitialValue,
  addButtonLabel,
  helpText,
  labelIcon,
}) => {
  const placeholderFieldPath = `_${fieldPath}`;
  const { setFieldValue, values } = useFormikContext();

  useEffect(() => {
    if (!getIn(values, placeholderFieldPath)) {
      setFieldValue(
        placeholderFieldPath,
        getIn(values, fieldPath)
          ? arrayToArrayOfObjects(getIn(values, fieldPath, ""))
          : arrayToArrayOfObjects(newItemInitialValue)
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
                <TextField
                  fieldPath={`${fieldPathPrefix}.note`}
                  label={i18next.t("Description")}
                  optimized
                  required
                  fluid
                />
              </Grid.Column>
              <Grid.Column width={3}>
                <Form.Field>
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
                </Form.Field>
              </Grid.Column>
            </Grid.Row>
          </Grid>
        );
      }}
    </ArrayField>
  );
};

NotesField.propTypes = {
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

NotesField.defaultProps = {
  addButtonLabel: i18next.t("Add description in another language"),
  newItemInitialValue: "",
  labelIcon: "pencil square",
};

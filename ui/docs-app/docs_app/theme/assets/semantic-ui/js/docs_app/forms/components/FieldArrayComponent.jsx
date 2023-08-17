import React from "react";
import PropTypes from "prop-types";
import { getIn, FieldArray, useFormikContext } from "formik";
import { Form, Icon } from "semantic-ui-react";
import _isEmpty from "lodash/isEmpty";
import { FieldLabel } from "react-invenio-forms";

export const FieldArrayComponent = ({
  addButtonLabel,
  children,
  defaultNewValue,
  fieldPath,
  label,
  labelIcon,
  helpText,
  showEmptyValue,
}) => {
  const { values } = useFormikContext();
  const getValues = (values) => {
    const existingValues = getIn(values, fieldPath, []);
    if (showEmptyValue && _isEmpty(existingValues)) {
      existingValues.push(defaultNewValue);
    }
    return existingValues;
  };

  const renderFormField = (arrayHelpers) => {
    const valuesToDisplay = getValues(values);

    return (
      <Form.Field>
        <FieldLabel htmlFor={fieldPath} icon={labelIcon} label={label} />

        {valuesToDisplay.map((value, index, array) => {
          const arrayPath = fieldPath;
          const indexPath = index;

          return (
            <div key={index}>
              {children({
                array,
                arrayHelpers,
                arrayPath,
                indexPath,
                value,
              })}
            </div>
          );
        })}

        <label className="helptext">{helpText}</label>

        <Form.Group>
          <Form.Button
            type="button"
            icon
            labelPosition="left"
            onClick={() => {
              arrayHelpers.push(defaultNewValue);
            }}
          >
            <Icon name="add" />
            {addButtonLabel}
          </Form.Button>
        </Form.Group>
      </Form.Field>
    );
  };

  return <FieldArray name={fieldPath} render={renderFormField} />;
};

FieldArrayComponent.propTypes = {
  addButtonLabel: PropTypes.string,
  children: PropTypes.func.isRequired,
  defaultNewValue: PropTypes.oneOfType([PropTypes.string, PropTypes.object])
    .isRequired,
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
  labelIcon: PropTypes.string,
  requiredOptions: PropTypes.array,
  showEmptyValue: PropTypes.bool,
};

FieldArrayComponent.defaultProps = {
  addButtonLabel: "Add new row",
  helpText: "",
  label: "",
  labelIcon: "",
  showEmptyValue: false,
};

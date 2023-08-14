import * as React from "react";
import {
  TextField,
  GroupField,
  FieldLabel,
  SelectField,
} from "react-invenio-forms";
import PropTypes from "prop-types";

export const SubjectField = ({
  fieldPath,
  label,
  required,
  optimized,
  labelIcon,
  placeholder,
  ...uiProps
}) => {
  return (
    <GroupField fieldPath={fieldPath} optimized>
      <SelectField
        fieldPath={`${fieldPath}.subject`}
        placeholder=""
        required
        width={4}
      />
      <TextField
        // TODO: hacky fix for SUI alignment bug for case with
        // field groups with empty field label on one of inputs
        className={`${!label ? "mt-20" : ""}`}
        fieldPath={`${fieldPath}.value`}
        label={
          <FieldLabel
            htmlFor={`${fieldPath}.value`}
            icon={labelIcon}
            label={label}
          />
        }
        required={required}
        optimized={optimized}
        placeholder={placeholder}
        {...uiProps}
        width={14}
      />
    </GroupField>
  );
};

SubjectField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.string,
  labelIcon: PropTypes.string,
  required: PropTypes.bool,
  placeholder: PropTypes.string,
  error: PropTypes.any,
  helpText: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
  disabled: PropTypes.bool,
  optimized: PropTypes.bool,
};

SubjectField.defaultProps = {
  label: undefined,
  labelIcon: undefined,
  placeholder: undefined,
  error: undefined,
  helpText: "",
  disabled: false,
  optimized: true,
  required: false,
};

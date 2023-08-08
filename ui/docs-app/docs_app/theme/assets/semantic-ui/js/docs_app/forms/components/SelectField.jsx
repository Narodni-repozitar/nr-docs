// This file is part of React-Invenio-Forms
// Copyright (C) 2020 CERN.
// Copyright (C) 2020 Northwestern University.
//
// React-Invenio-Forms is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import PropTypes from "prop-types";
import { FastField, Field, getIn } from "formik";
import { Form } from "semantic-ui-react";
import isEmpty from "lodash/isEmpty";

export class SelectField extends Component {
  renderError = (errors, name, value, direction = "above") => {
    const { options } = this.props;
    let error = null;
    if (!Array.isArray(value)) {
      if (
        !isEmpty(options) &&
        !options.find((o) => o.value === value) &&
        !isEmpty(value)
      ) {
        error = `The current value "${value}" is invalid, please select another value.`;
      }
    }

    if (!error) {
      error = errors[name];
    }
    return error
      ? {
          content: error,
          pointing: direction,
        }
      : null;
  };

  renderFormField = (formikProps) => {
    const {
      form: {
        values,
        setFieldValue,
        handleBlur,
        errors,
        initialErrors,
        initialValues,
      },
      ...cmpProps
    } = formikProps;
    const {
      defaultValue,
      error,
      fieldPath,
      label,
      options,
      onChange,
      onAddItem,
      multiple,
      ...uiProps
    } = cmpProps;
    const _defaultValue = multiple ? [] : "";
    const value = getIn(values, fieldPath, defaultValue || _defaultValue);
    const initialValue = getIn(initialValues, fieldPath, _defaultValue);
    console.log(fieldPath);
    console.log(uiProps);
    return (
      <Form.Dropdown
        fluid
        className="invenio-select-field"
        selection
        error={
          error ||
          getIn(errors, fieldPath, null) ||
          // We check if initialValue changed to display the initialError,
          // otherwise it would be displayed despite updating the fieldu
          (initialValue === value && getIn(initialErrors, fieldPath, null))
        }
        id={fieldPath}
        label={{ children: label, htmlFor: fieldPath }}
        name={fieldPath}
        onBlur={handleBlur}
        onChange={(event, data) => {
          if (onChange) {
            onChange({ event, data, formikProps });
            event.target.value = "";
          } else {
            setFieldValue(fieldPath, data.value);
          }
        }}
        onAddItem={(event, data) => {
          if (onAddItem) {
            onAddItem({ event, data, formikProps });
          }
        }}
        options={options}
        value={value}
        multiple={multiple}
        {...uiProps}
      />
    );
  };

  render() {
    const { optimized, fieldPath, ...uiProps } = this.props;
    const FormikField = optimized ? FastField : Field;
    console.log(fieldPath);
    return (
      <FormikField
        name={fieldPath}
        component={this.renderFormField}
        fieldPath={fieldPath}
        {...uiProps}
      />
    );
  }
}

SelectField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  options: PropTypes.array.isRequired,
  defaultValue: PropTypes.oneOfType([PropTypes.string, PropTypes.array]),
  optimized: PropTypes.bool,
  error: PropTypes.any,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  onChange: PropTypes.func,
  onAddItem: PropTypes.func,
  multiple: PropTypes.bool,
};

SelectField.defaultProps = {
  defaultValue: "",
  optimized: false,
  error: undefined,
  label: "",
  onChange: undefined,
  onAddItem: undefined,
  multiple: false,
};

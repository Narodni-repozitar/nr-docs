import React, { useState } from "react";
import { SelectField } from "react-invenio-forms";
import { useFormConfig } from "@js/oarepo_ui/forms";
import { useFormikContext, getIn } from "formik";
import PropTypes from "prop-types";

export const LanguageSelectField = ({
  fieldPath,
  multiple,
  optionsListName,
  ...restProps
}) => {
  const {
    formConfig: {
      vocabularies: { languages },
    },
  } = useFormConfig();
  const { setFieldValue, values } = useFormikContext();
  return (
    <SelectField
      search
      fieldPath={fieldPath}
      multiple={true}
      {...restProps}
      options={languages}
      onChange={({ e, data, formikProps }) => {
        console.log(data.value);
        formikProps.form.setFieldValue(
          fieldPath,
          data.value.map((lng) => ({ id: lng }))
        );
      }}
      value={getIn(values, fieldPath, []).map((lng) => lng.id)}
    />
  );
};

LanguageSelectField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  multiple: PropTypes.bool,
  optionsListName: PropTypes.string.isRequired,
};

export default LanguageSelectField;

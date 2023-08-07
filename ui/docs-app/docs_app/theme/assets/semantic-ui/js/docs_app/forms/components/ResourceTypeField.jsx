import React from "react";
import PropTypes from "prop-types";
import _get from "lodash/get";
import { FieldLabel, SelectField } from "react-invenio-forms";
import { i18next } from "@translations/oarepo_vocabularies_ui/i18next";

export const ResourceTypeField = ({
  fieldPath,
  label,
  labelIcon,
  options,
  labelclassname,
  required,
  ...uiProps
}) => {
  const groupErrors = (errors, fieldPath) => {
    const fieldErrors = _get(errors, fieldPath);
    if (fieldErrors) {
      return { content: fieldErrors };
    }
    return null;
  };

  const createOptions = (propsOptions) => {
    return propsOptions
      .sort((o1, o2) =>
        o1.title[i18next.language].localeCompare(o2.title[i18next.language])
      )
      .map((o) => {
        return {
          value: o.id,
          key: o.id,
          text: o.title[i18next.language],
        };
      });
  };

  const frontEndOptions = createOptions(options);
  return (
    <SelectField
      fieldPath={fieldPath}
      label={<FieldLabel htmlFor={fieldPath} icon={labelIcon} label={label} />}
      optimized
      options={frontEndOptions}
      selectOnBlur={false}
      labelclassname={labelclassname}
      required={required}
      {...uiProps}
    />
  );
};

ResourceTypeField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.string,
  labelIcon: PropTypes.string,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.object,
      id: PropTypes.string,
    })
  ).isRequired,
  labelclassname: PropTypes.string,
  required: PropTypes.bool,
};

ResourceTypeField.defaultProps = {
  label: i18next.t("Resource type"),
  labelIcon: "tag",
  labelclassname: "field-label-class",
  required: false,
};

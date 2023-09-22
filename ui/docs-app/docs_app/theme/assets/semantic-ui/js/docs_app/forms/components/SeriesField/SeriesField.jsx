import React from "react";
import PropTypes from "prop-types";
import { ArrayField, SelectField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { ArrayFieldItem } from "@js/oarepo_ui";

// TODO: I assume that seriesTitle and volume will come from formConfig similar to languages. Not sure about the volumes??
const seriesTitle = [
  { value: "series A", text: "series A" },
  { value: "series B", text: "series B" },
  { value: "series C", text: "series C" },
];
const seriesVolume = [
  { value: "1", text: "1" },
  { value: "2", text: "2" },
  { value: "3", text: "3" },
];

export const SeriesField = ({ fieldPath, helpText }) => {
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add series")}
      fieldPath={fieldPath}
      label={i18next.t("Series")}
      labelIcon="pencil"
      helpText={helpText}
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <ArrayFieldItem indexPath={indexPath} arrayHelpers={arrayHelpers}>
            <SelectField
              clearable
              width={8}
              fieldPath={`${fieldPathPrefix}.seriesTitle`}
              label={i18next.t("Series title")}
              required
              options={seriesTitle}
            />
            <SelectField
              clearable
              width={8}
              fieldPath={`${fieldPathPrefix}.seriesVolume`}
              label={i18next.t("Series volume")}
              options={seriesVolume}
            />
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

SeriesField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

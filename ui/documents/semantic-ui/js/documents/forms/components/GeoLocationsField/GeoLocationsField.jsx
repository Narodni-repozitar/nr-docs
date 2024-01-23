import React from "react";
import PropTypes from "prop-types";
import { ArrayField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/i18next";
import { ArrayFieldItem } from "@js/oarepo_ui";

export const GeoLocationsField = ({ fieldPath, helpText }) => {
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add location")}
      defaultNewValue={{}}
      fieldPath={fieldPath}
      label={i18next.t("Geolocation")}
      labelIcon="globe"
      helpText={helpText}
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <ArrayFieldItem indexPath={indexPath} arrayHelpers={arrayHelpers}>
            <TextField
              width={8}
              fieldPath={`${fieldPathPrefix}.geoLocationPlace`}
              label={i18next.t("Location")}
              required
            />
            <TextField
              width={4}
              fieldPath={`${fieldPathPrefix}.geoLocationPoint.pointLongitude`}
              label={i18next.t("Longitude")}
              required
            />
            <TextField
              width={4}
              fieldPath={`${fieldPathPrefix}.geoLocationPoint.pointLatitude`}
              label={i18next.t("Latitude")}
              required
            />
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

GeoLocationsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

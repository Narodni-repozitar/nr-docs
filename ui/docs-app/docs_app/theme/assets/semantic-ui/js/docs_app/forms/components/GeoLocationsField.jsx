import React from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon } from "semantic-ui-react";
import { ArrayField, GroupField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";

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
          <GroupField>
            <TextField
              width={10}
              fieldPath={`${fieldPathPrefix}.geoLocationPlace`}
              label={i18next.t("Location")}
              required
            />
            <TextField
              width={3}
              fieldPath={`${fieldPathPrefix}.geoLocationPoint.pointLongitude`}
              label={i18next.t("Longitude")}
              required
            />
            <TextField
              width={3}
              fieldPath={`${fieldPathPrefix}.geoLocationPoint.pointLatitude`}
              label={i18next.t("Latitude")}
              required
            />

            <Form.Field style={{ marginTop: "1.75rem" }}>
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

GeoLocationsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

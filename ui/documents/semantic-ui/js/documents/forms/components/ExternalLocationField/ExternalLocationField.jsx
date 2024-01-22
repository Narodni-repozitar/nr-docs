import React from "react";
import PropTypes from "prop-types";
import { TextField, GroupField, FieldLabel } from "react-invenio-forms";
import { i18next } from "@translations/i18next";
import { Form } from "semantic-ui-react";

export const ExternalLocationField = ({ fieldPath, helpText }) => {
  return (
    <Form.Field>
      <FieldLabel label={i18next.t("External location")} icon="pencil" />
      <GroupField>
        <TextField
          width={8}
          fieldPath={`${fieldPath}.externalLocationURL`}
          label={i18next.t("Resource external location")}
        />
        <TextField
          width={8}
          fieldPath={`${fieldPath}.externalLocationNote`}
          label={i18next.t("Note")}
        />
      </GroupField>
      <label className="helptext">{helpText}</label>
    </Form.Field>
  );
};

ExternalLocationField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

ExternalLocationField.defaultProps = {
  helpText: i18next.t(
    "Provide other URL where this resource is available (i.e. other repository, database, webpage). In the note field you can provide for example name of website or database or specify another external source for the resource. "
  ),
};

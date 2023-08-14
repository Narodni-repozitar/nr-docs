import React from "react";
import PropTypes from "prop-types";
import { TextField, GroupField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { Form } from "semantic-ui-react";

export const ExternalLocationField = ({ fieldPath }) => {
  return (
    <Form.Field>
      <label>{i18next.t("External location")}</label>
      <GroupField>
        <TextField
          width={8}
          fieldPath={`${fieldPath}.externalLocationURL`}
          label={i18next.t("Resource external location")}
          required
        />
        <TextField
          width={8}
          fieldPath={`${fieldPath}.externalLocationNote`}
          label={i18next.t("Note")}
        />
      </GroupField>
    </Form.Field>
  );
};

ExternalLocationField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

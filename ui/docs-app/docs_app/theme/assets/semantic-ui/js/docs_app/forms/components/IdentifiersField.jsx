import React from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon } from "semantic-ui-react";
import {
  ArrayField,
  SelectField,
  GroupField,
  TextField,
} from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { GroupErrorMessage } from "./GroupErrorMessage";

export const IdentifiersField = ({
  fieldPath,
  helpText,
  options,
  label,
  identifierLabel,
}) => {
  return (
    <React.Fragment>
      <ArrayField
        addButtonLabel={i18next.t("Add identifier")}
        fieldPath={fieldPath}
        label={label}
        labelIcon="pencil"
        helpText={helpText}
      >
        {({ arrayHelpers, indexPath }) => {
          const fieldPathPrefix = `${fieldPath}.${indexPath}`;
          return (
            <GroupField>
              <SelectField
                clearable
                width={4}
                fieldPath={`${fieldPathPrefix}.scheme`}
                label={i18next.t("Identifier type")}
                required
                options={options}
              />
              <TextField
                required
                width={12}
                fieldPath={`${fieldPathPrefix}.identifier`}
                label={identifierLabel}
              />

              <Form.Field style={{ marginTop: "1.75rem" }}>
                <Button
                  aria-label={i18next.t("Remove field")}
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
      <GroupErrorMessage fieldPath={fieldPath} />
    </React.Fragment>
  );
};

IdentifiersField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
  options: PropTypes.array.isRequired,
  label: PropTypes.string,
  identifierLabel: PropTypes.string,
};

IdentifiersField.defaultProps = {
  label: i18next.t("Identifier field"),
  identifierLabel: i18next.t("Object identifier"),
};

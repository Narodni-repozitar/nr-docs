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
import { useHighlightState } from "@js/oarepo_ui";

export const IdentifiersField = ({
  fieldPath,
  helpText,
  options,
  label,
  identifierLabel,
}) => {
  const { highlightedStates, handleHover, handleMouseLeave } =
    useHighlightState();
  return (
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
          <GroupField
            className={
              highlightedStates[indexPath]
                ? "highlighted invenio-group-field"
                : "invenio-group-field"
            }
          >
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

            <Form.Field>
              <Button
                aria-label={i18next.t("Remove field")}
                className="close-btn"
                icon
                onClick={() => {
                  arrayHelpers.remove(indexPath);
                  handleMouseLeave(indexPath);
                }}
                onMouseEnter={() => handleHover(indexPath)}
                onMouseLeave={() => handleMouseLeave(indexPath)}
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

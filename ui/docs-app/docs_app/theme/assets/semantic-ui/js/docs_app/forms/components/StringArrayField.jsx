import React from "react";
import PropTypes from "prop-types";
import { FieldLabel, TextField, GroupField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext, getIn, FieldArray, Field } from "formik";
import { Icon, Button, Form } from "semantic-ui-react";
import { GroupErrorMessage } from "./GroupErrorMessage";

export const StringArrayField = ({
  fieldPath,
  label,
  required,
  newItemInitialValue,
  addButtonLabel,
  helpText,
  labelIcon,
  disabled,
  ...uiProps
}) => {
  const { values } = useFormikContext();
  return (
    <Form.Field>
      <FieldLabel label={label} icon={labelIcon} htmlFor={fieldPath} />
      <FieldArray
        name={fieldPath}
        render={({ remove, push }) => (
          <React.Fragment>
            {getIn(values, fieldPath, []).map((item, index) => {
              const indexPath = `${fieldPath}.${index}`;
              return (
                <GroupField key={index}>
                  <TextField
                    width={16}
                    fieldPath={indexPath}
                    label={`#${index + 1}`}
                    optimized
                    fluid
                    {...uiProps}
                  />
                  <Form.Field style={{ marginTop: "1.75rem" }}>
                    <Button
                      aria-label={i18next.t("Remove field")}
                      className="close-btn"
                      icon
                      onClick={() => remove(indexPath)}
                    >
                      <Icon name="close" />
                    </Button>
                  </Form.Field>
                </GroupField>
              );
            })}
            <label style={{ fontWeight: "bold" }}>{helpText}</label>
            <GroupErrorMessage fieldPath={fieldPath} />
            <Form.Button
              type="button"
              icon
              labelPosition="left"
              onClick={() => {
                push(newItemInitialValue);
              }}
            >
              <Icon name="add" />
              {addButtonLabel}
            </Form.Button>
          </React.Fragment>
        )}
      />
    </Form.Field>
  );
};

StringArrayField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  newItemInitialValue: PropTypes.string,
  addButtonLabel: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  helpText: PropTypes.string,
  labelIcon: PropTypes.string,
  disabled: PropTypes.bool,
};

StringArrayField.defaultProps = {
  addButtonLabel: i18next.t("Add note"),
  newItemInitialValue: "",
  labelIcon: "pencil",
  label: i18next.t("Notes"),
  helpText: i18next.t("Items shall be unique"),
};

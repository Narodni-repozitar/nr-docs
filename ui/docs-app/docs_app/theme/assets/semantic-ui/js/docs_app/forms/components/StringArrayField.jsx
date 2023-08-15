import React from "react";
import PropTypes from "prop-types";
import { FieldLabel } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext, getIn, FieldArray, Field } from "formik";
import { Icon, Popup, Button, Form } from "semantic-ui-react";

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
  const { values, errors } = useFormikContext();
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
                <Field
                  // maybe use UUID library to generate unique keys when some unique Ids are not available?
                  key={indexPath}
                  name={indexPath}
                  id={indexPath}
                >
                  {({ field, meta }) => {
                    // really struggled to use invenio's Text field, as they are hard coding error as meta.error, it creates major issues when you have a group error, as Yup
                    // does not seem to allow to set the error as array of strings, which leads to problems i.e. if your error is for example "Must be unique" error meta equals to the letters from
                    // the returned string
                    return (
                      <Form.Input
                        {...field}
                        error={meta.error ?? getIn(errors, fieldPath, {}).error}
                        icon={
                          <Popup
                            basic
                            inverted
                            position="bottom center"
                            content={i18next.t("Remove item")}
                            trigger={
                              <Button
                                className="rel-ml-1"
                                onClick={() => remove(index)}
                              >
                                <Icon fitted name="close" />
                              </Button>
                            }
                          />
                        }
                        disabled={disabled}
                        fluid
                        label={`#${index + 1}`}
                        required={required}
                        {...uiProps}
                      />
                    );
                  }}
                </Field>
              );
            })}
            <label>{helpText}</label>
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

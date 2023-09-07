import React from "react";
import { Message } from "semantic-ui-react";
import { useFormikContext, getIn } from "formik";
import _isEmpty from "lodash/isEmpty";
import _startCase from "lodash/startCase";

// function to turn last part of fieldPath from form camelCase to Camel Case
const titleCase = (fieldPath) =>
  _startCase(fieldPath.split(".")[fieldPath.split(".").length - 1]);
// TODO: fix broken margins on the error message. Also potentially make Error dismissible, as
// it could be annoying for the user
export const FormFeedback = () => {
  const { values } = useFormikContext();
  const validationErrors = getIn(values, "validationErrors", {});
  const httpError = getIn(values, "httpErrors", "");
  const successMessage = getIn(values, "successMessage", "");
  if (!_isEmpty(validationErrors))
    return (
      <Message className="rel-mb-5" negative color="orange">
        <Message.Header>{validationErrors?.errorMessage}</Message.Header>
        <Message.List>
          {validationErrors?.errors?.map((error, index) => (
            <Message.Item key={index}>{`${titleCase(error.field)}:${
              error.messages[0]
            }`}</Message.Item>
          ))}
        </Message.List>
      </Message>
    );
  if (httpError)
    return (
      <Message negative color="orange">
        <Message.Header>{httpError}</Message.Header>
      </Message>
    );
  if (successMessage)
    return (
      <Message positive color="green">
        <Message.Header>{successMessage}</Message.Header>
      </Message>
    );
  return null;
};

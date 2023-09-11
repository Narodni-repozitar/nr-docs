import React, { useState, useEffect } from "react";
import { Message } from "semantic-ui-react";
import { useFormikContext, getIn } from "formik";
import _isEmpty from "lodash/isEmpty";
import _startCase from "lodash/startCase";

// function to turn last part of fieldPath from form camelCase to Camel Case
const titleCase = (fieldPath) =>
  _startCase(fieldPath.split(".")[fieldPath.split(".").length - 1]);
// TODO: fix broken margins on the error message. Also potentially make Error dismissible, as
// it could be annoying for the user

const CustomMessage = ({ children, ...uiProps }) => {
  const [visible, setVisible] = useState(true);
  console.log("custom message", visible);

  // useEffect(() => {
  //   return () => setVisible(true);
  // }, []);
  const handleDismiss = () => setVisible(false);
  return (
    visible && (
      <Message onDismiss={handleDismiss} className="rel-mb-2" {...uiProps}>
        {children}
      </Message>
    )
  );
};
export const FormFeedback = () => {
  const { values } = useFormikContext();
  const validationErrors = getIn(values, "validationErrors", {});
  const httpError = getIn(values, "httpErrors", "");
  const successMessage = getIn(values, "successMessage", "");
  if (!_isEmpty(validationErrors))
    return (
      <CustomMessage negative color="orange">
        <Message.Header>{validationErrors?.errorMessage}</Message.Header>
        <Message.List>
          {validationErrors?.errors?.map((error, index) => (
            <Message.Item key={index}>{`${titleCase(error.field)}:${
              error.messages[0]
            }`}</Message.Item>
          ))}
        </Message.List>
      </CustomMessage>
    );
  if (httpError)
    return (
      <CustomMessage negative color="orange">
        <Message.Header>{httpError}</Message.Header>
      </CustomMessage>
    );
  if (successMessage)
    return (
      <CustomMessage positive color="green">
        <Message.Header>{successMessage}</Message.Header>
      </CustomMessage>
    );
  return null;
};

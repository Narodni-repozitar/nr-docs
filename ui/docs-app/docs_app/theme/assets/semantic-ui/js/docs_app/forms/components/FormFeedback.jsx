import React from "react";
import { Message } from "semantic-ui-react";
import { useFormikContext, getIn } from "formik";
import _isEmpty from "lodash/isEmpty";
import _startCase from "lodash/startCase";

// component to be used downstream of Formik that plugs into Formik's state and displays any errors
// that apiClient sent to formik in auxilary keys. The keys are later removed when submitting the form

// function to turn last part of fieldPath from form camelCase to Camel Case
const titleCase = (fieldPath) =>
  _startCase(fieldPath.split(".")[fieldPath.split(".").length - 1]);

const CustomMessage = ({ children, ...uiProps }) => {
  return (
    <Message className="rel-mb-2" {...uiProps}>
      {children}
    </Message>
  );
};
export const FormFeedback = () => {
  const { values } = useFormikContext();
  const validationErrors = getIn(values, "validationErrors", {});
  let httpError = getIn(values, "httpErrors", "");
  if (httpError?.response?.data) {
    httpError = httpError?.response?.data.message;
  }
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

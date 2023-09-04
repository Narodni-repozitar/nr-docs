import React from "react";
import { Message } from "semantic-ui-react";
import { useFormikContext, getIn } from "formik";
import _isEmpty from "lodash/isEmpty";

export const FormFeedback = () => {
  const { values } = useFormikContext();
  const validationErrors = getIn(values, "validationErrors", {});
  const hasValidationErrors = !_isEmpty(validationErrors);
  return (
    hasValidationErrors && (
      <Message>
        <Message.Header>{validationErrors?.errorMessage}</Message.Header>
        <Message.List>
          {validationErrors?.errors?.map((error, index) => (
            <Message.Item
              key={index}
            >{`${error.field}:${error.messages[0]}`}</Message.Item>
          ))}
        </Message.List>
      </Message>
    )
  );
};

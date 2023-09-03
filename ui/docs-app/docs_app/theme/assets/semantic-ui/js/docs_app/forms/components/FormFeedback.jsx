import React from "react";
import { Message } from "semantic-ui-react";
import { useFormikContext, getIn } from "formik";

export const FormFeedback = () => {
  const { values } = useFormikContext();
  const validationErrors = getIn(values, "validationErrors");
  return (
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
  );
};

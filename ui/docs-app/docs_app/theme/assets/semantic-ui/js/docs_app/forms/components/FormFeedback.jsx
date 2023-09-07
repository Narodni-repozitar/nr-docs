import React from "react";
import { Message } from "semantic-ui-react";
import { useFormikContext, getIn } from "formik";
import _isEmpty from "lodash/isEmpty";
import PropTypes from "prop-types";

export const FormFeedback = ({ submitError }) => {
  // plug into httpErrors in formik too. Make a function that can parse out fieldPath
  //  (i.e. take metadata.resourceType and produce) Resource type
  const { values } = useFormikContext();
  const validationErrors = getIn(values, "validationErrors", {});
  const hasValidationErrors = !_isEmpty(validationErrors);
  if (hasValidationErrors)
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
  if (submitError)
    return (
      <Message>
        <Message.Header>{submitError?.errorMessage}</Message.Header>
      </Message>
    );
  return null;
};

FormFeedback.propTypes = {
  submitError: PropTypes.object,
};

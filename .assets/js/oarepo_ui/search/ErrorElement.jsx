import React from "react";
import PropTypes from "prop-types";

import { Message } from "semantic-ui-react";

export const ErrorElement = ({ error }) => {
  return (
    <Message
      error
      content={error.response.data.message || error.response.statusText}
      icon="warning sign"
    />
  );
};

ErrorElement.propTypes = {
  error: PropTypes.object.isRequired,
};

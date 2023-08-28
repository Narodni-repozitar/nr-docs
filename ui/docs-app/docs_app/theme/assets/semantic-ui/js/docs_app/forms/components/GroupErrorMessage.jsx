import React from "react";
import PropTypes from "prop-types";
import { Message, Icon } from "semantic-ui-react";
import { getIn, useFormikContext } from "formik";
import _has from "lodash/has";
import _isObject from "lodash/isObject";

// component to display group errors that are results of some interdependancies between fields inside of group field
// for example if items need to be unique in some array field or similar
// problem is that yup would return a string which would result in following structure
// groupFieldPath : errorString
// so this component checks if there is a groupError (yup validation set in such way to return object with groupError key in those cases)
// maybe there is a better way to do it?

export const GroupErrorMessage = ({ fieldPath }) => {
  const { errors } = useFormikContext();
  const groupError = getIn(errors, fieldPath);

  if (groupError && _isObject(groupError) && _has(groupError, "groupError")) {
    return (
      <Message negative attached="top">
        <Icon name="warning" />
        {groupError.groupError}
      </Message>
    );
  }
  return null;
};

GroupErrorMessage.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};

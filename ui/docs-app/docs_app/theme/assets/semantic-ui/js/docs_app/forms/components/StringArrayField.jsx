import React, { useEffect } from "react";
import PropTypes from "prop-types";
import { ArrayField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext, getIn } from "formik";
import { Icon, Popup, Button, Message } from "semantic-ui-react";
import _uniq from "lodash/uniq";

// similar issue as in multiling component. The invenio form's arrayfield adds an object when you add an item and we want the state to be notes:["string", "string",...]
// so I applied similar approach
const arrayToArrayOfObjects = (arr) => {
  return arr.map((item) => ({ text: item }));
};

const checkForDuplicates = (arr) => {
  return arr.length !== _uniq(arr).length;
};

export const StringArrayField = ({
  fieldPath,
  label,
  required,
  newItemInitialValue,
  addButtonLabel,
  helpText,
  labelIcon,
}) => {
  const placeholderFieldPath = `_${fieldPath}`;
  const { setFieldValue, values } = useFormikContext();

  const hasDuplicateStrings = checkForDuplicates(getIn(values, fieldPath, []));
  useEffect(() => {
    if (!getIn(values, placeholderFieldPath)) {
      setFieldValue(
        placeholderFieldPath,
        getIn(values, fieldPath)
          ? arrayToArrayOfObjects(getIn(values, fieldPath))
          : arrayToArrayOfObjects([])
      );
      return;
    }
    setFieldValue(
      fieldPath,
      getIn(values, placeholderFieldPath).map((item) => item.text)
    );
  }, [values[placeholderFieldPath]]);
  return (
    <React.Fragment>
      <ArrayField
        addButtonLabel={addButtonLabel}
        fieldPath={placeholderFieldPath}
        label={label}
        required={required}
        helpText={helpText}
        labelIcon={labelIcon}
        defaultNewValue={{ text: "" }}
      >
        {({ arrayHelpers, indexPath }) => {
          const fieldPathPrefix = `${placeholderFieldPath}.${indexPath}`;

          return (
            <TextField
              fieldPath={`${fieldPathPrefix}.text`}
              label={`#${indexPath + 1}`}
              optimized
              fluid
              icon={
                <Popup
                  basic
                  inverted
                  position="bottom center"
                  content={i18next.t("Remove item")}
                  trigger={
                    <Button
                      className="rel-ml-1"
                      onClick={() => arrayHelpers.remove(indexPath)}
                    >
                      <Icon fitted name="close" />
                    </Button>
                  }
                />
              }
            />
          );
        }}
      </ArrayField>
      {hasDuplicateStrings && (
        <Message
          negative
          content={i18next.t(
            "You have provided two identical items. Please remove or modify one"
          )}
        />
      )}
    </React.Fragment>
  );
};

StringArrayField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  newItemInitialValue: PropTypes.string,
  addButtonLabel: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  helpText: PropTypes.string,
  labelIcon: PropTypes.string,
};

StringArrayField.defaultProps = {
  addButtonLabel: i18next.t("Add note"),
  newItemInitialValue: "",
  labelIcon: "pencil square",
  label: i18next.t("Notes"),
  helpText: i18next.t("Items shall be unique"),
};

import React, { useEffect } from "react";
import PropTypes from "prop-types";
import { ArrayField, TextField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext, getIn } from "formik";
import { Icon, Popup } from "semantic-ui-react";

// similar issue as in multiling component. The invenio form's arrayfield adds an object when you add an item and we want the state to be notes:["string", "string",...]
// so I applied similar approach
const arrayToArrayOfObjects = (arr) => {
  return arr.map((item) => ({ note: item }));
};

export const transformArrayToObject = (arr) => {
  return arr.map((item) => item.note);
};

export const NotesField = ({
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
      transformArrayToObject(getIn(values, placeholderFieldPath))
    );
  }, [values[placeholderFieldPath]]);
  return (
    <ArrayField
      addButtonLabel={addButtonLabel}
      fieldPath={placeholderFieldPath}
      label={label}
      required={required}
      helpText={helpText}
      labelIcon={labelIcon}
      defaultNewValue={{ note: "" }}
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${placeholderFieldPath}.${indexPath}`;

        return (
          <TextField
            fieldPath={`${fieldPathPrefix}.note`}
            label={`#${indexPath + 1}`}
            optimized
            fluid
            icon={
              <Popup
                basic
                inverted
                position="bottom center"
                content={i18next.t("Remove note")}
                trigger={
                  <Icon
                    as="button"
                    onClick={() => arrayHelpers.remove(indexPath)}
                  >
                    <Icon name="close" />
                  </Icon>
                }
              />
            }
          />
        );
      }}
    </ArrayField>
  );
};

NotesField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  newItemInitialValue: PropTypes.string,
  addButtonLabel: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  helpText: PropTypes.string,
  labelIcon: PropTypes.string,
};

NotesField.defaultProps = {
  addButtonLabel: i18next.t("Add note"),
  newItemInitialValue: "",
  labelIcon: "pencil square",
  label: i18next.t("Notes"),
};

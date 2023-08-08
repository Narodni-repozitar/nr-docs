import React from "react";
import { SelectField } from "./SelectField";
import { useFormConfig } from "@js/oarepo_ui/forms";
import { useFormikContext, getIn } from "formik";
import PropTypes from "prop-types";

// the idea is for this component to be a simple searchable single or multiple selection drop down
// that would handle things items that are going to be placed inside the formConfig (HTML). From what I see, all the vocabularies
// we have except institutions vocabulary which is a bit bigger could be easily handled by this component meaning:
// access-rights, contributor-roles, countries, funders, item-relation-types, languages, licences (rights), resource-types, subject-categories
// need form config to contain vocabularis.[languages, licenses, resourceTypes]

export const LocalVocabularySelectField = ({
  fieldPath,
  multiple,
  optionsListName,
  ...uiProps
}) => {
  const { formConfig } = useFormConfig();
  const optionsList = formConfig.vocabularies[optionsListName] || [];

  const { values } = useFormikContext();
  return (
    <SelectField
      search
      fieldPath={fieldPath}
      multiple={true}
      options={optionsList}
      onChange={({ e, data, formikProps }) => {
        formikProps.form.setFieldValue(
          fieldPath,
          data.value.map((vocabItem) => ({ id: vocabItem }))
        );
      }}
      value={getIn(values, fieldPath, []).map((vocabItem) => vocabItem.id)}
      {...uiProps}
    />
  );
};

LocalVocabularySelectField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  multiple: PropTypes.bool,
  optionsListName: PropTypes.string.isRequired,
};

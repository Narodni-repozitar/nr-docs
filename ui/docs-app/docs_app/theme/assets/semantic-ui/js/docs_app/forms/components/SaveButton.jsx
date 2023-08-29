import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import {
  useFormConfig,
  useSubmitConfig,
  submitContextType,
} from "@js/oarepo_ui";

export const SaveButton = ({ ...uiProps }) => {
  const { handleSubmit, isSubmitting } = useFormikContext();
  const { record, formConfig } = useFormConfig();
  const { updateConfig } = useSubmitConfig();
  const existingRecord = !!record.id;
  console.log(existingRecord);
  console.log(formConfig.createUrl);

  return (
    <Button
      name="save"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="grey"
      onClick={(e) => {
        updateConfig({
          onSubmitSuccess: (result) => {
            console.log(result);
            // window.location.href = result.links.self_html;
          },
          apiUrl: existingRecord ? record.links.self : formConfig.createUrl,
          context: existingRecord
            ? submitContextType.update
            : submitContextType.create,
        });
        handleSubmit(e);
      }}
      icon="save"
      labelPosition="left"
      content={i18next.t("Save")}
      type="button"
      {...uiProps}
    />
  );
};

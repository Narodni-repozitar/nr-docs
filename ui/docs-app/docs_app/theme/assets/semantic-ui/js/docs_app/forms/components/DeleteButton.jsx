import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import { useSubmitConfig, submitContextType } from "@js/oarepo_ui";

export const DeleteButton = ({ ...uiProps }) => {
  const { handleSubmit, isSubmitting } = useFormikContext();
  const { updateConfig } = useSubmitConfig();

  const draftSaveSubmitConfig = {
    context: submitContextType.delete,
    onSubmitSuccess: [
      (result, formik) => {
        //  TODO: should redirect to /me page but we don't have that one yet
        window.location.href = "/docs/";
      },
    ],
  };

  return (
    <Button
      name="preview"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="red"
      onClick={async () => {
        await updateConfig(draftSaveSubmitConfig);
        handleSubmit();
      }}
      icon="delete"
      labelPosition="left"
      content={i18next.t("Delete")}
      type="button"
      {...uiProps}
    />
  );
};

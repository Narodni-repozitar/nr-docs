import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import { useSubmitConfig, submitContextType } from "@js/oarepo_ui";

export const PublishButton = ({ ...uiProps }) => {
  const { handleSubmit, isSubmitting } = useFormikContext();
  const { updateConfig } = useSubmitConfig();

  return (
    <Button
      name="publish"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="green"
      onClick={(e) => {
        updateConfig(submitContextType.publish);
        handleSubmit(e);
      }}
      icon="save"
      labelPosition="left"
      content={i18next.t("Publish")}
      type="button"
      {...uiProps}
    />
  );
};

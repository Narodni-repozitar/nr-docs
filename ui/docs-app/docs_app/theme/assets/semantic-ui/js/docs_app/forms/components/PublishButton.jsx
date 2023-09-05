import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import { useSubmitConfig, submitContextType } from "@js/oarepo_ui";

export const PublishButton = ({ ...uiProps }) => {
  const { isSubmitting, handleSubmit } = useFormikContext();
  const { updateConfig } = useSubmitConfig();
  const handlePublish = () => {
    updateConfig(submitContextType.publish);
    setTimeout(handleSubmit, 0);
  };

  return (
    <Button
      name="publish"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="green"
      onClick={() => handlePublish()}
      icon="save"
      labelPosition="left"
      content={i18next.t("Publish")}
      type="submit"
      {...uiProps}
    />
  );
};

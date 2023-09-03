import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import { useSubmitConfig, submitContextType } from "@js/oarepo_ui";

export const PublishButton = ({ ...uiProps }) => {
  const { handleSubmit, isSubmitting } = useFormikContext();
  const { updateConfig } = useSubmitConfig();

  const draftSaveSubmitConfig = {
    context: submitContextType.publish,
    onSubmitSuccess: [
      (result, formik) => {
        window.location.href = result.links.self_html;
      },
    ],
  };

  return (
    <Button
      name="publish"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="green"
      onClick={async () => {
        await updateConfig(draftSaveSubmitConfig);
        handleSubmit();
      }}
      icon="save"
      labelPosition="left"
      content={i18next.t("Publish")}
      type="submit"
      {...uiProps}
    />
  );
};

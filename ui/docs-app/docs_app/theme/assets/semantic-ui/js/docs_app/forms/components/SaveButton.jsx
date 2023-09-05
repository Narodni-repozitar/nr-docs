import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { submitContextType, useSubmitConfig } from "@js/oarepo_ui";
import { useFormikContext } from "formik";

export const SaveButton = ({ ...uiProps }) => {
  const { isSubmitting, handleSubmit } = useFormikContext();
  const { updateConfig } = useSubmitConfig();
  const handleSave = () => {
    updateConfig(submitContextType.save);
    setTimeout(handleSubmit, 0);
  };

  return (
    <Button
      name="save"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="grey"
      // onclick={submit({context: submitContextType.save, ...})}
      onClick={() => handleSave()}
      icon="save"
      labelPosition="left"
      content={i18next.t("Save")}
      type="button"
      {...uiProps}
    />
  );
};

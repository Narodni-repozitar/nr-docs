import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import { useSubmitConfig } from "@js/oarepo_ui";

export const DeleteButton = ({ ...uiProps }) => {
  const { handleSubmit, isSubmitting } = useFormikContext();
  const { updateConfig } = useSubmitConfig();

  return (
    <Button
      name="preview"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="red"
      onClick={(e) => {
        updateConfig("delete");
        handleSubmit(e);
      }}
      icon="eye"
      labelPosition="left"
      content={i18next.t("Delete")}
      type="button"
      {...uiProps}
    />
  );
};

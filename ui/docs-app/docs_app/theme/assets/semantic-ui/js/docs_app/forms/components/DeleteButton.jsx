import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import { useSubmitConfig, submitContextType } from "@js/oarepo_ui";

export const DeleteButton = ({ ...uiProps }) => {
  const { isSubmitting, values, handleSubmit } = useFormikContext();
  const { updateConfig } = useSubmitConfig();
  const handleDelete = () => {
    updateConfig(submitContextType.delete);
    setTimeout(handleSubmit, 0);
  };

  return (
    values.id && (
      <Button
        name="preview"
        disabled={isSubmitting}
        loading={isSubmitting}
        color="red"
        onClick={() => handleDelete()}
        icon="delete"
        labelPosition="left"
        content={i18next.t("Delete")}
        type="button"
        {...uiProps}
      />
    )
  );
};

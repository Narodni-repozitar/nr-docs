import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";

export const PreviewButton = ({ ...uiProps }) => {
  const { handleSubmit, isSubmitting } = useFormikContext();
  return (
    <Button
      name="preview"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="grey"
      onClick={handleSubmit}
      icon="eye"
      labelPosition="left"
      content={i18next.t("Preview")}
      type="button"
      {...uiProps}
    />
  );
};

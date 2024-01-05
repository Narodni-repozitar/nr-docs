import React, { memo } from "react";
import { useFormikContext } from "formik";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";

export const ValidateButton = memo(() => {
  const { isSubmitting, validateForm } = useFormikContext();
  return (
    <Button
      fluid
      disabled={isSubmitting}
      color="green"
      onClick={() => validateForm()}
      icon="check"
      labelPosition="left"
      content={i18next.t("Validate form")}
      type="button"
    />
  );
});

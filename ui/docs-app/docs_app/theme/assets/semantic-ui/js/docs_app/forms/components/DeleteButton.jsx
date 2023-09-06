import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { submitContextType, useSubmitSupport } from "@js/oarepo_ui";

export const DeleteButton = ({ ...uiProps }) => {
  const { isSubmitting, submit, values } = useSubmitSupport(
    submitContextType.delete
  );

  return (
    values.id && (
      <Button
        name="preview"
        disabled={isSubmitting}
        loading={isSubmitting}
        color="red"
        onClick={() => submit()}
        icon="delete"
        labelPosition="left"
        content={i18next.t("Delete")}
        type="button"
        {...uiProps}
      />
    )
  );
};

import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useApiClient } from "@js/oarepo_ui";

export const DeleteButton = ({ ...uiProps }) => {
  const apiClient = useApiClient();

  return (
    apiClient.formik.values.id && (
      <Button
        name="preview"
        disabled={apiClient.isSubmitting}
        loading={apiClient.isSubmitting}
        color="red"
        onClick={() => apiClient.delete()}
        icon="delete"
        labelPosition="left"
        content={i18next.t("Delete")}
        type="submit"
        {...uiProps}
      />
    )
  );
};

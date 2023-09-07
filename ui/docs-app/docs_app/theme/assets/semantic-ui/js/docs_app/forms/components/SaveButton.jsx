import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useApiClient } from "@js/oarepo_ui";

export const SaveButton = ({ ...uiProps }) => {
  const apiClient = useApiClient();
  return (
    <Button
      name="save"
      disabled={apiClient.isSubmitting}
      loading={apiClient.isSubmitting}
      color="grey"
      onClick={() => apiClient.save()}
      icon="save"
      labelPosition="left"
      content={i18next.t("Save")}
      type="submit"
      {...uiProps}
    />
  );
};

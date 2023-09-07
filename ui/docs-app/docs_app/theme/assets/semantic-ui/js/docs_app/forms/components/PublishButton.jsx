import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useApiClient } from "@js/oarepo_ui";

export const PublishButton = ({ ...uiProps }) => {
  const apiClient = useApiClient();
  return (
    <Button
      name="publish"
      disabled={apiClient.isSubmitting}
      loading={apiClient.isSubmitting}
      color="green"
      onClick={() => apiClient.publish()}
      icon="upload"
      labelPosition="left"
      content={i18next.t("Publish")}
      type="submit"
      {...uiProps}
    />
  );
};

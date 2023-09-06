import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { submitContextType, useSubmitSupport } from "@js/oarepo_ui";

export const PublishButton = ({ ...uiProps }) => {
  const { isSubmitting, submit } = useSubmitSupport(submitContextType.publish);
  return (
    <Button
      name="publish"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="green"
      onClick={() => submit()}
      icon="save"
      labelPosition="left"
      content={i18next.t("Publish")}
      type="submit"
      {...uiProps}
    />
  );
};

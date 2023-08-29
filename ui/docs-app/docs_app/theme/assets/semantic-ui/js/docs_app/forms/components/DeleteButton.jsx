import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import { OARepoDepositApiClient, useFormConfig } from "@js/oarepo_ui";

export const DeleteButton = ({ ...uiProps }) => {
  const { handleSubmit, isSubmitting } = useFormikContext();
  const { record } = useFormConfig();
  const handleDelete = () =>
    OARepoDepositApiClient.deleteDraft(record.links.self);
  return (
    <Button
      name="preview"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="red"
      onClick={handleDelete}
      icon="eye"
      labelPosition="left"
      content={i18next.t("Delete")}
      type="button"
      {...uiProps}
    />
  );
};

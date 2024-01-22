import React, { memo } from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { useDepositApiClient } from "@js/oarepo_ui";

export const SaveButton = memo(({ ...uiProps }) => {
  const { isSubmitting, save, isSaving } = useDepositApiClient();
  return (
    <Button
      name="save"
      disabled={isSubmitting}
      loading={isSaving}
      color="grey"
      onClick={() => save()}
      icon="save"
      labelPosition="left"
      content={i18next.t("Save")}
      type="submit"
      {...uiProps}
    />
  );
});

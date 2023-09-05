import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { submitContextType, useSubmitConfig } from "@js/oarepo_ui";
import { useFormikContext } from "formik";

export const SaveButton = ({ ...uiProps }) => {
  const { isSubmitting, handleSubmit } = useFormikContext();
  const { updateConfig } = useSubmitConfig();
  const handleSave = () => {
    updateConfig(submitContextType.save);
    setTimeout(handleSubmit, 0);
  };

  // two functions passed to submitSuccess. One function to manage validation errors that come
  // in the response body. Other one is used to update the record in formik's state with drafts PID
  // and links that come in response at the first time draft is created. I did not see more reasonable way to do it (how to
  // have updated record in the app, as we are not redirecting to another page but only changing history)
  // in invenio, record is not used straight from HTML, but rather it is placed in the store and then from the store
  // passed to formik's initial values, and this allows them to use enableReinitialize prop to reset the form with the
  // newly created PID (entire record actually)

  return (
    <Button
      name="save"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="grey"
      // onclick={submit({context: submitContextType.save, ...})}
      onClick={() => handleSave()}
      icon="save"
      labelPosition="left"
      content={i18next.t("Save")}
      type="button"
      {...uiProps}
    />
  );
};

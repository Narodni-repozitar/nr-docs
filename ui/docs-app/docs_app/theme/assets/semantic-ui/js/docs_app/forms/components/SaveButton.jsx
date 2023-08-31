import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import {
  useFormConfig,
  useSubmitConfig,
  submitContextType,
} from "@js/oarepo_ui";

export const SaveButton = ({ ...uiProps }) => {
  const { handleSubmit, isSubmitting, setValues } = useFormikContext();
  const { updateConfig } = useSubmitConfig();

  // two functions passed to submitSuccess. One function to manage validation errors that come
  // in the response body. Other one is used to update the record in formik's state with drafts PID
  // and links that come in respose at the first time draft is created. I did not see more reasonable way to do it
  // in invenio, record is not used straight from HTML, but rather it is placed in the store and then from the store
  // passed to formik's initial values, and this allows them to use enableReinitialize prop to reset the form with the n
  // newly created PID (entire record actually)
  const draftSaveSubmitConfig = {
    context: submitContextType.save,
    onSubmitSuccess: [
      (result, formik) => {
        if (!result.id) {
          setValues(result);
        }
      },

      (result, formik) => {
        if (result.errors) {
          result.errors?.forEach((err) =>
            formik.setFieldError(err.field, err.messages.join(" "))
          );
        }
      },
    ],
  };

  return (
    <Button
      name="save"
      disabled={isSubmitting}
      loading={isSubmitting}
      color="grey"
      onClick={(e) => {
        updateConfig(draftSaveSubmitConfig);
        handleSubmit(e);
      }}
      icon="save"
      labelPosition="left"
      content={i18next.t("Save")}
      type="button"
      {...uiProps}
    />
  );
};

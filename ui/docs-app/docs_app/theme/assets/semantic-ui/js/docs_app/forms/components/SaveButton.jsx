import React from "react";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { useFormikContext } from "formik";
import { useSubmitConfig, submitContextType } from "@js/oarepo_ui";

export const SaveButton = ({ ...uiProps }) => {
  const { handleSubmit, isSubmitting, setValues, values } = useFormikContext();
  const { updateConfig } = useSubmitConfig();

  // two functions passed to submitSuccess. One function to manage validation errors that come
  // in the response body. Other one is used to update the record in formik's state with drafts PID
  // and links that come in response at the first time draft is created. I did not see more reasonable way to do it (how to
  // have updated record in the app, as we are not redirecting to another page but only changing history)
  // in invenio, record is not used straight from HTML, but rather it is placed in the store and then from the store
  // passed to formik's initial values, and this allows them to use enableReinitialize prop to reset the form with the
  // newly created PID (entire record actually)
  const draftSaveSubmitConfig = {
    context: submitContextType.save,
    onSubmitSuccess: [
      (result, formik) => {
        if (!values.id) {
          window.history.replaceState(
            undefined,
            "",
            new URL(result.links.self_html).pathname
          );
          setValues(result);
        }
      },
      (result, formik) => {
        if (result.errors) {
          result.errors?.forEach((err) =>
            formik.setFieldError(err.field, err.messages.join(" "))
          );
          formik.setFieldValue("validationErrors", {
            errors: result.errors,
            errorMessage: i18next.t(
              "Form saved with validation errors. Fields listed below that failed validation were not saved to the server"
            ),
          });
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
      onClick={async () => {
        await updateConfig(draftSaveSubmitConfig);
        handleSubmit();
      }}
      icon="save"
      labelPosition="left"
      content={i18next.t("Save")}
      type="button"
      {...uiProps}
    />
  );
};

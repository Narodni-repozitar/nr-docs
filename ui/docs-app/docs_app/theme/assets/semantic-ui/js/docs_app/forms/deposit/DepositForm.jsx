import React from "react";
import _isEmpty from "lodash/isEmpty";
import { useFormConfig, useOnSubmit } from "@js/oarepo_ui";
import { BaseForm } from "react-invenio-forms";
import { Container } from "semantic-ui-react";
import { NRDocumentValidationSchema } from "./NRDocumentValidationSchema";


export const DepositForm = () => {
  const { record, formConfig } = useFormConfig();
  const context = formConfig.createUrl? submitContextType.create : submitContextType.update
  const { onSubmit, onSubmitError } = useOnSubmit({
    apiUrl: formConfig.createUrl || formConfig.updateUrl,
    context: context,
    onSubmitSuccess: (result) => {
      window.location.href = editMode
        ? currentPath.replace("/edit", "")
        : currentPath.replace("_new", result.id)
    }
  });

  return (
    <Container>
      <BaseForm
        onSubmit={onSubmit}
        formik={{
          initialValues: record,
          validationSchema: NRDocumentValidationSchema,
          validateOnChange: false,
          validateOnBlur: false,
          enableReinitialize: true,
        }}
      >
        <pre>Add your deposit form fields here 👇</pre>
      </BaseForm>
    </Container>
  );
};


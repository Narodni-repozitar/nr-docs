import React from "react";
import _isEmpty from "lodash/isEmpty";
import { useFormConfig } from "@js/oarepo_ui/forms";
import { BaseForm } from "react-invenio-forms";
import { Container } from "semantic-ui-react";

const VocabularyForm = () => {
  const { record, formConfig } = useFormConfig();

  return (
    <Container>
      <BaseForm
        onSubmit={onSubmit}
        formik={{
          initialValues: initialValues,
          validationSchema: VocabularyFormSchema,
          validateOnChange: false,
          validateOnBlur: false,
          enableReinitialize: true,
        }}
      >
        <h1>Deposit form</h1>
      </BaseForm>
    </Container>
  );
};

export default VocabularyForm;

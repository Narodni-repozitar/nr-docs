import React from "react";
import { Container } from "semantic-ui-react";
import { BaseFormLayout } from "@js/oarepo_ui";
import { NRDocumentValidationSchema } from "./NRDocumentValidationSchema";

export const FormAppLayout = () => {
  const formikProps = {
    validationSchema: NRDocumentValidationSchema,
  };
  return (
    <Container fluid>
      <BaseFormLayout formikProps={formikProps} />
    </Container>
  );
};
export default FormAppLayout;

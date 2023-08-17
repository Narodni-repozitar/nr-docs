import React from "react";
import { useFormikContext } from "formik";
import { Button, Container } from "semantic-ui-react";
import PropTypes from "prop-types";
import { i18next } from "@translations/docs_app/i18next";

export const ValidateButton = () => {
  const { isSubmitting, validateForm } = useFormikContext();
  return (
    <Container textAlign="center">
      <Button
        fluid
        disabled={isSubmitting}
        loading={isSubmitting}
        color="green"
        onClick={() => validateForm()}
        icon="upload"
        labelPosition="left"
        content={i18next.t("Validate form")}
        type="button"
      />
    </Container>
  );
};

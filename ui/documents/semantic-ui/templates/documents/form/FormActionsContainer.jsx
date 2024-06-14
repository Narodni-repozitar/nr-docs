import React from "react";
import { Card, Grid } from "semantic-ui-react";
import {
  PublishButton,
  PreviewButton,
  SaveButton,
  DeleteButton,
  ValidateButton,
  useFormConfig,
} from "@js/oarepo_ui";
import { TextField, FieldLabel } from "react-invenio-forms";
import { i18next } from "@translations/i18next";

const FormActionsContainer = () => {
  const { links } = useFormConfig();
  return (
    <Card fluid>
      {/* <Card.Content>
          <DepositStatusBox />
        </Card.Content> */}
      <Card.Content>
        <Grid>
          <Grid.Column computer={8} mobile={16} className="left-btn-col">
            <SaveButton fluid />
          </Grid.Column>

          <Grid.Column computer={8} mobile={16} className="right-btn-col">
            <PreviewButton fluid />
          </Grid.Column>

          <Grid.Column width={16} className="pt-10">
            <PublishButton
              additionalInputs={
                <TextField
                  fieldPath="metadata.version"
                  placeholder={i18next.t(
                    "Write the version (first, second ...)."
                  )}
                  label={
                    <FieldLabel
                      htmlFor={"metadata.version"}
                      icon="pencil"
                      label={i18next.t("Version")}
                    />
                  }
                />
              }
            />
          </Grid.Column>
          <Grid.Column width={16} className="pt-10" data-testid="validate-button">
            <ValidateButton />
          </Grid.Column>
          <Grid.Column width={16} className="pt-10">
            <DeleteButton redirectUrl={links.search} />
          </Grid.Column>
        </Grid>
      </Card.Content>
    </Card>
  );
};

export default FormActionsContainer;

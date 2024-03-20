import React from "react";
import { Card, Grid } from "semantic-ui-react";
import {
  PreviewButton,
  SaveButton,
  DeleteButton,
  ValidateButton,
  useFormConfig,
} from "@js/oarepo_ui";
import { PublishButtonComponent } from "@nr";

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
            <PublishButtonComponent />
          </Grid.Column>
          <Grid.Column width={16} className="pt-10">
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

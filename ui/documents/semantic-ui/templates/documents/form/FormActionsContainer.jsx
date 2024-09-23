import React from "react";
import { Card, Grid } from "semantic-ui-react";
import {
  PreviewButton,
  SaveButton,
  DeleteButton,
  SelectedCommunity,
  useDepositApiClient,
  serializeErrors,
} from "@js/oarepo_ui";
import { i18next } from "@translations/i18next";
import { RecordRequests } from "@js/oarepo_requests/components";
import { useFormikContext } from "formik";

const FormActionsContainer = () => {
  const { values, setErrors } = useFormikContext();
  const { save } = useDepositApiClient();
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
          {values.id && (
            <Grid.Column width={16} className="pt-10">
              <RecordRequests
                record={values}
                onErrorCallback={(e) =>
                  setErrors(
                    serializeErrors(
                      e?.response?.data?.errors,
                      i18next.t(
                        "Request failed due to record validation errors. Please fix them and try again."
                      )
                    )
                  )
                }
                saveDraft={save}
                shouldRedirectToEdit={false}
              />
            </Grid.Column>
          )}
          {values.id && (
            <Grid.Column width={16} className="pt-10">
              <DeleteButton redirectUrl="/me/records" />
            </Grid.Column>
          )}
          <Grid.Column width={16} className="pt-10">
            <SelectedCommunity />
          </Grid.Column>
        </Grid>
      </Card.Content>
    </Card>
  );
};

export default FormActionsContainer;

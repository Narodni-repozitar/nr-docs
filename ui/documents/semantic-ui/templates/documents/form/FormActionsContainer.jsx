import React from "react";
import { Card, Grid } from "semantic-ui-react";
import {
  PreviewButton,
  SaveButton,
  DeleteButton,
  useDepositApiClient,
  serializeErrors,
} from "@js/oarepo_ui";
import { i18next } from "@translations/i18next";
import { SelectedCommunity } from "@js/communities_components/CommunitySelector/SelectedCommunity";
import { RecordRequests } from "@js/oarepo_requests/components";
import { useFormikContext } from "formik";
import { REQUEST_TYPE } from "@js/oarepo_requests_common";

const FormActionsContainer = () => {
  const { values, setErrors } = useFormikContext();
  const { save } = useDepositApiClient();

  const onBeforeAction = ({ requestActionName }) => {
    // Do not try to save in case user is declining or cancelling the request from the form
    if (
      requestActionName === REQUEST_TYPE.DECLINE ||
      requestActionName === REQUEST_TYPE.CANCEL
    ) {
      return true;
    } else {
      return save({ successMessage: "" });
    }
  };

  return (
    <Card fluid>
      {/* <Card.Content>
          <DepositStatusBox />
        </Card.Content> */}
      <Card.Content>
        <Grid>
          <Grid.Column width={16}>
            <div className="flex">
              <SaveButton fluid className="mb-10" />
              <PreviewButton fluid className="mb-10" />
            </div>

            {values.id && (
              <RecordRequests
                record={values}
                onBeforeAction={onBeforeAction}
                onActionError={({ e, modalControl }) => {
                  if (e?.response?.data?.errors?.length > 0) {
                    const errors = serializeErrors(
                      e?.response?.data?.errors,
                      i18next.t(
                        "Action failed due to validation errors. Please correct the errors and try again:"
                      )
                    );
                    setErrors(errors);
                  }
                  modalControl?.closeModal();
                }}
              />
            )}
            {values.id && <DeleteButton redirectUrl="/me/records" />}
          </Grid.Column>
          <Grid.Column width={16} className="pt-10">
            <SelectedCommunity />
          </Grid.Column>
        </Grid>
      </Card.Content>
    </Card>
  );
};

export default FormActionsContainer;

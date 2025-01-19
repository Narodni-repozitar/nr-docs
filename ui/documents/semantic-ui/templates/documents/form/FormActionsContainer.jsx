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
import { setIn } from "formik";

const FormActionsContainer = () => {
  const { values, setErrors } = useFormikContext();
  const { save } = useDepositApiClient();

  const onBeforeAction = ({ requestActionName, requestOrRequestType }) => {
    const requestType =
      requestOrRequestType?.type || requestOrRequestType?.type_id;
    // Do not try to save in case user is declining or cancelling the request from the form
    if (
      requestActionName === REQUEST_TYPE.DECLINE ||
      requestActionName === REQUEST_TYPE.CANCEL ||
      requestType === "initiate_community_migration" ||
      requestType === "confirm_community_migration"
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
                onActionError={({ e, modalControl, formik }) => {
                  if (
                    e?.response?.data?.error_type === "cf_validation_error" &&
                    e?.response?.data?.errors
                  ) {
                    let errorsObj = {};
                    console.log(e?.response?.data?.errors);
                    for (const error of e.response.data.errors) {
                      errorsObj = setIn(
                        errorsObj,
                        error.field,
                        error.messages.join(" ")
                      );
                    }
                    console.log(errorsObj);
                    formik?.setErrors(errorsObj);
                  } else if (e?.response?.data?.errors?.length > 0) {
                    const errors = serializeErrors(
                      e?.response?.data?.errors,
                      i18next.t(
                        "Action failed due to validation errors. Please correct the errors and try again:"
                      )
                    );
                    setErrors(errors);
                    modalControl?.closeModal();
                  }
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

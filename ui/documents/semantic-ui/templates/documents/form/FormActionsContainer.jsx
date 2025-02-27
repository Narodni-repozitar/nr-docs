import React from "react";
import { Card, Grid } from "semantic-ui-react";
import {
  PreviewButton,
  SaveButton,
  DeleteButton,
  useDepositApiClient,
  AccessRightField,
  useFormConfig,
} from "@js/oarepo_ui";
import { i18next } from "@translations/i18next";
import { SelectedCommunity } from "@js/communities_components/CommunitySelector/SelectedCommunity";
import { RecordRequests } from "@js/oarepo_requests/components";
import { useFormikContext } from "formik";
import {
  REQUEST_TYPE,
  cfValidationErrorPlugin,
  recordValidationErrorsPlugin,
  beforeActionFormErrorPlugin,
} from "@js/oarepo_requests_common";

const FormActionsContainer = () => {
  const { values, setErrors } = useFormikContext();
  const { save } = useDepositApiClient();
  const {
    formConfig: {
      permissions,
      allowRecordRestriction,
      recordRestrictionGracePeriod,
    },
  } = useFormConfig();

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
      return save({
        errorMessage: i18next.t(
          "The request ({{requestType}}) could not be made due to validation errors. Please fix them and try again:",
          { requestType: requestOrRequestType.name }
        ),
      });
    }
  };
  return (
    <React.Fragment>
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
              <RecordRequests
                record={values}
                onBeforeAction={onBeforeAction}
                onErrorPlugins={[
                  cfValidationErrorPlugin,
                  recordValidationErrorsPlugin,
                  beforeActionFormErrorPlugin,
                ]}
                actionExtraContext={{ setErrors }}
              />
              <DeleteButton redirectUrl="/me/records" />
            </Grid.Column>
            <Grid.Column width={16} className="pt-10">
              <SelectedCommunity />
            </Grid.Column>
          </Grid>
        </Card.Content>
      </Card>
      <AccessRightField
        label={i18next.t("metadata/accessRights.label")}
        record={values}
        labelIcon="shield"
        fieldPath="access"
        showMetadataAccess={permissions?.can_manage_record_access}
        // permissions seem to not work properly when on /_new, in this case I think it is OK that you can restrict
        // since you have access to the form
        recordRestrictionGracePeriod={recordRestrictionGracePeriod}
        allowRecordRestriction={allowRecordRestriction}
      />
    </React.Fragment>
  );
};

export default FormActionsContainer;

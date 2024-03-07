import { createFormAppInit, parseFormAppConfig } from "@js/oarepo_ui/forms";
import FormAppLayout from "./FormAppLayout";
import { DepositFormControlPanel } from "./DepositFormControlPanel";
import { DepositFormFields } from "./DepositFormFields";
const { formConfig } = parseFormAppConfig();
const { overridableIdPrefix } = formConfig;

export const componentOverrides = {
  [`${overridableIdPrefix}.FormApp.layout`]: FormAppLayout,
  [`${overridableIdPrefix}.FormFields.container`]: DepositFormFields,
  [`${overridableIdPrefix}.FormActions.container`]: DepositFormControlPanel,
};

createFormAppInit({ componentOverrides });

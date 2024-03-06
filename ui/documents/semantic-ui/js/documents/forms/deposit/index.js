import { createFormAppInit } from "@js/oarepo_ui";
import { DepositForm } from "./DepositForm";

export const componentOverrides = {
  "Default.Form.FormApp.layout": DepositForm,
};

createFormAppInit({ componentOverrides: componentOverrides });

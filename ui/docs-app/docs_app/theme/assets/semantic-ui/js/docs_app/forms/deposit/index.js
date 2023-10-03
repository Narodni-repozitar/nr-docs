import { createFormAppInit } from "@js/oarepo_ui";
import { DepositForm } from "./DepositForm"

export const overriddenComponents = {
    "FormApp.layout": DepositForm,
};

createFormAppInit(overriddenComponents);

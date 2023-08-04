import { createFormAppInit } from "@js/oarepo_ui/forms";
import { DepositForm } from "./DepositForm"

export const overriddenComponents = {
    "FormApp.layout": DepositForm,
};

createFormAppInit(overriddenComponents);

import { createFormAppInit } from "@js/oarepo_ui/forms";

export const overriddenComponents = {
    "FormApp.layout": DepositForm,
};

createFormAppInit(overriddenComponents);

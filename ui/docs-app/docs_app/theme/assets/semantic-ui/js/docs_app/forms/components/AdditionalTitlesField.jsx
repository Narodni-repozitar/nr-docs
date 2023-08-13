import React from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon, Message } from "semantic-ui-react";
import { ArrayField, GroupField, SelectField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { I18nTextInputField } from "@js/oarepo_ui";

// this should come from formConfig in the actual use case
const subtitleTypes = [
  { text: "Alternative title", value: "alternative-title" },
  { text: "Translated title", value: "translated-title" },
  { text: "Subtitle", value: "subtitle" },
  { text: "Other", value: "other" },
];

export const AdditionalTitlesField = ({ fieldPath }) => {
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add additional title")}
      defaultNewValue={{}}
      fieldPath={fieldPath}
      label={i18next.t("Additional titles")}
      labelIcon="pencil"
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <GroupField border>
            <Form.Field width={13}>
              <I18nTextInputField
                fieldPath={`${fieldPathPrefix}.title`}
                label={i18next.t("Title")}
                required
              />
            </Form.Field>
            <Form.Field width={3}>
              <SelectField
                fieldPath={`${fieldPathPrefix}.titleType`}
                label={i18next.t("Title type")}
                optimized
                options={subtitleTypes}
                required
              />
            </Form.Field>

            <Form.Field style={{ marginTop: "1.75rem" }}>
              <Button
                aria-label={i18next.t("Remove field")}
                className="close-btn"
                icon
                onClick={() => arrayHelpers.remove(indexPath)}
              >
                <Icon name="close" />
              </Button>
            </Form.Field>
          </GroupField>
        );
      }}
    </ArrayField>
  );
};

AdditionalTitlesField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};

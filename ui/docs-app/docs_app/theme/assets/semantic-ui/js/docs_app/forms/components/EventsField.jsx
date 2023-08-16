import React from "react";
import PropTypes from "prop-types";
import { Button, Form, Icon } from "semantic-ui-react";
import { ArrayField, TextField, GroupField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { LocalVocabularySelectField } from "./LocalVocabularySelectField";
import { StringArrayField } from "./StringArrayField";
import { DateField } from "./DateField";

export const EventsField = ({ fieldPath, helpText }) => {
  return (
    <ArrayField
      addButtonLabel={i18next.t("Add event")}
      fieldPath={fieldPath}
      label={i18next.t("Events")}
      labelIcon="pencil"
      helpText={helpText}
    >
      {({ arrayHelpers, indexPath }) => {
        const fieldPathPrefix = `${fieldPath}.${indexPath}`;
        return (
          <React.Fragment>
            <TextField
              width={16}
              fieldPath={`${fieldPathPrefix}.eventNameOriginal`}
              label={i18next.t("Event name")}
              required
            />
            <StringArrayField
              width={16}
              fieldPath={`${fieldPathPrefix}.eventNameAlternate`}
              label={i18next.t("Event alternate name")}
              addButtonLabel={i18next.t("Add event alternate name")}
            />
            <DateField
              required
              width={16}
              fieldPath={`${fieldPathPrefix}.eventDate`}
              label={i18next.t("Event date")}
            />
            <GroupField>
              <TextField
                width={12}
                fieldPath={`${fieldPathPrefix}.eventLocation.place`}
                label={i18next.t("Place")}
                required
              />
              <LocalVocabularySelectField
                width={4}
                fieldPath={`${fieldPathPrefix}.eventLocation.country`}
                label={i18next.t("Country")}
                optionsListName="countries"
                required
              />
            </GroupField>

            <Form.Field className="rel-mt-1 rel-mb-1">
              <Button
                aria-label={i18next.t("Remove field")}
                className="close-btn"
                icon
                onClick={() => arrayHelpers.remove(indexPath)}
              >
                <Icon name="close" />
              </Button>
            </Form.Field>
          </React.Fragment>
        );
      }}
    </ArrayField>
  );
};

EventsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

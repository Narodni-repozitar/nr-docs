import React from "react";
import PropTypes from "prop-types";
import { ArrayField, TextField, GroupField } from "react-invenio-forms";
import { i18next } from "@translations/docs_app/i18next";
import { LocalVocabularySelectField } from "@js/oarepo_vocabularies";
import { StringArrayField } from "../StringArray/StringArrayField";
import { ArrayFieldItem, EDTFDaterangePicker } from "@js/oarepo_ui";

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
          <ArrayFieldItem
            indexPath={indexPath}
            arrayHelpers={arrayHelpers}
            className={"invenio-group-field events"}
          >
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
            <EDTFDaterangePicker
              required
              fieldPath={`${fieldPathPrefix}.eventDate`}
              label={i18next.t("Event date")}
              helpText={i18next.t(
                "Write down the time period in which the event took place. If it is not a range, choose same date twice."
              )}
            />
            <GroupField>
              <TextField
                style={{ marginTop: "0.28rem" }}
                width={12}
                fieldPath={`${fieldPathPrefix}.eventLocation.place`}
                label={i18next.t("Place")}
                required
                inline
              />
              <LocalVocabularySelectField
                width={4}
                fieldPath={`${fieldPathPrefix}.eventLocation.country`}
                label={i18next.t("Country")}
                optionsListName="countries"
                required
                clearable
              />
            </GroupField>
          </ArrayFieldItem>
        );
      }}
    </ArrayField>
  );
};

EventsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};

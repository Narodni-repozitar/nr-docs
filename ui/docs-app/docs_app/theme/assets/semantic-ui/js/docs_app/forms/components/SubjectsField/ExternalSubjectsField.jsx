import React from "react";
import PropTypes from "prop-types";
import { SubjectsFieldModal } from "./SubjectsFieldModal";
import { Button, Icon, Form } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { FieldLabel } from "react-invenio-forms";

export const ExternalSubjectsField = ({
  fieldPath,
  helpText,
  defaultNewValue,
  editLabel,
  addLabel,
  addButtonLabel,
  labelIcon,
  label,
  searchAppConfig,
  searchAppUrl,
  suggestionAPIHeaders,
}) => {
  return (
    <Form.Field>
      <FieldLabel label={label} icon={labelIcon} hmtlFor={fieldPath} />
      <SubjectsFieldModal
        suggestionAPIHeaders={suggestionAPIHeaders}
        searchAppConfig={searchAppConfig}
        initialAction="add"
        addLabel={addLabel}
        editLabel={editLabel}
        fieldPath={fieldPath}
        trigger={
          <Button type="button" icon labelPosition="left">
            <Icon name="add" />
            {addButtonLabel}
          </Button>
        }
      />
    </Form.Field>
  );
};

ExternalSubjectsField.defaultProps = {
  addButtonLabel: i18next.t("Add keyword"),
  suggestionAPIHeaders: {
    Accept: "application/vnd.inveniordm.v1+json",
  },
  searchAppConfig: {
    searchApi: {
      url: "",
      withCredentials: false,
      headers: {},
    },
    initialQueryState: {},
    aggs: [],
    sortOptions: [],
    paginationOptions: {},
    layoutOptions: {
      listView: true,
      gridView: false,
    },
    defaultSortingOnEmptyQueryString: {},
  },
};

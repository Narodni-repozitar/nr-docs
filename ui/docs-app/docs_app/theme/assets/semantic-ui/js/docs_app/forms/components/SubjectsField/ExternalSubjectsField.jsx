import React, { useState } from "react";
import PropTypes from "prop-types";
import { SubjectsFieldModal } from "./SubjectsFieldModal";
import { Button, Icon, Form, Dropdown } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { FieldLabel } from "react-invenio-forms";

const schemeOptions = [
  //   { value: "psh", text: "PSH" },
  //   { value: "czenas", text: "Czenas" },
  { value: "institutions", text: "institutions" },
  { value: "resource-types", text: "resource-types" },
];

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
  const [subjectScheme, setSubjectScheme] = React.useState("");

  const [open, setOpen] = React.useState(false);
  const openModal = () => {
    setOpen(true);
  };
  const closeModal = () => {
    setOpen(false);
    setSubjectScheme("");
  };
  return (
    <Form.Field>
      <FieldLabel label={label} icon={labelIcon} hmtlFor={fieldPath} />
      <Dropdown
        button
        text={addButtonLabel}
        options={schemeOptions}
        icon="add"
        labeled
        className="icon"
        selectOnBlur={false}
        value={subjectScheme}
        onChange={(e, { value }) => {
          setSubjectScheme(value);
          openModal();
        }}
      />
      <SubjectsFieldModal
        suggestionAPIHeaders={suggestionAPIHeaders}
        searchAppConfig={searchAppConfig}
        initialAction="add"
        addLabel={addLabel}
        editLabel={editLabel}
        fieldPath={fieldPath}
        open={open}
        closeModal={closeModal}
        openModal={openModal}
        subjectScheme={subjectScheme}
        schemeOptions={schemeOptions}
      />
    </Form.Field>
  );
};

ExternalSubjectsField.defaultProps = {
  addButtonLabel: i18next.t("Add keyword"),
  suggestionAPIHeaders: {
    Accept: "application/json",
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

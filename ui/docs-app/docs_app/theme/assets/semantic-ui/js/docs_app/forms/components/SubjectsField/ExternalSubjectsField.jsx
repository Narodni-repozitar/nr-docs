import React, { useState } from "react";
import PropTypes from "prop-types";
import { SubjectsFieldModal } from "./SubjectsFieldModal";
import { Button, Icon, Form, Dropdown } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { FieldLabel } from "react-invenio-forms";
import { useFormikContext, getIn } from "formik";
import _flatMap from "lodash/flatMap";
import _groupBy from "lodash/groupBy";
const schemeOptions = [
  //   { value: "psh", text: "PSH" },
  //   { value: "czenas", text: "Czenas" },
  { value: "institutions", text: "institutions" },
  { value: "resource-types", text: "resource-types" },
];

const serverData = [
  {
    classificationCode: "uk-1-lekarska-fakulta",
    subject: [
      {
        lang: "cs",
        value: "1. lékařská fakulta",
      },
      {
        lang: "en",
        value: "First Faculty of Medicine",
      },
    ],
    subjectScheme: "institutions",
    valueURI:
      "https://0.0.0.0:5000/vocabularies/institutions/uk-1-lekarska-fakulta",
  },
  {
    classificationCode: "uk-2-lekarska-fakulta",
    subject: [
      {
        lang: "cs",
        value: "2. lékařská fakulta",
      },
      {
        lang: "en",
        value: "Second Faculty of Medicine",
      },
    ],
    subjectScheme: "institutions",
    valueURI:
      "https://0.0.0.0:5000/vocabularies/institutions/uk-2-lekarska-fakulta",
  },
  {
    classificationCode: "uk-3-lekarska-fakulta",
    subject: [
      {
        lang: "cs",
        value: "3. lékařská fakulta",
      },
      {
        lang: "en",
        value: "Third Faculty of Medicine",
      },
    ],
    subjectScheme: "institutions",
    valueURI:
      "https://0.0.0.0:5000/vocabularies/institutions/uk-3-lekarska-fakulta",
  },
];
console.log(_groupBy(serverData, "subjectScheme"));

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
  const { setFieldValue, values } = useFormikContext();
  const initialExternalSubjects = _groupBy(
    getIn(values, fieldPath, {}),
    "subjectScheme"
  );
  // simpler to keep state as an object with keys being the subjectScheme i.e. {psh:[], czesnas:[]} in order
  // to not have complicated logic to allow for same ids in differemt schemes and transform to and from
  // formik state (Formik's state will be a flat array of objects)
  const [externalSubjects, setExternalSubjects] = useState(
    initialExternalSubjects
  );
  console.log(externalSubjects);
  const [open, setOpen] = React.useState(false);
  const openModal = () => {
    setOpen(true);
  };
  const handleRemove = (subject) => {
    const { classificationCode, subjectScheme } = subject;

    setExternalSubjects({
      ...externalSubjects,
      [subjectScheme]: externalSubjects[subjectScheme]?.filter(
        (subject) => subject.classificationCode !== classificationCode
      ),
    });
  };

  const handleCheckboxChange = (subject) => {
    const { classificationCode, subjectScheme } = subject;
    if (
      externalSubjects[subjectScheme]?.find(
        (subject) => subject.classificationCode === classificationCode
      )
    ) {
      handleRemove(subject);
    } else {
      setExternalSubjects({
        ...externalSubjects,
        [subjectScheme]: [...(externalSubjects[subjectScheme] ?? []), subject],
      });
    }
  };

  const handleAddSubjects = () => {
    const subjectsArray = _flatMap(externalSubjects, (array) => array);
    console.log(subjectsArray);
    setFieldValue(fieldPath, subjectsArray);
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
        externalSubjects={externalSubjects}
        handleCheckboxChange={handleCheckboxChange}
        handleRemove={handleRemove}
        setFieldValue={setFieldValue}
        handleAddSubjects={handleAddSubjects}
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

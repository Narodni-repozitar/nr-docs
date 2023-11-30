import React, { useState } from "react";
import PropTypes from "prop-types";
import { SubjectsFieldModal } from "./SubjectsFieldModal";
import { Form, Dropdown } from "semantic-ui-react";
import { i18next } from "@translations/docs_app/i18next";
import { FieldLabel } from "react-invenio-forms";
import { useFormikContext, getIn } from "formik";
import _flatMap from "lodash/flatMap";
import _groupBy from "lodash/groupBy";

const schemeOptions = [
  { value: "psh", text: "PSH" },
  { value: "czenas", text: "Czenas" },
  { value: "institutions", text: "institutions" },
  { value: "resource-types", text: "resource-types" },
];

export const ExternalSubjectsField = ({
  fieldPath,
  addButtonLabel,
  labelIcon,
  label,
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
ExternalSubjectsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  addButtonLabel: PropTypes.string,
  labelIcon: PropTypes.string,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
  suggestionAPIHeaders: PropTypes.object,
};

ExternalSubjectsField.defaultProps = {
  addButtonLabel: i18next.t("Add keyword"),
  suggestionAPIHeaders: {
    Accept: "application/json",
  },
};

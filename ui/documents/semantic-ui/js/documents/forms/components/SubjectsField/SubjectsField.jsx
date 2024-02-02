import React from "react";
import PropTypes from "prop-types";
import { Form, Icon, Divider, Button } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { SubjectsModal } from "./SubjectsModal";
import { useFormikContext, getIn } from "formik";
import _difference from "lodash/difference";
import { FieldLabel } from "react-invenio-forms";

export const SubjectsField = ({ fieldPath }) => {
  const { values, setFieldValue } = useFormikContext();
  const subjects = getIn(values, fieldPath, []);
  const externalSubjects = subjects.filter(
    (subject) => subject?.subjectScheme !== "keyword"
  );
  const regularSubjects = _difference(subjects, externalSubjects).map(
    (subject) => ({ ...subject, id: crypto.randomUUID() })
  );
  const handleSubjectRemoval = (id, lang) => {
    const newRegularSubjects = regularSubjects.map((subject) => {
      if (subject.id === id) {
        subject.subject = subject.subject.filter((s) => s.lang !== lang);
        return subject;
      }
      return subject;
    });
    setFieldValue(fieldPath, [
      ...externalSubjects,
      ...newRegularSubjects
        .filter((subject) => subject?.subject?.length > 0)
        .map((subject) => {
          const { id, ...subjectWithoutId } = subject;
          return subjectWithoutId;
        }),
    ]);
  };
  const handleSubjectAdd = (newSubject) => {
    setFieldValue(fieldPath, [...subjects, newSubject]);
  };
  return (
    <Form.Field className="ui subjects-field">
      <FieldLabel
        htmlFor={fieldPath}
        label={i18next.t("Subjects")}
        icon="pencil"
      />
      {externalSubjects?.length > 0 && (
        <React.Fragment>
          <Divider horizontal section>
            {i18next.t("External subjects (psh, czenas ...)")}
          </Divider>
          {externalSubjects.map(({ subject, valueURI }, i) => (
            <React.Fragment key={i}>
              <a href={valueURI}>
                <span
                  style={{
                    fontSize: "1.1rem",
                    marginRight: "1rem",
                  }}
                >
                  {subject.map((s) => `${s.lang}: ${s.value}  `)}
                </span>
              </a>
            </React.Fragment>
          ))}
        </React.Fragment>
      )}
      {regularSubjects?.length > 0 && (
        <React.Fragment>
          <Divider horizontal section>
            {i18next.t("Free text keywords")}
          </Divider>
          {regularSubjects.map(({ subject, id }) => (
            <React.Fragment key={id}>
              <span
                style={{
                  fontSize: "1.1rem",
                }}
              >
                {subject.map((s, i) => (
                  <span
                    style={{
                      marginRight: "1rem",
                      textWrap: "nowrap",
                      border: "1px solid blue",
                      borderRadius: "5px",
                      padding: "0.2rem",
                      lineHeight: "2rem",
                    }}
                    key={i}
                  >
                    {s.lang}: {s.value}
                    <Button
                      onClick={() => handleSubjectRemoval(id, s.lang)}
                      style={{
                        backgroundColor: "transparent",
                        padding: 0,
                        paddingLeft: "inherit",
                      }}
                      type="button"
                    >
                      <Icon name="close" />
                    </Button>
                  </span>
                ))}
              </span>
            </React.Fragment>
          ))}
        </React.Fragment>
      )}

      <SubjectsModal
        handleSubjectAdd={handleSubjectAdd}
        fieldPath={fieldPath}
        trigger={
          <Form.Button
            type="button"
            icon
            labelPosition="left"
            style={{ marginTop: "1rem" }}
          >
            <Icon name="add" />
            {i18next.t("Add keywords")}
          </Form.Button>
        }
      />
    </Form.Field>
  );
};

SubjectsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};

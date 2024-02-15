import React, { useCallback } from "react";
import PropTypes from "prop-types";
import { Form, Icon, Button, Divider } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { SubjectsModal } from "./SubjectsModal";
import { useFormikContext, getIn } from "formik";
import _difference from "lodash/difference";
import { FieldLabel } from "react-invenio-forms";
import { ExternalSubjects } from "./ExternalSubjects";
import { KeywordSubjects } from "./KeywordSubjects";

export const SubjectsField = ({ fieldPath }) => {
  const { values, setFieldValue } = useFormikContext();
  const subjects = getIn(values, fieldPath, []);
  const externalSubjects = subjects.filter(
    (subject) => subject?.subjectScheme !== "keyword"
  );

  const keywordSubjects = _difference(subjects, externalSubjects).map(
    (subject) => ({
      ...subject,
      id: crypto.randomUUID(),
    })
  );
  const handleSubjectRemoval = useCallback(
    (id, lang) => {
      const newKeywordSubjects = keywordSubjects.map((subject) => {
        if (subject.id === id) {
          subject.subject = subject.subject.filter((s) => s.lang !== lang);
          return subject;
        }
        return subject;
      });
      setFieldValue(fieldPath, [
        ...externalSubjects,
        ...newKeywordSubjects
          .filter((subject) => subject?.subject?.length > 0)
          .map((subject) => {
            const { id, ...subjectWithoutId } = subject;
            return subjectWithoutId;
          }),
      ]);
    },
    [fieldPath, externalSubjects, keywordSubjects, setFieldValue]
  );

  const handleSubjectAdd = useCallback(
    (newSubject) => {
      setFieldValue(fieldPath, [...subjects, newSubject]);
    },
    [fieldPath, subjects, setFieldValue]
  );
  return (
    <Form.Field className="ui subjects-field">
      <FieldLabel
        htmlFor={fieldPath}
        label={i18next.t("Subjects")}
        icon="pencil"
      />
      <ExternalSubjects externalSubjects={externalSubjects} />
      {externalSubjects.length > 0 && (
        <Divider horizontal section>
          {i18next.t("Free text keywords")}
        </Divider>
      )}
      <KeywordSubjects
        keywordSubjects={keywordSubjects}
        externalSubjects={externalSubjects}
        handleSubjectRemoval={handleSubjectRemoval}
      />
      <div>
        <SubjectsModal
          handleSubjectAdd={handleSubjectAdd}
          fieldPath={fieldPath}
          trigger={
            <Button
              className="rel-mt-1"
              type="button"
              icon
              labelPosition="left"
            >
              <Icon name="add" />
              {i18next.t("Add keywords")}
            </Button>
          }
        />
      </div>
    </Form.Field>
  );
};

SubjectsField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
};

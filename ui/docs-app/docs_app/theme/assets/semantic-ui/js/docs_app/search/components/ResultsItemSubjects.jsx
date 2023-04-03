import React from "react";
import PropTypes from "prop-types";

import _groupBy from "lodash/groupBy";
import { Label, List } from "semantic-ui-react";
import { i18next } from "@translations/oarepo_ui/i18next";

const SubjectElement = ({ subject }) => {
  const { subject: subjectName, valueURI, subjectScheme } = subject;
  return subject.valueURI ? (
    <a
      className="subject-link"
      href={valueURI}
      target="_blank"
      title={`${subjectScheme || ""} ${i18next.t("subject definition")}`}
    >
      <span className="subject-name">{subjectName.value}</span>
    </a>
  ) : (
    <span className="subject-name">{subjectName.value}</span>
  );
};

SubjectElement.propTypes = {
  subject: PropTypes.object.isRequired,
};

export function ResultsItemSubjects({ subjects, maxCount = 6, ...rest }) {
  const langGroups = _groupBy(subjects, "subject.lang");

  return Object.entries(langGroups).map(([lang, values]) => (
    <div key={lang}>
      <Label className="green basic lang-tag" size="tiny">
        {lang.toUpperCase()}
      </Label>
      <List horizontal divided size="tiny" style={{ display: "inline" }}>
        {values.slice(0, maxCount).map((sub) => (
          <List.Item
            key={`${sub.subject.lang}-${sub.subject.value}-${sub.valueURI}`}
          >
            <List.Content verticalAlign="middle">
              <SubjectElement subject={sub} />
            </List.Content>
          </List.Item>
        ))}
        {values.length > maxCount && <List.Item>...</List.Item>}
      </List>
    </div>
  ));
}

ResultsItemSubjects.propTypes = {
  subjects: PropTypes.array.isRequired,
  maxCount: PropTypes.number,
};

ResultsItemSubjects.defaultProps = {
  maxCount: 6,
};

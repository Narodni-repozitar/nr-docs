import React from "react";
import PropTypes from "prop-types";
import { Icon, Button, Label } from "semantic-ui-react";

export const KeywordSubjects = ({ keywordSubjects, handleSubjectRemoval }) => {
  return (
    keywordSubjects?.length > 0 && (
      <React.Fragment>
        {keywordSubjects.map(({ subject, id }, index) => (
          <React.Fragment key={id}>
            {subject.map((s, i) => (
              <Label className="keyword-subjects label" key={i}>
                {s.lang}: {s.value}
                <Button
                  className="keyword-subjects-remove-btn p-0 rel-pl-1"
                  onClick={() => handleSubjectRemoval(id, s.lang)}
                  type="button"
                >
                  <Icon name="close" />
                </Button>
              </Label>
            ))}
            {index + 1 !== keywordSubjects.length && (
              <Label className="keyword-subject-divider">|</Label>
            )}
          </React.Fragment>
        ))}
      </React.Fragment>
    )
  );
};

KeywordSubjects.propTypes = {
  keywordSubjects: PropTypes.array.isRequired,
  handleSubjectRemoval: PropTypes.func.isRequired,
};

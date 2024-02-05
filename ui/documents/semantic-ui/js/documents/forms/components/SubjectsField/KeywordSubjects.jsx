import React from "react";
import PropTypes from "prop-types";
import { Divider, Icon, Button, Label } from "semantic-ui-react";
import { i18next } from "@translations/i18next";

export const KeywordSubjects = ({
  keywordSubjects,
  externalSubjects,
  handleSubjectRemoval,
}) => {
  return (
    keywordSubjects?.length > 0 && (
      <React.Fragment>
        {externalSubjects.length > 0 && (
          <Divider horizontal section>
            {i18next.t("Free text keywords")}
          </Divider>
        )}
        {keywordSubjects.map(({ subject, id }, index) => (
          <React.Fragment key={id}>
            {subject.map((s, i) => (
              <Label className="keyword-subjects label" key={i}>
                {s.lang}: {s.value}
                <Button
                  className="keyword-subjects-remove-btn"
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
  externalSubjects: PropTypes.array.isRequired,
  handleSubjectRemoval: PropTypes.func.isRequired,
};

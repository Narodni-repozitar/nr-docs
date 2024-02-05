import React from "react";
import { i18next } from "@translations/i18next";
import { Divider, Label } from "semantic-ui-react";
import PropTypes from "prop-types";

export const ExternalSubjects = ({ externalSubjects }) => {
  return (
    externalSubjects?.length > 0 && (
      <React.Fragment>
        <Divider horizontal section>
          {i18next.t("External subjects (psh, czenas ...)")}
        </Divider>
        {externalSubjects.map(({ subject, valueURI }, i) => (
          <Label key={i} className="external-subjects label">
            <a href={valueURI}>
              {subject.map((s) => `${s.lang}: ${s.value}  `)}
            </a>
          </Label>
        ))}
      </React.Fragment>
    )
  );
};

ExternalSubjects.propTypes = { externalSubjects: PropTypes.array.isRequired };

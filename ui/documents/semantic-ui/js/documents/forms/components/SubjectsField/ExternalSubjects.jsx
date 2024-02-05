import React from "react";
import { i18next } from "@translations/i18next";
import { Divider } from "semantic-ui-react";
import PropTypes from "prop-types";

export const ExternalSubjects = ({ externalSubjects }) => {
  return (
    externalSubjects?.length > 0 && (
      <React.Fragment>
        <Divider horizontal section>
          {i18next.t("External subjects (psh, czenas ...)")}
        </Divider>
        {externalSubjects.map(({ subject, valueURI }, i) => (
          <React.Fragment key={i}>
            <a href={valueURI}>
              <span className="external-subjects label">
                {subject.map((s) => `${s.lang}: ${s.value}  `)}
              </span>
            </a>
          </React.Fragment>
        ))}
      </React.Fragment>
    )
  );
};

ExternalSubjects.propTypes = { externalSubjects: PropTypes.array.isRequired };

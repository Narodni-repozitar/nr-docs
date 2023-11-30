import React from "react";
import { List, Container, Checkbox } from "semantic-ui-react";
import { withState } from "react-searchkit";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import _truncate from "lodash/truncate";
import { object2array } from "@js/oarepo_ui";

export const ResultsList = withState(
  ({
    currentResultsState: results,
    multiple,
    fieldPath,
    onClose,
    subjectScheme,
    externalSubjects,
    handleCheckboxChange,
  }) => {
    return (
      <Overridable id="ExternalApiSuggestions.container" results={results}>
        <Container>
          <List relaxed="very">
            {results?.data.hits?.map((record) => {
              const { title, id, links } = record;
              const serializedSubject = {
                classificationCode: id,
                subjectScheme,
                valueURI: links?.self_html,
                subject: object2array(title, "lang", "value"),
              };
              return (
                <List.Item key={id}>
                  <Checkbox
                    onChange={() => handleCheckboxChange(serializedSubject)}
                    checked={
                      !!externalSubjects[subjectScheme]?.find(
                        (selectedSubject) =>
                          selectedSubject.classificationCode === id
                      )
                    }
                  />
                  {title.cs}
                  <a href={links?.self_html}>
                    {links.self_html &&
                      _truncate(links.self_html, {
                        length: 40,
                        omission: "...",
                      })}
                  </a>
                </List.Item>
              );
            })}
          </List>
        </Container>
      </Overridable>
    );
  }
);

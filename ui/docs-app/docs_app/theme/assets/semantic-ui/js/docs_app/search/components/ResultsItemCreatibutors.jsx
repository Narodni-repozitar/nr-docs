import React from "react";

import { List } from "semantic-ui-react";

import { DoubleSeparator } from "./DoubleSeparator";
import { IconPersonIdentifier } from "./IconPersonIdentifier";

import _get from "lodash/get";
import { i18next } from "@translations/docs_app/i18next";

export function ResultsItemCreatibutors({
  creators = [],
  contributors = [],
  maxCreators = 3,
  maxContributors = 3,
  searchUrl,
  className,
}) {
  let spanClass = "creatibutor-wrap separated";
  className && (spanClass += ` ${className}`);

  function getIcons(personName = "No name", identifiers = []) {
    let icons = identifiers.map((i) => (
      <IconPersonIdentifier
        key={`${i.scheme}:${i.identifier}`}
        identifier={i}
        personName={personName}
      />
    ));
    return icons;
  }

  function getLink(personName = "No name", searchField = "creators") {
    let link = (
      <a
        className="creatibutor-link"
        href={`${searchUrl}?q=&f=metadata_${searchField}_fullName:${personName}`}
        title={`${personName}: ${i18next.t(
          "Find more records by this person"
        )}`}
      >
        <span className="creatibutor-name">{personName}</span>
      </a>
    );
    return link;
  }

  return (
    <>
      <List horizontal divided className="inline">
        {creators
          .slice(0, maxCreators)
          .map(({ fullName, authorityIdentifiers }) => (
            <List.Item as="span" className={spanClass} key={fullName}>
              {getLink(fullName)}
              {getIcons(fullName, authorityIdentifiers)}
            </List.Item>
          ))}
      </List>
      <DoubleSeparator />
      <List horizontal divided className="inline">
        {contributors
          .slice(0, maxContributors)
          .map(({ fullName, authorityIdentifiers, role }) => (
            <List.Item as="span" className={spanClass} key={fullName}>
              {getLink(fullName, "contributors")}
              {getIcons(fullName, authorityIdentifiers)}
              {role && <span className="contributor-role">({role.title})</span>}
            </List.Item>
          ))}
      </List>
    </>
  );
}

import React from "react";

import { List } from "semantic-ui-react";

import { DoubleSeparator } from "./DoubleSeparator";
import { IconPersonIdentifier } from "./IconPersonIdentifier";

import _get from "lodash/get";
import _groupBy from "lodash/groupBy";
import _toPairs from "lodash/toPairs";
import _join from "lodash/join";

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

  const uniqueContributors = _toPairs(
    _groupBy(
      contributors.slice(0, maxContributors),
      ({ fullName, authorityIdentifiers = [] }) => {
        const idKeys = _join(
          authorityIdentifiers.map((i) => `${i.scheme}:${i.identifier}`),
          ";"
        );
        return `${fullName}-${idKeys}`;
      }
    )
  ).map(([groupKey, entries]) => ({
    id: groupKey,
    fullName: entries[0].fullName,
    authorityIdentifiers: entries[0].authorityIdentifiers,
    roles: _join(
      entries.map(({ role }) => role.title),
      ", "
    ),
  }));

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
        href={`${searchUrl}?q=&f=metadata_${searchField}_fullName:${encodeURI(
          personName
        )}`}
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
      {uniqueContributors.length > 0 && <DoubleSeparator />}
      <List horizontal divided className="inline">
        {uniqueContributors.map(({ id, fullName, identifiers, roles }) => (
          <List.Item as="span" className={spanClass} key={id}>
            {getLink(fullName, "contributors")}
            {getIcons(fullName, identifiers)}
            {roles && <span className="contributor-role">({roles})</span>}
          </List.Item>
        ))}
      </List>
    </>
  );
}

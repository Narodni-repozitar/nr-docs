import React from "react";

import { List } from "semantic-ui-react";

import _get from "lodash/get";
import { i18next } from "@translations/docs_app/i18next";

export function ResultsItemCreatibutors({
  creators = [],
  contributors = [],
  maxCreators = 3,
  maxContributors = 3,
  className,
}) {
  let spanClass = "creatibutor-wrap separated";
  className && (spanClass += ` ${className}`);

  function makeIcon(scheme, identifier, name) {
    let link = null;
    let linkTitle = null;
    let icon = null;
    let alt = "";

    switch (scheme) {
      case "orcid":
        link = `https://orcid.org/${identifier}`;
        linkTitle = i18next.t("ORCID profile");
        icon = "/static/images/orcid.svg";
        alt = "ORCID logo";
        break;
      case "ror":
        link = `https://ror.org/${identifier}`;
        linkTitle = i18next.t("ROR profile");
        icon = "/static/images/ror-icon.svg";
        alt = "ROR logo";
        break;
      case "gnd":
        link = `https://d-nb.info/gnd/${identifier}`;
        linkTitle = i18next.t("GND profile");
        icon = "/static/images/gnd-icon.svg";
        alt = "GND logo";
        break;
      default:
        return null;
    }

    icon = (
      <a
        className="no-text-decoration mr-0"
        href={link}
        aria-label={`${name}: ${linkTitle}`}
        title={`${name}: ${linkTitle}`}
        key={scheme}
      >
        <img className="inline-id-icon ml-5" src={icon} alt={alt} />
      </a>
    );
    return icon;
  }

  function getIcons(creator) {
    let ids = _get(creator, "person_or_org.identifiers", []);
    let creatorName = _get(creator, "person_or_org.name", "No name");
    let icons = ids.map((c) => makeIcon(c.scheme, c.identifier, creatorName));
    return icons;
  }

  function getLink(creator) {
    let creatorName = _get(creator, "fullName", "No name");
    let link = (
      <a
        className="creatibutor-link"
        href={`/search?q=metadata.creators.person_or_org.name:"${creatorName}"`}
        title={`${creatorName}: ${i18next.t("Search")}`}
      >
        <span className="creatibutor-name">{creatorName}</span>
      </a>
    );
    return link;
  }

  return (
    <>
      <List horizontal divided className="inline">
        {creators.slice(0, maxCreators).map((creator) => (
          <List.Item as="span" className={spanClass} key={creator.fullName}>
            {getLink(creator)}
            {getIcons(creator)}
          </List.Item>
        ))}
      </List>
      a
      <List horizontal divided className="inline">
        {contributors.slice(0, maxContributors).map((creator) => (
          <List.Item as="span" className={spanClass} key={creator.fullName}>
            {getLink(creator)}
            {getIcons(creator)}
          </List.Item>
        ))}
      </List>
    </>
  );
}

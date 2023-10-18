import React from "react";
import { Image } from "semantic-ui-react";

export const ResultsItemLicense = ({ rights = [] }) => {
  const licenseBadges = rights.map((r) => ({
    ...r,
    badge: r.id === "3-BY-ND-CZ" ? "by-nd.png" : null,
  }));
  return licenseBadges.map(
    ({ id, title, type, badge }) =>
      badge && (
        <Image
          as="a"
          href={`/vocabularies/licenses/${id}`}
          key={id}
          centered
          fluid
          className="license-rights"
          src={`/static/images/licenses/${badge}`}
          title={title}
          aria-label={title}
        />
      )
  );
};

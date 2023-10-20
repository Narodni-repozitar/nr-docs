import React from "react";
import { Image } from "semantic-ui-react";

export const ResultsItemAccessStatus = ({ status }) => {
  const { id, title } = status;
  const iconFile = id === "c_abf2" ? "zamky_open_access.svg" : null;
  return (
    iconFile && (
      <Image
        as="a"
        href={`/vocabularies/access-rights/${id}`}
        centered
        fluid
        title={title}
        aria-label={title}
        className={`access-status ${title}`}
        src={`/static/icons/locks/${iconFile}`}
      />
    )
  );
};

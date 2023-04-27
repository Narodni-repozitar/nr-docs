import React from "react";

export const SearchFacetLink = ({
  searchUrl = "/",
  searchFacet,
  value,
  title,
  label,
  className,
  ...rest
}) => (
  <a
    className={`${className} ui search link`}
    href={`${searchUrl}?q=&f=${searchFacet}:${encodeURI(value)}`}
    aria-label={title}
    title={title}
    {...rest}
  >
    <span className={`${className} label`}>{label || value}</span>
  </a>
);

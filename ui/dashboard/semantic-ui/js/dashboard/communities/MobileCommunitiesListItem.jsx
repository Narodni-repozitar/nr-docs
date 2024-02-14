// This file is part of InvenioRDM
// Copyright (C) 2022 CERN.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_app_rdm/i18next";
import React from "react";
import { Image } from "react-invenio-forms";
import { Grid, Icon, Header } from "semantic-ui-react";
import PropTypes from "prop-types";
import { CommunityTypeLabel } from "./CommunityTypeLabel";
import { RestrictedLabel } from "./RestrictedLabel";

export const MobileCommunitiesListItem = ({
  result,
  communityTypeLabelTransparent,
  isRestricted,
}) => {
  const communityType = result.ui?.type?.title_l10n;
  return (
    <Grid className="mobile only item result-list-item community rel-mb-1 rel-p-1">
      {isRestricted && (
        <Grid.Row>
          <Grid.Column width={16} verticalAlign="middle" className="pl-0 pr-0">
            <RestrictedLabel access={result.access.visibility} />
          </Grid.Column>
        </Grid.Row>
      )}

      <Grid.Row verticalAlign="middle">
        <Grid.Column width={16} verticalAlign="middle" className="pl-0 pr-0">
          <div className="flex align-items-center">
            <div>
              <Image
                wrapped
                src={result.links.logo}
                size="mini"
                className="community-image rel-mr-1"
                alt=""
              />
            </div>
            <div>
              <Header as="h4">
                <a className="truncate-lines-2" href={result?.links?.members}>
                  {result.metadata.title}
                </a>
              </Header>
            </div>
          </div>
        </Grid.Column>
      </Grid.Row>

      {result.metadata.description && (
        <Grid.Row className="pt-0">
          <Grid.Column width={16} className="pl-0 pr-0">
            <p className="truncate-lines-1 text size small text-muted mt-5">
              {result.metadata.description}
            </p>
          </Grid.Column>
        </Grid.Row>
      )}

      {(communityType ||
        result.metadata.website ||
        result.metadata.organizations) && (
        <Grid.Row className="pt-0">
          <Grid.Column width={16} verticalAlign="bottom" className="pl-0 pr-0">
            <div className="text size small text-muted">
              {communityType && (
                <div className="mb-5">
                  <CommunityTypeLabel
                    transparent={communityTypeLabelTransparent}
                    type={communityType}
                  />
                </div>
              )}

              {result.metadata.website && (
                <div className="rel-mr-1 mb-5">
                  <Icon name="linkify" />
                  <a
                    href={result.metadata.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-muted"
                  >
                    {result.metadata.website}
                  </a>
                </div>
              )}

              {result.metadata.organizations && (
                <div className="mb-5">
                  <Icon name="building outline" />
                  {result.metadata.organizations.map((org, index) => {
                    const separator = (index > 0 && ", ") || "";

                    return (
                      <span className="text-muted" key={org.name}>
                        {separator}
                        {org.name}
                        {org.id && (
                          <a
                            href={`https://ror.org/${org.id}`}
                            aria-label={`${org.name}'s ROR ${i18next.t(
                              "profile"
                            )}`}
                            title={`${org.name}'s ROR ${i18next.t("profile")}`}
                            target="_blank"
                            rel="noreferrer"
                          >
                            <img
                              className="inline-id-icon ml-5"
                              src="/static/images/ror-icon.svg"
                              alt=""
                            />
                          </a>
                        )}
                      </span>
                    );
                  })}
                </div>
              )}
            </div>
          </Grid.Column>
        </Grid.Row>
      )}
    </Grid>
  );
};

MobileCommunitiesListItem.propTypes = {
  result: PropTypes.object.isRequired,
  communityTypeLabelTransparent: PropTypes.bool,
  isRestricted: PropTypes.bool,
};

MobileCommunitiesListItem.defaultProps = {
  communityTypeLabelTransparent: false,
};

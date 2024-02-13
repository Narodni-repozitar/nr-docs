// This file is part of InvenioRDM
// Copyright (C) 2022 CERN.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_app_rdm/i18next";
import React from "react";
import { Image } from "react-invenio-forms";
import { Button, Grid, Icon, Header } from "semantic-ui-react";
import PropTypes from "prop-types";
import { CommunityTypeLabel } from "./CommunityTypeLabel";
import { RestrictedLabel } from "./RestrictedLabel";

export const ComputerTabledCommunitiesListItem = ({
  result,
  communityTypeLabelTransparent,
  isRestricted,
}) => {
  const communityType = result.ui?.type?.title_l10n;
  const canUpdate = result.ui?.permissions?.can_update;

  return (
    <Grid className="computer tablet only item result-list-item community rel-mb-1 rel-p-1">
      <Grid.Column
        tablet={(canUpdate && 13) || 16}
        computer={13}
        verticalAlign="middle"
        className="pl-0"
      >
        <div className="flex align-items-center">
          <Image
            wrapped
            src={result.links.logo}
            size="small"
            className="community-image rel-mr-2"
            alt=""
          />
          <div>
            {result.access.visibility === "restricted" && (
              <div className="rel-mb-1">
                <RestrictedLabel access={result.access.visibility} />
              </div>
            )}
            <Header as="h4">
              <a className="truncate-lines-2" href={result?.links?.members}>
                {result.metadata.title}
              </a>
            </Header>
            {result.metadata.description && (
              <p className="truncate-lines-1 text size small text-muted mt-5">
                {result.metadata.description}
              </p>
            )}

            {(communityType ||
              result.metadata.website ||
              result.metadata.organizations) && (
              <div className="flex align-items-center wrap mt-5 text size small text-muted">
                {communityType && (
                  <CommunityTypeLabel
                    transparent={communityTypeLabelTransparent}
                    type={communityType}
                  />
                )}

                {result.metadata.website && (
                  <div className="rel-mr-1">
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
                  <div>
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
                              title={`${org.name}'s ROR ${i18next.t(
                                "profile"
                              )}`}
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
            )}
          </div>
        </div>
      </Grid.Column>

      {canUpdate && (
        <Grid.Column width={3} textAlign="right" className="pr-0">
          <div>
            <Button
              compact
              size="small"
              href={result.links.settings_html}
              className="mt-0 mr-0"
              labelPosition="left"
              icon="edit"
              content={i18next.t("Edit")}
            />
          </div>
        </Grid.Column>
      )}
    </Grid>
  );
};

ComputerTabledCommunitiesListItem.propTypes = {
  result: PropTypes.object.isRequired,
  communityTypeLabelTransparent: PropTypes.bool,
  isRestricted: PropTypes.bool,
};

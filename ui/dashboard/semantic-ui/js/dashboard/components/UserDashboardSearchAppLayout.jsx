// This file is part of InvenioRDM
// Copyright (C) 2020-2022 CERN.
// Copyright (C) 2020-2021 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
// Copyright (C) 2021 New York University.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { SearchAppResultsPane } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/i18next";
import React from "react";
import { SearchBar } from "react-searchkit";
import { GridResponsiveSidebarColumn } from "react-invenio-forms";
import { Grid, Button, Container } from "semantic-ui-react";
import PropTypes from "prop-types";
import { SearchAppFacets } from "@js/oarepo_ui";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export const UserDashboardSearchAppLayoutHOC = ({
  placeholder,
  extraContent,
  extraRow,
  appName,
}) => {
  const DashboardUploadsSearchLayout = (props) => {
    const [sidebarVisible, setSidebarVisible] = React.useState(false);
    const { config } = props;
    return (
      <QueryClientProvider client={queryClient}>
        <Container className="rel-mt-4 rel-mb-4">
          <Grid>
            <GridResponsiveSidebarColumn
              width={3}
              open={sidebarVisible}
              onHideClick={() => setSidebarVisible(false)}
            >
              <SearchAppFacets aggs={config.aggs} appName={appName} />
            </GridResponsiveSidebarColumn>
            <Grid.Column computer={13} mobile={16} tablet={16}>
              <Grid columns="equal">
                <Grid.Row only="computer" verticalAlign="middle">
                  <Grid.Column>
                    <SearchBar placeholder={placeholder} className="rel-pl-1" />
                  </Grid.Column>
                  {extraContent()}
                </Grid.Row>
                <Grid.Column only="mobile tablet" mobile={2} tablet={2}>
                  <Button
                    basic
                    icon="sliders"
                    onClick={() => setSidebarVisible(true)}
                    aria-label={i18next.t("Filter results")}
                  />
                </Grid.Column>

                <Grid.Column
                  only="mobile tablet"
                  mobile={14}
                  tablet={14}
                  floated="right"
                >
                  <SearchBar placeholder={placeholder} />
                </Grid.Column>
                <Grid.Row only="tablet mobile" verticalAlign="middle">
                  {extraContent()}
                </Grid.Row>
                {extraRow && (
                  <Grid.Row verticalAlign="middle" only="mobile">
                    {extraRow}
                  </Grid.Row>
                )}
                <Grid.Row>
                  <Grid.Column mobile={16} tablet={16} computer={16}>
                    <SearchAppResultsPane
                      layoutOptions={config.layoutOptions}
                      appName={appName}
                    />
                  </Grid.Column>
                </Grid.Row>
              </Grid>
            </Grid.Column>
          </Grid>
        </Container>
      </QueryClientProvider>
    );
  };

  DashboardUploadsSearchLayout.propTypes = {
    config: PropTypes.object.isRequired,
  };

  return DashboardUploadsSearchLayout;
};

UserDashboardSearchAppLayoutHOC.propTypes = {
  placeholder: PropTypes.string,
  extraContent: PropTypes.func,
  extraRow: PropTypes.func,
  appName: PropTypes.string,
};

UserDashboardSearchAppLayoutHOC.defaultProps = {
  extraContent: () => null,
  extraRow: null,
  appName: undefined,
  placeholder: "",
};

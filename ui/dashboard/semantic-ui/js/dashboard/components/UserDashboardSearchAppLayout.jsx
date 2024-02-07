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
import Overridable from "react-overridable";
import { SearchAppFacets, SearchAppSort } from "@js/oarepo_ui";
import { UserDashboardMobileTabletNav } from "./UserDashboardMobileTabletNav";

const Sidebar = () => <div>This is the sidebar</div>;

export const UserDashboardSearchAppLayoutHOC = ({
  searchBarPlaceholder = "",
  topRow = () => (
    <Grid.Column mobile={6} tablet={6} computer={4}>
      <SearchBar placeholder={searchBarPlaceholder} />
    </Grid.Column>
  ),
  appName = undefined,
}) => {
  const DashboardUploadsSearchLayout = (props) => {
    const [sidebarVisible, setSidebarVisible] = React.useState(false);
    const { config } = props;
    return (
      <Container className="rel-mt-2 rel-mb-2">
        <Grid>
          <UserDashboardMobileTabletNav />
          <GridResponsiveSidebarColumn
            width={3}
            open={sidebarVisible}
            onHideClick={() => setSidebarVisible(false)}
          >
            <Sidebar />
          </GridResponsiveSidebarColumn>
          <Grid.Column computer={13} mobile={16} tablet={16}>
            <Grid columns="equal">
              <Grid.Row only="computer" verticalAlign="middle">
                <Grid.Column width={5}>
                  <SearchBar
                    placeholder={searchBarPlaceholder}
                    className="rel-pl-1"
                  />
                </Grid.Column>
                <Grid.Column width={3}>
                  <div>Filter cmp</div>
                </Grid.Column>
                <Grid.Column floated="right" textAlign="right">
                  <SearchAppSort options={config.sortOptions} />
                </Grid.Column>
              </Grid.Row>
              <Grid.Row only="mobile tablet" width={16} verticalAlign="middle">
                <Grid.Column mobile={1} tablet={1}>
                  <Button
                    basic
                    icon="sliders"
                    onClick={() => setSidebarVisible(true)}
                    aria-label={i18next.t("Filter results")}
                  />
                </Grid.Column>
                <Grid.Column only="tablet" tablet={15}>
                  <Grid>
                    <Grid.Row verticalAlign="middle" width={16}>
                      <Grid.Column width={8} floated="left">
                        <SearchBar
                          placeholder={searchBarPlaceholder}
                          className="rel-pl-1"
                        />
                      </Grid.Column>
                      <Grid.Column width={3}>
                        <div>Filter cmp</div>
                      </Grid.Column>
                      <Grid.Column floated="right" textAlign="right" width={5}>
                        <SearchAppSort options={config.sortOptions} />
                      </Grid.Column>
                    </Grid.Row>
                  </Grid>
                </Grid.Column>
                <Grid.Column only="mobile" mobile={14}>
                  <Grid>
                    <Grid.Row verticalAlign="middle" width={16}>
                      <Grid.Column className="rel-ml-1" width={16}>
                        <SearchBar
                          placeholder={searchBarPlaceholder}
                          className="rel-pl-1"
                        />
                      </Grid.Column>
                    </Grid.Row>
                  </Grid>
                </Grid.Column>
                {/* {topRow()} */}

                {/* <Grid.Column floated="right" width={4}>
                  <SearchAppSort
                    options={config.sortOptions}
                    className="rel-mr-1"
                  />
                </Grid.Column> */}
              </Grid.Row>
              <Grid.Row only="mobile">
                <Grid.Column>
                  <SearchAppSort options={config.sortOptions} />
                </Grid.Column>
              </Grid.Row>

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
    );
  };

  DashboardUploadsSearchLayout.propTypes = {
    config: PropTypes.object.isRequired,
  };

  return DashboardUploadsSearchLayout;
};

import React, { useState, useEffect } from "react";
import { Grid, Menu, MenuItem } from "semantic-ui-react";
import { i18next } from "@translations/i18next";

export const UserDashboardMobileTabletNav = () => {
  const [currentLocation, setCurrentLocation] = useState(null);
  console.log(currentLocation);

  useEffect(() => {
    const updateLocation = () => {
      setCurrentLocation(window.location.href);
    };

    window.addEventListener("hashchange", updateLocation);

    updateLocation();

    return () => {
      window.removeEventListener("hashchange", updateLocation);
    };
  }, []);
  return (
    <Grid.Row width={16} only="tablet mobile">
      <Grid.Column textAlign="left">
        <Menu
          as="nav"
          borderless
          style={{ boxShadow: "none" }}
          compact
          className="pl-0"
        >
          <MenuItem
            name="records"
            active={currentLocation?.includes("/me/records")}
            //   active={activeItem === "editorials"}
            onClick={() => (window.location.href = "/me/records")}
          >
            {i18next.t("Records")}
          </MenuItem>

          <MenuItem
            name="communities"
            active={currentLocation?.includes("/me/communities")}
            onClick={() => (window.location.href = "/me/communities")}
          >
            {i18next.t("Communities")}
          </MenuItem>

          <MenuItem
            name="requests"
            active={currentLocation?.includes("/me/requests")}
            onClick={() => (window.location.href = "/me/requests")}
          >
            {i18next.t("Requests")}
          </MenuItem>
        </Menu>
      </Grid.Column>
    </Grid.Row>
  );
};

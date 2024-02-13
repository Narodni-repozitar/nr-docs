// This file is part of InvenioRDM
// Copyright (C) 2022 CERN.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/i18next";
import React from "react";
import PropTypes from "prop-types";
import { Item, Label } from "semantic-ui-react";

export const MobileRecordsListItem = ({ result, uiMetadata }) => {
  const { abstract, title, resourceType, createdDate, viewLink, accessRights } =
    uiMetadata;

  return (
    <Item
      key={result.id}
      className="mobile only rel-p-1 rel-mb-1 result-list-item record"
    >
      <Item.Content>
        <Item.Extra>
          <Label size="tiny">{resourceType.title}</Label>
          <Label size="tiny">{accessRights.title}</Label>
        </Item.Extra>
        <Item.Header as="h2">
          <a href={viewLink}>{title}</a>
        </Item.Header>
        <Item.Description>{abstract}</Item.Description>
        <Item.Extra>
          <Item.Extra>
            <div>
              <small>
                {createdDate ? (
                  <>
                    {i18next.t("Uploaded on {{uploadDate}}", {
                      uploadDate: createdDate,
                    })}
                  </>
                ) : (
                  i18next.t("No creation date found.")
                )}
              </small>
            </div>
          </Item.Extra>
        </Item.Extra>
      </Item.Content>
    </Item>
  );
};

MobileRecordsListItem.propTypes = {
  result: PropTypes.object.isRequired,
  uiMetadata: PropTypes.object.isRequired,
};

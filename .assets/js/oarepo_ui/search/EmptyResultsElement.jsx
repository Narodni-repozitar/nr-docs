import React from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/oarepo_ui/i18next";
import { Button, Header, Icon, Segment } from "semantic-ui-react";

export const EmptyResultsElement = ({
  queryString,
  resetQuery,
  extraContent,
}) => {
  return (
    <Segment placeholder textAlign="center">
      <Header icon>
        <Icon name="search" />
      </Header>
      {queryString && (
        <em>
          {i18next.t("We couldn't find any matches for ")} "{queryString}"
        </em>
      )}
      <br />
      <Button primary onClick={() => resetQuery()}>
        {i18next.t("Start over")}
      </Button>
      {extraContent}
    </Segment>
  );
};

EmptyResultsElement.propTypes = {
  queryString: PropTypes.string,
  resetQuery: PropTypes.func.isRequired,
  extraContent: PropTypes.node,
};

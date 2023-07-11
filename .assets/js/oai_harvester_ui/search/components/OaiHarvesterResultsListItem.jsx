import React, { useContext } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

import _get from "lodash/get";
import _join from "lodash/join";
import _truncate from "lodash/truncate";


import { Item, Label, Icon } from "semantic-ui-react";
import { withState, buildUID } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";


export const OaiHarvesterResultsListItemComponent = ({
  currentQueryState,
  result,
  appName,
}) => {
  const searchAppConfig = useContext(SearchConfigurationContext);
  // console.log(result);
  const name = _get(result, "name");
  const url = _get(result, "baseurl");
  const code = _get(result, "code");
  const viewLink = new URL(
      result.links.self,
    new URL(searchAppConfig.ui_endpoint, window.location.origin)
  );
  return (
    <Overridable
      id={buildUID("RecordsResultsListItem.layout", "", appName)}
      result={result}
      name={name}
    >
      <Item key={result.id}>
        <Item.Content>
          <Item.Extra className="labels-actions"></Item.Extra>
          <Item.Header as="h2">
            <a href={viewLink}>{name}</a>
          </Item.Header>
          <Item.Description>
            {code} - {url}
          </Item.Description>
        </Item.Content>
      </Item>
    </Overridable>
  );
};

OaiHarvesterResultsListItemComponent.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiHarvesterResultsListItemComponent.defaultProps = {
  currentQueryState: null,
  appName: "",
};


export const OaiHarvesterResultsListItem = (props) => {
  return (
    <Overridable
      id={buildUID("OaiHarvesterResultsListItem", "", props.appName)}
      {...props}
    >
      <OaiHarvesterResultsListItemComponent {...props} />
    </Overridable>
  );
};

OaiHarvesterResultsListItem.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiHarvesterResultsListItem.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const OaiHarvesterResultsListItemWithState = withState(
  ({ currentQueryState, result, appName }) => (
    <OaiHarvesterResultsListItem
      currentQueryState={currentQueryState}
      result={result}
      appName={appName}
    />
  )
);

OaiHarvesterResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

OaiHarvesterResultsListItemComponent.defaultProps = {
  currentQueryState: null,
};
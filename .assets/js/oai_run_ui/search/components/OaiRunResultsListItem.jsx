import React, { useContext } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

import _get from "lodash/get";
import _join from "lodash/join";
import _truncate from "lodash/truncate";


import { Item, Label, Icon } from "semantic-ui-react";
import { withState, buildUID } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";


export const OaiRunResultsListItemComponent = ({
  currentQueryState,
  result,
  appName,
}) => {
  const searchAppConfig = useContext(SearchConfigurationContext);
  const id = _get(result, "id");
  const started =_get(result, "started");
  const harvester =_get(result, "harvester.name");
  const viewLink = new URL(
      result.links.self,
    new URL(searchAppConfig.ui_endpoint, window.location.origin)
  );
  return (
    <Overridable
      id={buildUID("RecordsResultsListItem.layout", "", appName)}
      result={result}
      name={id}
    >
      <Item key={result.id}>
        <Item.Content>
          <Item.Extra className="labels-actions"></Item.Extra>
          <Item.Header as="h2">
            <a href={viewLink}>Run - {id}</a>
          </Item.Header>
          <Item.Description>
            {harvester}
            <br/>
            Start - {started}
          </Item.Description>
        </Item.Content>
      </Item>
    </Overridable>
  );
};

OaiRunResultsListItemComponent.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiRunResultsListItemComponent.defaultProps = {
  currentQueryState: null,
  appName: "",
};


export const OaiRunResultsListItem = (props) => {
  return (
    <Overridable
      id={buildUID("OaiRunResultsListItem", "", props.appName)}
      {...props}
    >
      <OaiRunResultsListItemComponent {...props} />
    </Overridable>
  );
};

OaiRunResultsListItem.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiRunResultsListItem.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const OaiRunResultsListItemWithState = withState(
  ({ currentQueryState, result, appName }) => (
    <OaiRunResultsListItem
      currentQueryState={currentQueryState}
      result={result}
      appName={appName}
    />
  )
);

OaiRunResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

OaiRunResultsListItemComponent.defaultProps = {
  currentQueryState: null,
};
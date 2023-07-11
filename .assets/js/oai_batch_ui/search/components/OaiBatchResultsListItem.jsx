import React, { useContext } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

import _get from "lodash/get";



import { Item, Label, Icon } from "semantic-ui-react";
import { withState, buildUID } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";


export const OaiBatchResultsListItemComponent = ({
  currentQueryState,
  result,
  appName,
}) => {
  const searchAppConfig = useContext(SearchConfigurationContext);
  const id = _get(result, "id");
  const run =  _get(result, "run.id");
  const started = _get(result, "started");
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
            <a href={viewLink}>Batch - {id}</a>
          </Item.Header>
          <Item.Description>
            <b>Run</b> - {run}
            <br/>
            <b>Start</b> - {started}
          </Item.Description>
        </Item.Content>
      </Item>
    </Overridable>
  );
};

OaiBatchResultsListItemComponent.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiBatchResultsListItemComponent.defaultProps = {
  currentQueryState: null,
  appName: "",
};


export const OaiBatchResultsListItem = (props) => {
  return (
    <Overridable
      id={buildUID("OaiBatchResultsListItem", "", props.appName)}
      {...props}
    >
      <OaiBatchResultsListItemComponent {...props} />
    </Overridable>
  );
};

OaiBatchResultsListItem.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiBatchResultsListItem.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const OaiBatchResultsListItemWithState = withState(
  ({ currentQueryState, result, appName }) => (
    <OaiBatchResultsListItem
      currentQueryState={currentQueryState}
      result={result}
      appName={appName}
    />
  )
);

OaiBatchResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

OaiBatchResultsListItemComponent.defaultProps = {
  currentQueryState: null,
};
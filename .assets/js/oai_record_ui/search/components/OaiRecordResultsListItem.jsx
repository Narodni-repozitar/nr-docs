import React, { useContext } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

import _get from "lodash/get";
import _join from "lodash/join";
import _truncate from "lodash/truncate";


import { Item, Label, Icon } from "semantic-ui-react";
import { withState, buildUID } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";


export const OaiRecordResultsListItemComponent = ({
  currentQueryState,
  result,
  appName,
}) => {
  const searchAppConfig = useContext(SearchConfigurationContext);
  const id = _get(result, "oai_identifier");
  const title =_get(result, "entry.metadata.title");
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
            <a href={viewLink}>{id}</a>
          </Item.Header>
          <Item.Description>
            {title}
          </Item.Description>
        </Item.Content>
      </Item>
    </Overridable>
  );
};

OaiRecordResultsListItemComponent.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiRecordResultsListItemComponent.defaultProps = {
  currentQueryState: null,
  appName: "",
};


export const OaiRecordResultsListItem = (props) => {
  return (
    <Overridable
      id={buildUID("OaiRecordResultsListItem", "", props.appName)}
      {...props}
    >
      <OaiRecordResultsListItemComponent {...props} />
    </Overridable>
  );
};

OaiRecordResultsListItem.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

OaiRecordResultsListItem.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const OaiRecordResultsListItemWithState = withState(
  ({ currentQueryState, result, appName }) => (
    <OaiRecordResultsListItem
      currentQueryState={currentQueryState}
      result={result}
      appName={appName}
    />
  )
);

OaiRecordResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

OaiRecordResultsListItemComponent.defaultProps = {
  currentQueryState: null,
};
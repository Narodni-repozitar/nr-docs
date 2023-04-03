import React, { useContext } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

import _get from "lodash/get";
import _join from "lodash/join";
import _truncate from "lodash/truncate";

import { Item, Label, Icon } from "semantic-ui-react";
import { withState, buildUID } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";

import { i18next } from "@translations/oarepo_ui/i18next";

import { ResultsItemCreators } from "./ResultsItemCreators";
import { ResultsItemSubjects } from "./ResultsItemSubjects";

export const ResultsListItemComponent = ({
  currentQueryState,
  result,
  appName,
}) => {
  const searchAppConfig = useContext(SearchConfigurationContext);
  const accessStatusId = _get(result, "ui.access_status.id", "open");
  const accessStatus = _get(result, "metadata.accessRights.title", "Open");
  const accessStatusIcon = _get(result, "ui.access_status.icon", "unlock");
  const createdDate = _get(result, "created", "No creation date found.");
  const creators = result.metadata.creators.slice(0, 3);

  const descriptionStripped = _get(
    result,
    "metadata.abstract[0].value",
    "No description"
  );

  const publicationDate = _get(
    result,
    "metadata.dateAvailable",
    "No publication date found."
  );
  const resourceType = _get(
    result,
    "metadata.resourceType.title",
    "No resource type"
  );
  const subjects = _get(result, "metadata.subjects", []);
  const title = _get(result, "metadata.title", "No title");
  const version = _get(result, "revision_id", null);
  const versions = _get(result, "versions");

  const publishingInformation = _join(
    _get(result, "metadata.publishers", []),
    ","
  );

  console.log(subjects);
  const filters =
    currentQueryState && Object.fromEntries(currentQueryState.filters);
  const allVersionsVisible = filters?.allversions;
  const numOtherVersions = version - 1;

  const viewLink = new URL(
    result.links.self,
    new URL(searchAppConfig.ui_endpoint, window.location.origin)
  );
  return (
    <Overridable
      id={buildUID("RecordsResultsListItem.layout", "", appName)}
      result={result}
      accessStatusId={accessStatusId}
      accessStatus={accessStatus}
      accessStatusIcon={accessStatusIcon}
      createdDate={createdDate}
      creators={creators}
      descriptionStripped={descriptionStripped}
      publicationDate={publicationDate}
      resourceType={resourceType}
      subjects={subjects}
      title={title}
      version={version}
      versions={versions}
      allVersionsVisible={allVersionsVisible}
      numOtherVersions={numOtherVersions}
    >
      <Item key={result.id}>
        <Item.Content>
          <Item.Extra className="labels-actions">
            <Label size="tiny" className="primary">
              {publicationDate} (v{version})
            </Label>
            <Label size="tiny" className="neutral">
              {resourceType}
            </Label>
            <Label size="tiny" className={`access-status ${accessStatusId}`}>
              {accessStatusIcon && <Icon name={accessStatusIcon} />}
              {accessStatus}
            </Label>
          </Item.Extra>
          <Item.Header as="h2">
            <a href={viewLink}>{title}</a>
          </Item.Header>
          <Item className="creatibutors">
            <ResultsItemCreators creators={creators} />
          </Item>
          <Item.Description>
            {_truncate(descriptionStripped, { length: 350 })}
          </Item.Description>
          <Item.Extra>
            <ResultsItemSubjects subjects={subjects} />
            <div>
              <small>
                <p>
                  {createdDate && (
                    <>
                      {i18next.t("Uploaded on")} <span>{createdDate}</span>
                    </>
                  )}
                  {createdDate && publishingInformation && " | "}
                  {publishingInformation && (
                    <>
                      {i18next.t("Published in: ")}{" "}
                      <span>{publishingInformation}</span>
                    </>
                  )}
                </p>
              </small>
            </div>
            {!allVersionsVisible && version > 1 && (
              <p>
                <small>
                  <b>
                    {numOtherVersions} more{" "}
                    {numOtherVersions > 1 ? "versions" : "version"} exist for
                    this record
                  </b>
                </small>
              </p>
            )}
          </Item.Extra>
        </Item.Content>
      </Item>
    </Overridable>
  );
};

ResultsListItemComponent.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

ResultsListItemComponent.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const ResultsListItem = (props) => {
  return (
    <Overridable id={buildUID("ResultsListItem", "", props.appName)} {...props}>
      <ResultsListItemComponent {...props} />
    </Overridable>
  );
};

ResultsListItem.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

ResultsListItem.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const ResultsListItemWithState = withState(
  ({ currentQueryState, result, appName }) => (
    <ResultsListItem
      currentQueryState={currentQueryState}
      result={result}
      appName={appName}
    />
  )
);

ResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

ResultsListItemWithState.defaultProps = {
  currentQueryState: null,
};

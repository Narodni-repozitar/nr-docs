import React, { useContext } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import _get from "lodash/get";
import _join from "lodash/join";
import _truncate from "lodash/truncate";
import { Grid, Item, Label, List, Icon } from "semantic-ui-react";
import { withState, buildUID } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/i18next";
import {
  ResultsItemAccessStatus,
  ResultsItemSubjects,
  ResultsItemCreatibutors,
  ResultsItemLicense,
  DoubleSeparator,
  ResultsItemResourceType,
} from "@nr/search";
import { getValueFromMultilingualArray } from "@js/oarepo_ui";
import sanitizeHtml from "sanitize-html";

const ItemHeader = ({ title, searchUrl, selfLink }) => {
  const viewLink = new URL(
    selfLink,
    new URL(searchUrl, window.location.origin)
  );
  return (
    <Item.Header as="h2">
      <a href={viewLink} dangerouslySetInnerHTML={{ __html: title }}></a>
    </Item.Header>
  );
};

ItemHeader.propTypes = {
  title: PropTypes.string.isRequired,
  searchUrl: PropTypes.string.isRequired,
  selfLink: PropTypes.string.isRequired,
};

const ItemSubheader = ({
  creators,
  contributors,
  publicationDate,
  languages,
  resourceType,
  thesis,
  subjects,
  searchUrl,
}) => {
  const isThesisDefended = thesis?.dateDefended;

  return (
    <Item.Meta>
      <Grid columns={1}>
        <Grid.Column>
          <Grid.Row className="ui double separated creatibutors">
            <ResultsItemCreatibutors
              creators={creators}
              contributors={contributors}
              searchUrl={searchUrl}
            />
          </Grid.Row>
          <Grid.Row className="ui separated">
            <span
              aria-label={i18next.t("Publication date")}
              title={i18next.t("Publication date")}
            >
              {publicationDate}
            </span>
            {languages.length > 0 && <DoubleSeparator />}
            <span
              aria-label={i18next.t("Languages")}
              title={i18next.t("Languages")}
            >
              {_join(
                languages.map((l) => l.title),
                ", "
              )}
            </span>
          </Grid.Row>
          <Grid.Row>
            <ResultsItemResourceType
              searchUrl={searchUrl}
              resourceType={resourceType}
            />
            {thesis && (
              <Label pointing="left" size="mini" basic>
                <Icon
                  name={isThesisDefended ? "check circle" : "remove circle"}
                  color={isThesisDefended ? "green" : "red"}
                />{" "}
                {isThesisDefended
                  ? i18next.t("defended")
                  : i18next.t("not defended")}
              </Label>
            )}
          </Grid.Row>
          <Grid.Row>
            <ResultsItemSubjects searchUrl={searchUrl} subjects={subjects} />
          </Grid.Row>
        </Grid.Column>
      </Grid>
    </Item.Meta>
  );
};

ItemSubheader.propTypes = {
  creators: PropTypes.array,
  contributors: PropTypes.array,
  publicationDate: PropTypes.string,
  languages: PropTypes.array,
  resourceType: PropTypes.object,
  thesis: PropTypes.object,
  subjects: PropTypes.array,
  searchUrl: PropTypes.string,
};

const ItemExtraInfo = ({ createdDate, publishers, version }) => {
  return (
    <Item.Extra>
      <div>
        <small>
          <p>
            {createdDate && (
              <>
                {i18next.t("Uploaded on")} <span>{createdDate}</span>{" "}
                {version && `(${i18next.t("version")}: ${String(version)})`}
              </>
            )}
            {createdDate && publishers.length > 0 && " | "}
            {publishers.length > 0 && (
              <>
                {i18next.t("Published in: ")}{" "}
                <span>{_join(publishers, ", ")}</span>
              </>
            )}
          </p>
        </small>
      </div>
    </Item.Extra>
  );
};

ItemExtraInfo.propTypes = {
  createdDate: PropTypes.string,
  publishers: PropTypes.array,
  version: PropTypes.string,
};

const ItemSidebarIcons = ({ accessStatus, rights }) => {
  return (
    <Item.Extra className="labels-actions">
      <List>
        {accessStatus && (
          <List.Item>
            <ResultsItemAccessStatus status={accessStatus} />
          </List.Item>
        )}
        {rights && (
          <List.Item>
            <ResultsItemLicense rights={rights} />
          </List.Item>
        )}
      </List>
    </Item.Extra>
  );
};

ItemSidebarIcons.propTypes = {
  accessStatus: PropTypes.object,
  rights: PropTypes.object,
};

export const ResultsListItemComponent = ({
  currentQueryState,
  result,
  appName,
  ...rest
}) => {
  const searchAppConfig = useContext(SearchConfigurationContext);

  const { allowedHtmlTags } = searchAppConfig;
  const accessRights = _get(result, "access_status", null);
  const createdDate = _get(result, "created", "No creation date found.");
  const creators = result.metadata?.creators;
  const contributors = _get(result, "metadata.contributors", []);

  const rights = _get(result, "metadata.rights");

  const abstract = _get(result, "metadata.abstract", null);

  const languages = _get(result, "metadata.languages", []);

  const publicationDate = _get(
    result,
    "metadata.dateIssued",
    i18next.t("No publication date found.")
  );
  const resourceType = _get(result, "metadata.resourceType");

  const subjects = _get(result, "metadata.subjects", []);

  const additionalTitles = _get(result, "metadata.additionalTitles", []);

  const translatedTitle = additionalTitles.find(
    (title) =>
      title?.titleType === "translatedTitle" &&
      title?.title?.lang === i18next.language
  )?.title?.value;

  const title = sanitizeHtml(
    translatedTitle ?? _get(result, "metadata.title", i18next.t("No title")),
    {
      allowedTags: allowedHtmlTags,
      allowedAttributes: {},
    }
  );

  const version = _get(result, "metadata.version", null);

  const thesis = _get(result, "metadata.thesis");
  const publishers = _get(result, "metadata.publishers", []);

  const filters =
    currentQueryState && Object.fromEntries(currentQueryState.filters);
  const allVersionsVisible = filters?.allversions;

  return (
    <Overridable
      id={buildUID("RecordsResultsListItem.layout", "", appName)}
      result={result}
      accessStatus={accessRights}
      createdDate={createdDate}
      creators={creators}
      abstract={abstract}
      publicationDate={publicationDate}
      publishers={publishers}
      resourceType={resourceType}
      subjects={subjects}
      languages={languages}
      title={title}
      version={version}
      rights={rights}
      thesis={thesis}
      allVersionsVisible={allVersionsVisible}
    >
      <Item key={result.id} data-testid="result-item">
        <Item.Content>
          <Grid>
            <Grid.Row columns={2}>
              <Grid.Column className="results-list item-side computer tablet only">
                <ItemSidebarIcons rights={rights} accessStatus={accessRights} />
              </Grid.Column>
              <Grid.Column className="results-list item-main">
                <div className="justify-space-between flex">
                  <ItemHeader
                    title={title}
                    searchUrl={searchAppConfig.ui_endpoint}
                    selfLink={result.links.self_html}
                  />
                  <div className="item-access-rights">
                    <Label title={result.state_timestamp}>{result.state}</Label>
                    {accessRights && accessRights.id !== "open" && (
                      <Label title={`${accessRights.description_l10n}`}>
                        {accessRights.title_l10n}
                      </Label>
                    )}
                  </div>
                </div>
                <ItemSubheader
                  creators={creators}
                  contributors={contributors}
                  publicationDate={publicationDate}
                  languages={languages}
                  resourceType={resourceType}
                  thesis={thesis}
                  subjects={subjects}
                  searchUrl={searchAppConfig.ui_endpoint}
                />
                {abstract && abstract.length > 0 && (
                  <Item.Description
                    dangerouslySetInnerHTML={{
                      __html: _truncate(
                        sanitizeHtml(getValueFromMultilingualArray(abstract), {
                          allowedTags: allowedHtmlTags,
                          allowedAttributes: {},
                        }),
                        {
                          length: 350,
                        }
                      ),
                    }}
                  />
                )}
                <ItemExtraInfo
                  createdDate={createdDate}
                  publishers={publishers}
                  version={version}
                />
              </Grid.Column>
            </Grid.Row>
          </Grid>
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

const ResultsListItemWithState = withState(
  ({ currentQueryState, updateQueryState, result, appName }) => (
    <ResultsListItem
      currentQueryState={currentQueryState}
      updateQueryState={updateQueryState}
      result={result}
      appName={appName}
    />
  )
);

export default ResultsListItemWithState;

ResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

ResultsListItemWithState.defaultProps = {
  currentQueryState: null,
};

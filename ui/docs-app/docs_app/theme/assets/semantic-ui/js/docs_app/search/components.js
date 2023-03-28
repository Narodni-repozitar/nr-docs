import {
  SearchBar,
  MultipleOptionsSearchBarRSK,
} from '@js/invenio_search_ui/components'
import _get from 'lodash/get'
import _join from 'lodash/join'
import _truncate from 'lodash/truncate'
import React, { Component } from 'react'
import Overridable from 'react-overridable'
import { withState, buildUID } from 'react-searchkit'
import {
  Button,
  Card,
  Checkbox,
  Grid,
  Header,
  Icon,
  Input,
  Item,
  Label,
  Message,
  Segment,
} from 'semantic-ui-react'
import PropTypes from 'prop-types'

// TODO: implement actual translations
const i18next = {
  t: (value) => value,
}

export function SearchItemCreators({ creators, className }) {
  let spanClass = 'creatibutor-wrap separated'
  className && (spanClass += ` ${className}`)

  function makeIcon(scheme, identifier, name) {
    let link = null
    let linkTitle = null
    let icon = null
    let alt = ''

    switch (scheme) {
      case 'orcid':
        link = `https://orcid.org/${identifier}`
        linkTitle = i18next.t('ORCID profile')
        icon = '/static/images/orcid.svg'
        alt = 'ORCID logo'
        break
      case 'ror':
        link = `https://ror.org/${identifier}`
        linkTitle = i18next.t('ROR profile')
        icon = '/static/images/ror-icon.svg'
        alt = 'ROR logo'
        break
      case 'gnd':
        link = `https://d-nb.info/gnd/${identifier}`
        linkTitle = i18next.t('GND profile')
        icon = '/static/images/gnd-icon.svg'
        alt = 'GND logo'
        break
      default:
        return null
    }

    icon = (
      <a
        className="no-text-decoration mr-0"
        href={link}
        aria-label={`${name}: ${linkTitle}`}
        title={`${name}: ${linkTitle}`}
        key={scheme}
      >
        <img className="inline-id-icon ml-5" src={icon} alt={alt} />
      </a>
    )
    return icon
  }

  function getIcons(creator) {
    let ids = _get(creator, 'person_or_org.identifiers', [])
    let creatorName = _get(creator, 'person_or_org.name', 'No name')
    let icons = ids.map((c) => makeIcon(c.scheme, c.identifier, creatorName))
    return icons
  }

  function getLink(creator) {
    let creatorName = _get(creator, 'fullName', 'No name')
    let link = (
      <a
        className="creatibutor-link"
        href={`/search?q=metadata.creators.person_or_org.name:"${creatorName}"`}
        title={`${creatorName}: ${i18next.t('Search')}`}
      >
        <span className="creatibutor-name">{creatorName}</span>
      </a>
    )
    return link
  }
  return creators.map((creator) => (
    <span className={spanClass} key={creator.fullName}>
      {getLink(creator)}
      {getIcons(creator)}
    </span>
  ))
}

class RecordsResultsListItemComponent extends Component {
  render() {
    const { currentQueryState, result, key, appName } = this.props

    const accessStatusId = _get(result, 'ui.access_status.id', 'open')
    const accessStatus = _get(result, 'metadata.accessRights.title', 'Open')
    const accessStatusIcon = _get(result, 'ui.access_status.icon', 'unlock')
    const createdDate = _get(result, 'created', 'No creation date found.')
    const creators = result.metadata.creators.slice(0, 3)

    const descriptionStripped = _get(
      result,
      'metadata.abstract[0].value',
      'No description',
    )

    const publicationDate = _get(
      result,
      'metadata.dateAvailable',
      'No publication date found.',
    )
    const resourceType = _get(
      result,
      'metadata.resourceType.title',
      'No resource type',
    )
    const subjects = _get(result, 'metadata.subjects', [])
    const title = _get(result, 'metadata.title', 'No title')
    const version = _get(result, 'revision_id', null)
    const versions = _get(result, 'versions')

    const publishingInformation = _join(
      _get(result, 'metadata.publishers', []),
      ',',
    )

    const filters =
      currentQueryState && Object.fromEntries(currentQueryState.filters)
    const allVersionsVisible = filters?.allversions
    const numOtherVersions = version - 1

    // Derivatives
    const viewLink = `/docs/${result.links.self}`
    return (
      <Overridable
        id={buildUID('RecordsResultsListItem.layout', '', appName)}
        result={result}
        key={key}
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
        <Item key={key ?? result.id}>
          <Item.Content>
            <Item.Extra className="labels-actions">
              <Label size="tiny" className="primary">
                {publicationDate} ({version})
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
              <SearchItemCreators creators={creators} />
            </Item>
            <Item.Description>
              {_truncate(descriptionStripped, { length: 350 })}
            </Item.Description>
            <Item.Extra>
              {subjects.map((subject) => (
                <Label key={subject.subject} size="tiny">
                  {subject.subject}
                </Label>
              ))}
              <div>
                <small>
                  <p>
                    {createdDate && (
                      <>
                        {i18next.t('Uploaded on')} <span>{createdDate}</span>
                      </>
                    )}
                    {createdDate && publishingInformation && ' | '}
                    {publishingInformation && (
                      <>
                        {i18next.t('Published in: ')}{' '}
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
                      {numOtherVersions} more{' '}
                      {numOtherVersions > 1 ? 'versions' : 'version'} exist for
                      this record
                    </b>
                  </small>
                </p>
              )}
            </Item.Extra>
          </Item.Content>
        </Item>
      </Overridable>
    )
  }
}

RecordsResultsListItemComponent.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  key: PropTypes.string,
  appName: PropTypes.string,
}

RecordsResultsListItemComponent.defaultProps = {
  key: null,
  currentQueryState: null,
  appName: '',
}

export const RecordsResultsListItem = Overridable.component(
  'RecordsResultsListItem',
  RecordsResultsListItemComponent,
)

export const RDMRecordResultsListItemWithState = withState(
  ({ currentQueryState, result, appName }) => (
    <RecordsResultsListItem
      currentQueryState={currentQueryState}
      result={result}
      appName={appName}
    />
  ),
)

RDMRecordResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
}

RDMRecordResultsListItemWithState.defaultProps = {
  currentQueryState: null,
}

// TODO: Update this according to the full List item template?
export const RDMRecordResultsGridItem = ({ result }) => {
  const descriptionStripped = _get(
    result,
    'ui.description_stripped',
    'No description',
  )
  return (
    <Card fluid href={`/records/${result.pid}`}>
      <Card.Content>
        <Card.Header>{result.metadata.title}</Card.Header>
        <Card.Description>
          {_truncate(descriptionStripped, { length: 200 })}
        </Card.Description>
      </Card.Content>
    </Card>
  )
}

RDMRecordResultsGridItem.propTypes = {
  result: PropTypes.object.isRequired,
}

export const RDMRecordSearchBarContainer = ({ appName }) => {
  return (
    <Overridable id={buildUID('SearchApp.searchbar', '', appName)}>
      <SearchBar />
    </Overridable>
  )
}

RDMRecordSearchBarContainer.propTypes = {
  appName: PropTypes.string.isRequired,
}

export const RDMRecordMultipleSearchBarElement = ({
  queryString,
  onInputChange,
}) => {
  const headerSearchbar = document.getElementById('header-search-bar')
  const searchbarOptions = JSON.parse(headerSearchbar.dataset.options)

  return (
    <MultipleOptionsSearchBarRSK
      options={searchbarOptions}
      onInputChange={onInputChange}
      queryString={queryString}
      placeholder={i18next.t('Search records...')}
    />
  )
}

RDMRecordMultipleSearchBarElement.propTypes = {
  queryString: PropTypes.string.isRequired,
  onInputChange: PropTypes.func.isRequired,
}

export const RDMRecordSearchBarElement = withState(
  ({
    placeholder: passedPlaceholder,
    queryString,
    onInputChange,
    updateQueryState,
    currentQueryState,
  }) => {
    const placeholder = passedPlaceholder || i18next.t('Search')

    const onSearch = () => {
      updateQueryState({ ...currentQueryState, queryString })
    }

    const onBtnSearchClick = () => {
      onSearch()
    }
    const onKeyPress = (event) => {
      if (event.key === 'Enter') {
        onSearch()
      }
    }
    return (
      <Input
        action={{
          icon: 'search',
          onClick: onBtnSearchClick,
          className: 'search',
          'aria-label': 'Search',
        }}
        fluid
        placeholder={placeholder}
        onChange={(event, { value }) => {
          onInputChange(value)
        }}
        value={queryString}
        onKeyPress={onKeyPress}
      />
    )
  },
)

export const RDMToggleComponent = ({
  updateQueryFilters,
  userSelectionFilters,
  filterValue,
  label,
  title,
}) => {
  const _isChecked = (userSelectionFilters) => {
    const isFilterActive =
      userSelectionFilters.filter((filter) => filter[0] === filterValue[0])
        .length > 0
    return isFilterActive
  }

  const onToggleClicked = () => {
    updateQueryFilters(filterValue)
  }

  var isChecked = _isChecked(userSelectionFilters)
  return (
    <Card className="borderless facet">
      <Card.Content>
        <Card.Header as="h2">{title}</Card.Header>
      </Card.Content>
      <Card.Content>
        <Checkbox
          toggle
          label={label}
          name="versions-toggle"
          id="versions-toggle"
          onClick={onToggleClicked}
          checked={isChecked}
        />
      </Card.Content>
    </Card>
  )
}

RDMToggleComponent.propTypes = {
  title: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  filterValue: PropTypes.array.isRequired,
  userSelectionFilters: PropTypes.array.isRequired,
  updateQueryFilters: PropTypes.func.isRequired,
}

export const RDMCountComponent = ({ totalResults }) => {
  return <Label>{totalResults.toLocaleString('en-US')}</Label>
}

RDMCountComponent.propTypes = {
  totalResults: PropTypes.number.isRequired,
}

export const RDMEmptyResults = ({ queryString, searchPath, resetQuery }) => {
  return (
    <Grid>
      <Grid.Row centered>
        <Grid.Column width={12} textAlign="center">
          <Header as="h2">
            {i18next.t("We couldn't find any matches for ")}
            {(queryString && `'${queryString}'`) || i18next.t('your search')}
          </Header>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row centered>
        <Grid.Column width={8} textAlign="center">
          <Button primary onClick={resetQuery}>
            <Icon name="search" />
            {i18next.t('Start over')}
          </Button>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row centered>
        <Grid.Column width={12}>
          <Segment secondary padded size="large">
            <Header as="h3" size="small">
              {i18next.t('ProTip')}!
            </Header>
            <p>
              <a
                href={`${searchPath}?q=metadata.publication_date:[2017-01-01 TO *]`}
              >
                metadata.publication_date:[2017-01-01 TO *]
              </a>{' '}
              {i18next.t(
                'will give you all the publications from 2017 until today.',
              )}
            </p>
            <p>
              {i18next.t('For more tips, check out our ')}
              <a href="/help/search" title={i18next.t('Search guide')}>
                {i18next.t('search guide')}
              </a>
              {i18next.t(' for defining advanced search queries.')}
            </p>
          </Segment>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  )
}

RDMEmptyResults.propTypes = {
  queryString: PropTypes.string.isRequired,
  resetQuery: PropTypes.func.isRequired,
  searchPath: PropTypes.string,
}

RDMEmptyResults.defaultProps = {
  searchPath: '/search',
}

export const RDMErrorComponent = ({ error }) => {
  return (
    <Message error content={error.response.data.message} icon="warning sign" />
  )
}

RDMErrorComponent.propTypes = {
  error: PropTypes.object.isRequired,
}

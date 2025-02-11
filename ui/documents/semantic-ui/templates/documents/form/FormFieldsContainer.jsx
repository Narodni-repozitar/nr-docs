import {
  useFormConfig,
  MultilingualTextInput,
  FormikStateLogger,
  EDTFSingleDatePicker,
  useFieldData,
  useSanitizeInput,
  useDepositApiClient,
} from "@js/oarepo_ui";
import { CommunitySelector } from "@js/communities_components/CommunitySelector/CommunitySelector";
import {
  LocalVocabularySelectField,
  VocabularyTreeSelectField,
} from "@js/oarepo_vocabularies";
import { TextField } from "react-invenio-forms";
import {
  StringArrayField,
  AdditionalTitlesField,
  FundersField,
  ExternalLocationField,
  SubjectsField,
  SeriesField,
  EventsField,
  IdentifiersField,
  CreatibutorsField,
  RelatedItemsField,
  objectIdentifiersSchema,
  FileUploader,
  LicenseField,
} from "@nr/forms";
import Overridable from "react-overridable";
import { i18next } from "@translations/i18next";
import _has from "lodash/has";
import { useFormikContext, getIn } from "formik";

import React, { Component, useState } from "react";
import PropTypes from "prop-types";
import { Field, FastField } from "formik";
import { Accordion, Container, Icon, Grid } from "semantic-ui-react";
import _omit from "lodash/omit";
import _get from "lodash/get";

// Define the accordion data
const accordionData = [
  {
    name: "Basic information",
    includesPaths: [
      "metadata.title",
      "metadata.additionalTitles",
      "metadata.resourceType",
      "metadata.objectIdentifiers",
      "metadata.languages",
      "metadata.dateIssued",
      "metadata.publishers",
      "metadata.accessRights",
      "metadata.rights",
      "metadata.dateModified",
    ],
  },
  {
    name: "Creators",
    includesPaths: ["metadata.creators", "metadata.contributors"],
  },
  {
    name: "Document description",
    includesPaths: [
      "metadata.subjects",
      "metadata.subjectCategories",
      "metadata.abstract",
      "metadata.series",
      "metadata.externalLocation",
      "metadata.notes",
    ],
  },
  {
    name: "Financing information",
    includesPaths: ["metadata.fundingReferences"],
  },
  {
    name: "Related items",
    includesPaths: ["metadata.relatedItems"],
  },
  {
    name: "Events",
    includesPaths: ["metadata.events"],
  },
  {
    name: "Files upload",
    includesPaths: ["files.enabled"],
  },
];

// New Accordion Control Panel Component
const AccordionControlPanel = ({ activeAccordion, setActiveAccordion }) => {
  const { partialSave } = useDepositApiClient();

  const saveAndSetActiveAccordion = async (title) => {
    const response = await partialSave({
      includedErrorPaths: accordionData.find(
        (acc) => acc.name === activeAccordion
      ).includesPaths,
    });
    if (!response) return;
    setActiveAccordion(title);
  };

  return (
    <div>
      <h3>Accordion Control</h3>
      {accordionData.map((accordion) => (
        <div>
          <button
            key={accordion.name}
            onClick={() => saveAndSetActiveAccordion(accordion.name)}
            style={{
              marginRight: "10px",
              padding: "5px 10px",
              backgroundColor:
                activeAccordion === accordion.name ? "lightblue" : "white",
              border: "1px solid gray",
              cursor: "pointer",
            }}
          >
            {accordion.name}
          </button>
        </div>
      ))}
    </div>
  );
};

const FormFieldsContainer = () => {
  const { formConfig, files: recordFiles } = useFormConfig();
  const editMode = _has(formConfig, "updateUrl");

  const submissibleResourceTypes = React.useCallback(
    (options) =>
      options.filter(
        (opt) => !!opt.props?.submission && opt.props?.submission !== "false"
      ),
    []
  );
  const { getFieldData } = useFieldData();

  const { label: subjectCategoriesLabel } = React.useMemo(
    () =>
      getFieldData({
        fieldPath: "metadata.subjectCategories",
        icon: "tag",
      }),
    []
  );

  const { values, setFieldValue, setFieldTouched } = useFormikContext();
  const { sanitizeInput } = useSanitizeInput();

  // State for controlling active accordion
  const [activeAccordion, setActiveAccordion] =
    React.useState("Basic information");

  return (
    <Grid>
      <Grid.Column width={4}>
        <AccordionControlPanel
          activeAccordion={activeAccordion}
          setActiveAccordion={setActiveAccordion}
        />
      </Grid.Column>
      <Grid.Column width={12}>
        <Overridable id="NrDocs.Deposit.CommunitySelector.container">
          <CommunitySelector />
        </Overridable>
        {accordionData.map((accordion) => {
          const { name, includesPaths } = accordion;
          return (
            <Overridable
              key={name}
              id={`NrDocs.Deposit.AccordionField${name.replace(
                / /g,
                ""
              )}.container`}
            >
              <AccordionField
                includesPaths={includesPaths}
                active={activeAccordion === name}
                label={i18next.t(name)}
              >
                {name === "Basic information" && (
                  <>
                    <Overridable
                      id="NrDocs.Deposit.TitleField.container"
                      fieldPath="metadata.title"
                    >
                      <TextField
                        optimized
                        fieldPath="metadata.title"
                        {...getFieldData({ fieldPath: "metadata.title" })}
                        onBlur={() => {
                          const cleanedContent = sanitizeInput(
                            getIn(values, "metadata.title")
                          );
                          setFieldValue("metadata.title", cleanedContent);
                          setFieldTouched("metadata.title", true);
                        }}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.AdditionalTitlesField.container"
                      fieldPath="metadata.additionalTitles"
                    >
                      <AdditionalTitlesField fieldPath="metadata.additionalTitles" />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.ResourceTypeField.container"
                      fieldPath="metadata.resourceType"
                    >
                      <LocalVocabularySelectField
                        optimized
                        fieldPath="metadata.resourceType"
                        multiple={false}
                        filterFunction={submissibleResourceTypes}
                        clearable
                        optionsListName="resource-types"
                        {...getFieldData({
                          fieldPath: "metadata.resourceType",
                          icon: "tag",
                        })}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.ObjectIdentifiersField.container"
                      fieldPath="metadata.objectIdentifiers"
                    >
                      <IdentifiersField
                        options={objectIdentifiersSchema}
                        fieldPath="metadata.objectIdentifiers"
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.LanguagesField.container"
                      fieldPath="metadata.languages"
                    >
                      <LocalVocabularySelectField
                        optimized
                        fieldPath="metadata.languages"
                        multiple={true}
                        clearable
                        optionsListName="languages"
                        {...getFieldData({
                          fieldPath: "metadata.languages",
                          icon: "language",
                        })}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.DateIssuedField.container"
                      fieldPath="metadata.dateIssued"
                    >
                      <EDTFSingleDatePicker
                        fieldPath="metadata.dateIssued"
                        {...getFieldData({
                          fieldPath: "metadata.dateIssued",
                          icon: "calendar",
                        })}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.PublishersField.container"
                      fieldPath="metadata.publishers"
                    >
                      <StringArrayField
                        fieldPath="metadata.publishers"
                        addButtonLabel={i18next.t("Add publisher")}
                        {...getFieldData({ fieldPath: "metadata.publishers" })}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.AccessRightsField.container"
                      fieldPath="metadata.accessRights"
                    >
                      <LocalVocabularySelectField
                        optimized
                        fieldPath="metadata.accessRights"
                        clearable
                        optionsListName="access-rights"
                        {...getFieldData({
                          fieldPath: "metadata.accessRights",
                          icon: "tag",
                        })}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.LicenseField.container"
                      fieldPath="metadata.rights"
                    >
                      <LicenseField
                        searchConfig={{
                          searchApi: {
                            axios: {
                              headers: {
                                Accept: "application/vnd.inveniordm.v1+json",
                              },
                              url: "/api/vocabularies/rights",
                            },
                          },
                          initialQueryState: {
                            size: 25,
                            page: 1,
                            sortBy: "bestmatch",
                            filters: [["tags", ""]],
                          },
                        }}
                        fieldPath="metadata.rights"
                        {...getFieldData({
                          fieldPath: "metadata.rights",
                          icon: "drivers license",
                        })}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.DateModifiedField.container"
                      fieldPath="metadata.dateModified"
                    >
                      {editMode && (
                        <EDTFSingleDatePicker
                          fieldPath="metadata.dateModified"
                          {...getFieldData({
                            fieldPath: "metadata.dateModified",
                            icon: "calendar",
                          })}
                        />
                      )}
                    </Overridable>
                  </>
                )}
                {name === "Creators" && (
                  <>
                    <Overridable
                      id="NrDocs.Deposit.CreatorsField.container"
                      fieldPath="metadata.creators"
                    >
                      <CreatibutorsField
                        fieldPath="metadata.creators"
                        schema="creators"
                        autocompleteNames="off"
                        fieldPathPrefix="metadata.creators.0"
                        {...getFieldData({
                          fieldPath: "metadata.creators",
                          icon: "user",
                        })}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.ContributorsField.container"
                      fieldPath="metadata.contributors"
                    >
                      <CreatibutorsField
                        addButtonLabel={i18next.t("Add contributor")}
                        modal={{
                          addLabel: i18next.t("Add contributor"),
                          editLabel: i18next.t("Edit contributor"), // Removed the extra } here
                        }}
                        fieldPath="metadata.contributors"
                        schema="contributors"
                        autocompleteNames="off"
                        nameTypeHelpText={i18next.t(
                          "Choose if the contributor is a person or an organization."
                        )}
                        fieldPathPrefix="metadata.contributors.0"
                        {...getFieldData({
                          fieldPath: "metadata.contributors",
                          icon: "user",
                        })}
                      />
                    </Overridable>
                  </>
                )}
                {name === "Document description" && (
                  <>
                    <Overridable
                      id="NrDocs.Deposit.SubjectsField.container"
                      fieldPath="metadata.subjects"
                    >
                      <SubjectsField fieldPath="metadata.subjects" />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.SubjectCategoriesField.container"
                      fieldPath="metadata.subjectCategories"
                    >
                      <VocabularyTreeSelectField
                        fieldPath="metadata.subjectCategories"
                        multiple={true}
                        vocabulary="subject-categories"
                        label={subjectCategoriesLabel}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.AbstractField.container"
                      fieldPath="metadata.abstract"
                    >
                      <MultilingualTextInput
                        textFieldLabel={i18next.t("Description")}
                        fieldPath="metadata.abstract"
                        rich={true}
                        lngFieldWidth={4}
                        {...getFieldData({ fieldPath: "metadata.abstract" })}
                      />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.SeriesField.container"
                      fieldPath="metadata.series"
                    >
                      <SeriesField fieldPath="metadata.series" />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.ExternalLocationField.container"
                      fieldPath="metadata.externalLocation"
                    >
                      <ExternalLocationField fieldPath="metadata.externalLocation" />
                    </Overridable>
                    <Overridable
                      id="NrDocs.Deposit.NotesField.container"
                      fieldPath="metadata.notes"
                    >
                      <StringArrayField
                        fieldPath="metadata.notes"
                        {...getFieldData({ fieldPath: "metadata.notes" })}
                      />
                    </Overridable>
                  </>
                )}
                {name === "Financing information" && (
                  <>
                    <Overridable
                      id="NrDocs.Deposit.FundersField.container"
                      fieldPath="metadata.fundingReferences"
                    >
                      <FundersField fieldPath="metadata.fundingReferences" />
                    </Overridable>
                  </>
                )}
                {name === "Related items" && (
                  <>
                    <Overridable
                      id="NrDocs.Deposit.RelatedItemsField.container"
                      fieldPath="metadata.relatedItems"
                    >
                      <RelatedItemsField
                        fieldPath="metadata.relatedItems"
                        {...getFieldData({
                          fieldPath: "metadata.relatedItems",
                        })}
                      />
                    </Overridable>
                  </>
                )}
                {name === "Events" && (
                  <>
                    <Overridable
                      id="NrDocs.Deposit.EventsField.container"
                      fieldPath="metadata.events"
                    >
                      <EventsField fieldPath="metadata.events" />
                    </Overridable>
                  </>
                )}
                {name === "Files upload" && (
                  <Overridable id="NrDocs.Deposit.FileUploader.container">
                    <FileUploader recordFiles={recordFiles} />
                  </Overridable>
                )}
              </AccordionField>
            </Overridable>
          );
        })}
        {process.env.NODE_ENV === "development" && <FormikStateLogger />}
      </Grid.Column>
    </Grid>
  );
};

export default FormFieldsContainer;

export class AccordionField extends Component {
  hasError(errors, initialValues = undefined, values = undefined) {
    const { includesPaths } = this.props;
    for (const errorPath in errors) {
      for (const subPath in errors[errorPath]) {
        const path = `${errorPath}.${subPath}`;
        if (
          _get(initialValues, path, "") === _get(values, path, "") &&
          includesPaths.includes(`${errorPath}.${subPath}`)
        )
          return true;
      }
    }
    return false;
  }

  renderAccordion = (props) => {
    const {
      form: { errors, status, initialErrors, initialValues, values },
    } = props;

    // eslint-disable-next-line no-unused-vars
    const { label, children, active, ...ui } = this.props;
    const uiProps = _omit({ ...ui }, ["optimized", "includesPaths"]);
    const hasError = status
      ? this.hasError(status)
      : this.hasError(errors) ||
        this.hasError(initialErrors, initialValues, values);
    const panels = [
      {
        key: `panel-${label}`,
        title: {
          content: label,
        },
        content: {
          content: <Container>{children}</Container>,
        },
      },
    ];

    const errorClass = hasError ? "error secondary" : "";
    const [activeIndex, setActiveIndex] = useState(active ? 0 : -1);

    const handleTitleClick = (e, { index }) => {
      setActiveIndex(activeIndex === index ? -1 : index);
    };

    return (
      <Accordion
        inverted
        className={`invenio-accordion-field ${errorClass}`}
        {...uiProps}
      >
        {panels.map((panel, index) => (
          <React.Fragment key={panel.key}>
            <Accordion.Title
              active={active}
              index={index}
              onClick={handleTitleClick}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  handleTitleClick(e, { index });
                }
              }}
              tabIndex={0}
            >
              {panel.title.content}
              <Icon name="angle right" />
            </Accordion.Title>
            {active && (
              <Accordion.Content active={active}>
                {panel.content.content}
              </Accordion.Content>
            )}
          </React.Fragment>
        ))}
      </Accordion>
    );
  };

  render() {
    const { optimized } = this.props;

    const FormikField = optimized ? FastField : Field;
    return <FormikField name="" component={this.renderAccordion} />;
  }
}

AccordionField.propTypes = {
  active: PropTypes.bool,
  includesPaths: PropTypes.array,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  optimized: PropTypes.bool,
  children: PropTypes.node,
  ui: PropTypes.object,
};

AccordionField.defaultProps = {
  active: true,
  includesPaths: [],
  label: "",
  optimized: false,
  children: null,
  ui: null,
};

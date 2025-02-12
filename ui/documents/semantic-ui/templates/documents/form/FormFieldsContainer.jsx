import {
  useFormConfig,
  MultilingualTextInput,
  FormikStateLogger,
  EDTFSingleDatePicker,
  useFieldData,
  useSanitizeInput,
  useDepositApiClient,
  FormFeedback,
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
import { createPortal } from "react-dom";

import React, { Component, useState } from "react";
import PropTypes from "prop-types";
import { Field, FastField } from "formik";
import {
  Accordion,
  Container,
  Icon,
  Grid,
  StepTitle,
  StepGroup,
  StepDescription,
  StepContent,
  Step,
  Sticky,
  Form,
  Button,
} from "semantic-ui-react";
import _omit from "lodash/omit";
import _get from "lodash/get";

// Define the accordion data

// New Accordion Control Panel Component
const AccordionControlPanel = ({
  activeAccordion,
  handleAccordionChange,
  accordionData,
  saveAndSetActiveAccordion,
}) => {
  return (
    <div
      style={{
        textAlign: "center",
        position: "sticky",
        top: 0,
        left: 0,
        width: "100%",
        zIndex: 1000,
        background: "white",
      }}
    >
      <StepGroup
        style={{
          width: "100%",
          textAlign: "center",
          borderLeft: "none",
          borderRight: "none",
          borderTop: "none",
        }}
      >
        {accordionData.map((accordion) => (
          <Step
            active={activeAccordion.id === accordion.id}
            key={accordion.id}
            onClick={() => saveAndSetActiveAccordion(accordion.id)}
          >
            <StepContent>
              <StepTitle>{accordion.name}</StepTitle>
            </StepContent>
          </Step>
        ))}
      </StepGroup>{" "}
    </div>
  );
};

const FormFieldsContainer = ({
  handleAccordionChange,
  accordionData,
  activeAccordion,
  formFeedbackRef,
}) => {
  const { formConfig, files: recordFiles } = useFormConfig();
  const editMode = _has(formConfig, "updateUrl");
  const formStepsDiv = document.getElementById("form-steps");
  const { partialSave } = useDepositApiClient();

  const submissibleResourceTypes = React.useCallback(
    (options) =>
      options.filter(
        (opt) => !!opt.props?.submission && opt.props?.submission !== "false"
      ),
    []
  );
  const { getFieldData } = useFieldData();

  const saveAndSetActiveAccordion = async (accordionId) => {
    const currentIndex = accordionData.findIndex(
      (accordion) => accordion.id === activeAccordion.id
    );
    const nextIndex = accordionData.findIndex(
      (accordion) => accordion.id === accordionId
    );
    if (nextIndex < currentIndex) {
      handleAccordionChange(accordionId);
      return;
    }
    const response = await partialSave({
      includedErrorPaths: accordionData.find(
        (acc) => acc.id === activeAccordion.id
      ).includesPaths,
    });
    if (!response) return;
    handleAccordionChange(accordionId);
  };

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

  return (
    <React.Fragment>
      {createPortal(
        <Sticky context={formFeedbackRef} style={{ zIndex: 1000 }}>
          <AccordionControlPanel
            activeAccordion={activeAccordion}
            handleAccordionChange={handleAccordionChange}
            accordionData={accordionData}
            saveAndSetActiveAccordion={saveAndSetActiveAccordion}
          />
          <div>
            <FormFeedback
              activeAccordion={activeAccordion}
              handleAccordionChange={handleAccordionChange}
              accordionData={accordionData}
            />
          </div>
        </Sticky>,
        formStepsDiv
      )}
      <Overridable id="NrDocs.Deposit.CommunitySelector.container">
        <CommunitySelector />
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionFieldBasicInformation.container">
        <AccordionField
          includesPaths={[
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
          ]}
          active={activeAccordion.name === "Basic information"}
          label={i18next.t("Basic information")}
        >
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
        </AccordionField>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionFieldCreatibutors.container">
        <AccordionField
          active={activeAccordion.name === "Creators"}
          includesPaths={["metadata.creators", "metadata.contributors"]}
          label={i18next.t("Creators")}
        >
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
                editLabel: i18next.t("Edit contributor"),
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
        </AccordionField>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionFieldDescription.container">
        <AccordionField
          includesPaths={[
            "metadata.subjects",
            "metadata.subjectCategories",
            "metadata.abstract",
            "metadata.series",
            "metadata.externalLocation",
            "metadata.notes",
          ]}
          active={activeAccordion.name === "Document description"}
          label={i18next.t("Document description")}
        >
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
        </AccordionField>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionFinancingInformation.container">
        <AccordionField
          includesPaths={["metadata.fundingReferences"]}
          active={activeAccordion.name === "Financing information"}
          label={i18next.t("Financing information")}
        >
          <Overridable
            id="NrDocs.Deposit.FundersField.container"
            fieldPath="metadata.fundingReferences"
          >
            <FundersField fieldPath="metadata.fundingReferences" />
          </Overridable>
        </AccordionField>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionRelatedItems.container">
        <AccordionField
          includesPaths={["metadata.relatedItems"]}
          active={activeAccordion.name === "Related items"}
          label={i18next.t("Related items")}
        >
          <Overridable
            id="NrDocs.Deposit.RelatedItemsField.container"
            fieldPath="metadata.relatedItems"
          >
            <RelatedItemsField
              fieldPath="metadata.relatedItems"
              {...getFieldData({ fieldPath: "metadata.relatedItems" })}
            />
          </Overridable>
        </AccordionField>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionEvents.container">
        <AccordionField
          includesPaths={["metadata.events"]}
          active={activeAccordion.name === "Events"}
          label={i18next.t("Events")}
        >
          <Overridable
            id="NrDocs.Deposit.EventsField.container"
            fieldPath="metadata.events"
          >
            <EventsField fieldPath="metadata.events" />
          </Overridable>
        </AccordionField>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionFieldFiles.container">
        <AccordionField
          includesPaths={["files.enabled"]}
          active={activeAccordion.name === "Files upload"}
          label={
            <label htmlFor="files.enabled">{i18next.t("Files upload")}</label>
          }
          data-testid="filesupload-button"
        >
          <Overridable id="NrDocs.Deposit.FileUploader.container">
            <FileUploader recordFiles={recordFiles} />
          </Overridable>
        </AccordionField>
      </Overridable>
      <div style={{ textAlign: "center" }} className="rel-mt-2">
        {activeAccordion.id !== accordionData[0].id && (
          <Button
            labelPosition="left"
            content={i18next.t("Back")}
            primary
            icon="arrow left"
            onClick={() => {
              saveAndSetActiveAccordion(
                accordionData[
                  accordionData.findIndex(
                    (acc) => acc.id === activeAccordion.id
                  ) - 1
                ].id
              );
            }}
          />
        )}
        {activeAccordion.id !== accordionData[accordionData.length - 1].id && (
          <Button
            primary
            content={i18next.t("Next")}
            labelPosition="right"
            icon="arrow right"
            onClick={() => {
              saveAndSetActiveAccordion(
                accordionData[
                  accordionData.findIndex(
                    (acc) => acc.id === activeAccordion.id
                  ) + 1
                ].id
              );
            }}
          />
        )}
      </div>

      {process.env.NODE_ENV === "development" && <FormikStateLogger />}
    </React.Fragment>
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
        style={{ margin: "0" }}
      >
        {panels.map((panel, index) => (
          <React.Fragment key={panel.key}>
            <Accordion.Title
              style={{ display: "none" }}
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

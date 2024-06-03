import React, { useCallback } from "react";
import {
  useFormConfig,
  MultilingualTextInput,
  FormikStateLogger,
  EDTFSingleDatePicker,
  useFieldData,
  FieldDataProvider,
  getFieldData as getFieldDataUtil,
} from "@js/oarepo_ui";
import {
  LocalVocabularySelectField,
  VocabularyTreeSelectField,
} from "@js/oarepo_vocabularies";
import { AccordionField, FieldLabel, TextField } from "react-invenio-forms";
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

const FormFieldsContainer = () => {
  const { formConfig, files: recordFiles } = useFormConfig();
  const editMode = _has(formConfig, "updateUrl");
  const filterResourceTypes = useCallback(
    (options) => options.filter((option) => option.props?.submission),
    []
  );
  const { getFieldData } = useFieldData();
  return (
    <React.Fragment>
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
          active
          label={i18next.t("Basic information")}
        >
          <Overridable
            id="NrDocs.Deposit.TitleField.container"
            fieldPath="metadata.title"
          >
            <TextField
              optimized
              fieldPath="metadata.title"
              {...getFieldData("metadata.title").fullRepresentation}
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
            <VocabularyTreeSelectField
              optimized
              fieldPath="metadata.resourceType"
              clearable
              optionsListName="resource-types"
              filterFunction={filterResourceTypes}
              {...getFieldData("metadata.resourceType", "tag")
                .fullRepresentation}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.ObjectIdentifiersField.container"
            fieldPath="metadata.objectIdentifiers"
          >
            <IdentifiersField
              options={objectIdentifiersSchema}
              fieldPath="metadata.objectIdentifiers"
              identifierLabel={i18next.t("Identifier")}
              label={i18next.t("Identifier")}
              helpText={i18next.t(
                "Choose identifier type and write the identifier. You can add more identifiers."
              )}
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
              {...getFieldData("metadata.languages", "language")
                .fullRepresentation}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.DateIssuedField.container"
            fieldPath="metadata.dateIssued"
          >
            <EDTFSingleDatePicker
              fieldPath="metadata.dateIssued"
              {...getFieldData("metadata.dateIssued", "calendar")
                .fullRepresentation}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.PublishersField.container"
            fieldPath="metadata.publishers"
          >
            <StringArrayField
              fieldPath="metadata.publishers"
              addButtonLabel={i18next.t("Add publisher")}
              {...getFieldData("metadata.publishers").fullRepresentation}
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
              {...getFieldData("metadata.accessRights", "tag")
                .fullRepresentation}
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
              {...getFieldData("metadata.rights", "drivers license")
                .fullRepresentation}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.DateModifiedField.container"
            fieldPath="metadata.dateModified"
          >
            {editMode && (
              <EDTFSingleDatePicker
                fieldPath="metadata.dateModified"
                {...getFieldData("metadata.dateModified").fullRepresentation}
              />
            )}
          </Overridable>
        </AccordionField>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionFieldCreatibutors.container">
        <AccordionField
          active
          includesPaths={["metadata.creators", "metadata.contributors"]}
          label={i18next.t("Creators")}
        >
          <FieldDataProvider fieldPathPrefix="metadata.creators.0">
            {/* TODO: make a hoc to wrap each component that needs a specific provider (with specific prefix) */}
            <Overridable
              id="NrDocs.Deposit.CreatorsField.container"
              fieldPath="metadata.creators"
            >
              <CreatibutorsField
                label={i18next.t("Authors")}
                labelIcon="user"
                fieldPath="metadata.creators"
                schema="creators"
                autocompleteNames="off"
                required
              />
            </Overridable>
          </FieldDataProvider>
          <FieldDataProvider fieldPathPrefix="metadata.contributors.0">
            <Overridable
              id="NrDocs.Deposit.ContributorsField.container"
              fieldPath="metadata.contributors"
            >
              <CreatibutorsField
                label={i18next.t("Contributors")}
                addButtonLabel={i18next.t("Add contributor")}
                modal={{
                  addLabel: i18next.t("Add contributor"),
                  editLabel: i18next.t("Edit contributor"),
                }}
                labelIcon="user"
                fieldPath="metadata.contributors"
                schema="contributors"
                autocompleteNames="off"
                nameFieldPlaceholder={i18next.t("Write contributor's name.")}
                lastNameFieldPlaceholder={i18next.t(
                  "Write contributor's last name."
                )}
                nameTypeHelpText={i18next.t(
                  "Choose if the contributor is a person or an organization."
                )}
              />
            </Overridable>
          </FieldDataProvider>
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
          active
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
              optimized
              fieldPath="metadata.subjectCategories"
              multiple={true}
              clearable
              optionsListName="subject-categories"
              {...getFieldData("metadata.subjectCategories", "tag")
                .fullRepresentation}
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
              required
              lngFieldWidth={4}
              {...getFieldData("metadata.abstract").fullRepresentation}
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
              {...getFieldData("metadata.notes").fullRepresentation}
            />
          </Overridable>
        </AccordionField>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionFinancingInformation.container">
        <AccordionField
          includesPaths={["metadata.fundingReferences"]}
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
        <FieldDataProvider fieldPathPrefix="metadata.relatedItems.0">
          <AccordionField
            includesPaths={["metadata.relatedItems"]}
            label={i18next.t("Related items")}
          >
            <Overridable
              id="NrDocs.Deposit.RelatedItemsField.container"
              fieldPath="metadata.relatedItems"
            >
              <RelatedItemsField
                fieldPath="metadata.relatedItems"
                label={
                  <FieldLabel
                    htmlFor={"metadata.relatedItems"}
                    icon="pencil"
                    label={i18next.t("Link to/from other resources")}
                  />
                }
                {...getFieldData("metadata.relatedItems")}
              />
            </Overridable>
          </AccordionField>
        </FieldDataProvider>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionEvents.container">
        <AccordionField
          includesPaths={["metadata.events"]}
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
          active
          label={
            <label htmlFor="files.enabled">{i18next.t("Files upload")}</label>
          }
        >
          <Overridable id="NrDocs.Deposit.FileUploader.container">
            <FileUploader recordFiles={recordFiles} />
          </Overridable>
        </AccordionField>
      </Overridable>
      {process.env.NODE_ENV === "development" && <FormikStateLogger />}
    </React.Fragment>
  );
};

export default FormFieldsContainer;

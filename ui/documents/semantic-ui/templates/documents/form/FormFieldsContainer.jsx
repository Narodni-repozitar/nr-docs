import React, { useCallback } from "react";
import {
  useFormConfig,
  MultilingualTextInput,
  FormikStateLogger,
  EDTFSingleDatePicker,
  sanitizeInput,
  validTags,
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
import { useFormikContext, getIn } from "formik";

const FormFieldsContainer = () => {
  const { formConfig, files: recordFiles } = useFormConfig();
  const editMode = _has(formConfig, "updateUrl");
  const filterResourceTypes = useCallback(
    (options) => options.filter((option) => option.props?.submission),
    []
  );

  const { values, setFieldValue, setFieldTouched } = useFormikContext();
  const toolBar = "bold italic | bullist numlist | outdent indent | undo redo";

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
              required
              placeholder={i18next.t("Fill in the main title of the resource.")}
              label={
                <FieldLabel
                  htmlFor={"metadata.title"}
                  icon="pencil"
                  label={i18next.t("Title")}
                />
              }
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
            <VocabularyTreeSelectField
              optimized
              fieldPath="metadata.resourceType"
              required
              clearable
              label={
                <FieldLabel
                  htmlFor={"metadata.resourceType"}
                  icon="tag"
                  label={i18next.t("Resource type")}
                />
              }
              placeholder={i18next.t("Select resource type")}
              optionsListName="resource-types"
              filterFunction={filterResourceTypes}
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
              required
              label={
                <FieldLabel
                  htmlFor={"metadata.languages"}
                  icon="language"
                  label={i18next.t("Language")}
                />
              }
              clearable
              optionsListName="languages"
              placeholder={i18next.t("Select the language(s) of the resource")}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.DateIssuedField.container"
            fieldPath="metadata.dateIssued"
          >
            <EDTFSingleDatePicker
              fieldPath="metadata.dateIssued"
              label={i18next.t("Publication date")}
              helpText={i18next.t(
                "The date can be a year, year and month or a full date."
              )}
              placeholder={i18next.t(
                "Choose the date when the document was issued."
              )}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.PublishersField.container"
            fieldPath="metadata.publishers"
          >
            <StringArrayField
              fieldPath="metadata.publishers"
              addButtonLabel={i18next.t("Add publisher")}
              label={i18next.t("Publishers")}
              helpText={i18next.t(
                "Write the name of the publisher. You can write more publishers"
              )}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.AccessRightsField.container"
            fieldPath="metadata.accessRights"
          >
            <LocalVocabularySelectField
              optimized
              fieldPath="metadata.accessRights"
              required
              clearable
              label={
                <FieldLabel
                  htmlFor={"metadata.accessRights"}
                  icon="tag"
                  label={i18next.t("Access rights")}
                />
              }
              optionsListName="access-rights"
              placeholder={i18next.t(
                "Choose access type - if the resource is open or has some restrictions."
              )}
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
              label={i18next.t("Licenses")}
              labelIcon="drivers license"
              helpText={i18next.t(
                "If a Creative Commons license is associated with the resource, select the appropriate license option from the menu. We recommend choosing the latest versions, namely 3.0 Czech and 4.0 International."
              )}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.DateModifiedField.container"
            fieldPath="metadata.dateModified"
          >
            {editMode && (
              <EDTFSingleDatePicker
                fieldPath="metadata.dateModified"
                label={i18next.t("Date modified")}
                helpText=""
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
              label={
                <FieldLabel
                  htmlFor={"metadata.subjectCategories"}
                  icon="tag"
                  label={i18next.t("Subject Categories")}
                />
              }
              clearable
              optionsListName="subject-categories"
              placeholder={i18next.t("Select the discipline.")}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.AbstractField.container"
            fieldPath="metadata.abstract"
          >
            <MultilingualTextInput
              labelIcon="pencil"
              label={i18next.t("Abstract")}
              textFieldLabel={i18next.t("Description")}
              fieldPath="metadata.abstract"
              rich={true}
              editorConfig={{
                toolbar: toolBar,
                valid_elements: validTags,
              }}
              required
              helpText={i18next.t(
                "Choose abstract language and write down the text.Abstract can be provided in multiple languages."
              )}
              lngFieldWidth={4}
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
              label={i18next.t("Notes")}
              fieldPath="metadata.notes"
              helpText={i18next.t(
                "Space for additional information related to the resource."
              )}
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
            />
          </Overridable>
        </AccordionField>
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
          data-testid="filesupload-button"
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

import * as React from "react";
import {
  useFormConfig,
  MultilingualTextInput,
  FormikStateLogger,
  EDTFSingleDatePicker,
  useFieldData,
  FilesField,
  StringArrayField,
  TextField,
  IdentifiersField,
} from "@js/oarepo_ui/forms";
import { CommunitySelector } from "@js/communities_components/CommunitySelector/CommunitySelector";
import {
  LocalVocabularySelectField,
  VocabularyTreeSelectField,
} from "@js/oarepo_vocabularies";
import { AccordionField } from "react-invenio-forms";
import {
  AdditionalTitlesField,
  FundersField,
  ExternalLocationField,
  SubjectsField,
  SeriesField,
  EventsField,
  CreatibutorsField,
  RelatedItemsField,
  objectIdentifiersSchema,
  LicenseField,
} from "@nr/forms";
import Overridable from "react-overridable";
import { i18next } from "@translations/i18next";
import _has from "lodash/has";

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

  return (
    <React.Fragment>
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
            <TextField fieldPath="metadata.title" />
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
              fieldPath="metadata.resourceType"
              filterFunction={submissibleResourceTypes}
              optionsListName="resource-types"
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
              fieldPath="metadata.languages"
              optionsListName="languages"
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.DateIssuedField.container"
            fieldPath="metadata.dateIssued"
          >
            <EDTFSingleDatePicker fieldPath="metadata.dateIssued" />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.PublishersField.container"
            fieldPath="metadata.publishers"
          >
            <StringArrayField
              fieldPath="metadata.publishers"
              addButtonLabel={i18next.t("Add publisher")}
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.LicenseField.container"
            fieldPath="metadata.rights"
          >
            <LicenseField fieldPath="metadata.rights" />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.DateModifiedField.container"
            fieldPath="metadata.dateModified"
          >
            {editMode && (
              <EDTFSingleDatePicker fieldPath="metadata.dateModified" />
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
              fieldPath="metadata.subjectCategories"
              vocabulary="subject-categories"
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.AbstractField.container"
            fieldPath="metadata.abstract"
          >
            <MultilingualTextInput fieldPath="metadata.abstract" rich={true} />
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
              addButtonLabel={i18next.t("Add note")}
              fieldPath="metadata.notes"
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
            <RelatedItemsField fieldPath="metadata.relatedItems" />
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
      <div>
        TODO: metadata only - do we need to have an explicit checkbox or are
        missing files enough to express that the record does not have those?
      </div>
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
            <FilesField
              fileMetadataFields={[
                {
                  id: "fileNote",
                  defaultValue: "",
                  isUserInput: true,
                },
              ]}
              recordFiles={recordFiles}
              allowedFileTypes={formConfig.allowed_file_extensions}
            />
          </Overridable>
        </AccordionField>
      </Overridable>
      {process.env.NODE_ENV === "development" && <FormikStateLogger />}
    </React.Fragment>
  );
};

export default FormFieldsContainer;

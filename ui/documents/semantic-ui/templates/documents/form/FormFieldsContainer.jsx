import * as React from "react";
import {
  useFormConfig,
  MultilingualTextInput,
  FormikStateLogger,
  EDTFSingleDatePicker,
  useFieldData,
  useSanitizeInput,
  FilesField,
  StringArrayField,
  FundingField,
  CreatibutorsField,
} from "@js/oarepo_ui/forms";
import { CommunitySelector } from "@js/communities_components/CommunitySelector/CommunitySelector";
import {
  LocalVocabularySelectField,
  VocabularyTreeSelectField,
} from "@js/oarepo_vocabularies";
import { AccordionField, TextField } from "react-invenio-forms";
import {
  AdditionalTitlesField,
  ExternalLocationField,
  SubjectsField,
  SeriesField,
  EventsField,
  IdentifiersField,
  RelatedItemsField,
  objectIdentifiersSchema,
  LicenseField,
} from "@nr/forms";
import Overridable from "react-overridable";
import { i18next } from "@translations/i18next";
import _has from "lodash/has";
import { useFormikContext, getIn } from "formik";

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

  const { values, setFieldValue, setFieldTouched } = useFormikContext();
  const { sanitizeInput } = useSanitizeInput();

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
              autocompleteNames="search"
            />
          </Overridable>
          <Overridable
            id="NrDocs.Deposit.ContributorsField.container"
            fieldPath="metadata.contributors"
          >
            <CreatibutorsField
              fieldPath="metadata.contributors"
              schema="contributors"
              autocompleteNames="search"
              showRoleField={true}
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
              multiple={true}
              vocabulary="subject-categories"
              {...getFieldData({
                fieldPath: "metadata.subjectCategories",
                icon: "tag",
              })}
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
              addButtonLabel={i18next.t("Add note")}
              fieldPath="metadata.notes"
              {...getFieldData({ fieldPath: "metadata.notes" })}
            />
          </Overridable>
        </AccordionField>
      </Overridable>
      <Overridable id="NrDocs.Deposit.AccordionFinancingInformation.container">
        <AccordionField
          includesPaths={["metadata.funders"]}
          label={i18next.t("Financing information")}
        >
          <Overridable
            id="NrDocs.Deposit.FundersField.container"
            fieldPath="metadata.funders"
          >
            <FundingField fieldPath="metadata.funders" />
            {/* <FundersField fieldPath="metadata.fundingReferences" /> */}
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
              {...getFieldData({ fieldPath: "metadata.relatedItems" })}
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

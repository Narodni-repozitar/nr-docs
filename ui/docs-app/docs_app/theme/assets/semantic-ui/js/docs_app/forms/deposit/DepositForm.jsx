import React, { useRef } from "react";
import {
  useFormConfig,
  MultilingualTextInput,
  BaseForm,
  FormFeedback,
  FormikStateLogger,
  EDTFSingleDatePicker,
} from "@js/oarepo_ui";
import { LocalVocabularySelectField } from "@js/oarepo_vocabularies";
import { AccordionField, FieldLabel, TextField } from "react-invenio-forms";
import { Container, Grid, Ref, Sticky, Card } from "semantic-ui-react";
import { NRDocumentValidationSchema } from "./NRDocumentValidationSchema";
import {
  StringArrayField,
  AdditionalTitlesField,
  GeoLocationsField,
  FundersField,
  ExternalLocationField,
  ValidateButton,
  SubjectsField,
  SeriesField,
  EventsField,
  IdentifiersField,
  PreviewButton,
  SaveButton,
  DeleteButtonComponent,
  PublishButtonComponent,
  CreatibutorsField,
  RelatedItemsField,
  objectIdentifiersSchema,
  systemIdentifiersSchema,
  FileUploader,
} from "../components/";
import Overridable from "react-overridable";
import { i18next } from "@translations/docs_app/i18next";
import _has from "lodash/has";

export const DepositForm = () => {
  const { record, formConfig } = useFormConfig();
  const editMode = _has(formConfig, "updateUrl");
  const sidebarRef = useRef(null);
  const formFeedbackRef = useRef(null);

  record.links = record.links || {};
  record.links.files =
    "https://localhost:5000/api/nr-documents/4z30f-2bt23/draft/files";
  record.files = { enabled: true };
  return (
    <Container>
      <BaseForm
        onSubmit={() => {}}
        formik={{
          initialValues: record,
          validationSchema: NRDocumentValidationSchema,
          validateOnChange: false,
          validateOnBlur: false,
          enableReinitialize: true,
        }}
      >
        <Grid>
          <Ref innerRef={formFeedbackRef}>
            <Grid.Column
              id="main-content"
              mobile={16}
              tablet={16}
              computer={11}
            >
              <Sticky context={formFeedbackRef} offset={20}>
                <Overridable id="NrDocs.Deposit.FormFeedback.container">
                  <FormFeedback />
                </Overridable>
              </Sticky>
              <Overridable id="NrDocs.Deposit.AccordionFieldFiles.container">
                <AccordionField
                  includesPaths={["files.enabled"]}
                  active
                  label={i18next.t("Files")}
                >
                  <Overridable id="NrDocs.Deposit.FileUploader.container">
                    <FileUploader record={record} />
                  </Overridable>
                </AccordionField>
              </Overridable>
              <Overridable id="NrDocs.Deposit.AccordionFieldBasicInformation.container">
                <AccordionField
                  includesPaths={[
                    "metadata.title",
                    "metadata.additionalTitles",
                    "metadata.creators",
                    "metadata.contributors",
                    "metadata.relatedItems",
                    "metadata.languages",
                    "metadata.resourceType",
                    "metadata.abstract",
                    "metadata.accessRights",
                    "metadata.rights",
                    "metadata.dateAvailable",
                    "metadata.dateModified",
                    "metadata.publishers",
                  ]}
                  active
                  label={i18next.t("Basic information")}
                >
                  <Overridable
                    id="NrDocs.Deposit.TitleField.container"
                    fieldPath="metadata.title"
                  >
                    <TextField
                      fieldPath="metadata.title"
                      required
                      label={
                        <FieldLabel
                          htmlFor={"metadata.title"}
                          icon="pencil"
                          label={i18next.t("Title")}
                        />
                      }
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.AdditionalTitlesField.container"
                    fieldPath="metadata.additionalTitles"
                  >
                    <AdditionalTitlesField fieldPath="metadata.additionalTitles" />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.CreatorsField.container"
                    fieldPath="metadata.creators"
                  >
                    <CreatibutorsField
                      label={i18next.t("Creators")}
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
                    />
                  </Overridable>
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
                  <Overridable
                    id="NrDocs.Deposit.LanguagesField.container"
                    fieldPath="metadata.languages"
                  >
                    <LocalVocabularySelectField
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
                      placeholder={i18next.t("Choose languages")}
                      clearable
                      optionsListName="languages"
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.ResourceTypeField.container"
                    fieldPath="metadata.resourceType"
                  >
                    <LocalVocabularySelectField
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
                      required
                      helpText={i18next.t("Detailed description")}
                      lngFieldWidth={4}
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.AccessRightsField.container"
                    fieldPath="metadata.accessRights"
                  >
                    <LocalVocabularySelectField
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
                      placeholder={i18next.t("Select access rights")}
                      optionsListName="access-rights"
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.LicenseField.container"
                    fieldPath="metadata.rights"
                  >
                    <LocalVocabularySelectField
                      fieldPath="metadata.rights"
                      multiple={true}
                      label={
                        <FieldLabel
                          htmlFor={"metadata.rights"}
                          icon="drivers license"
                          label={i18next.t("Licenses")}
                        />
                      }
                      placeholder={i18next.t("Choose licenses")}
                      clearable
                      optionsListName="licenses"
                      helpText={i18next.t(
                        "If a Creative Commons license is associated with the resource, select the appropriate license option from the menu. We recommend choosing the latest versions, namely 3.0 Czech and 4.0 International."
                      )}
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.DateAvailableField.container"
                    fieldPath="metadata.dateAvailable"
                  >
                    <EDTFSingleDatePicker
                      fieldPath="metadata.dateAvailable"
                      label={i18next.t("Date available")}
                      helpText={i18next.t(
                        "If the dataset has been published elsewhere, use the date of first publication. You can also specify a future publication date (for embargo). If you do not enter a date, the system will automatically fill the date when the record is published. Format: YYYY-MM-DD, YYYYY-MM or YYYYY."
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
                  <Overridable
                    id="NrDocs.Deposit.PublishersField.container"
                    fieldPath="metadata.publishers"
                  >
                    <StringArrayField
                      fieldPath="metadata.publishers"
                      addButtonLabel={i18next.t("Add publisher")}
                      label={i18next.t("Publishers")}
                    />
                  </Overridable>
                </AccordionField>
              </Overridable>
              <Overridable id="NrDocs.Deposit.AccordionFieldDescription.container">
                <AccordionField
                  includesPaths={[
                    "metadata.technicalInfo",
                    "metadata.methods",
                    "metadata.notes",
                    "metadata.subjects",
                    "metadata.subjectCategories",
                  ]}
                  active
                  label={i18next.t("Resource description")}
                >
                  <Overridable
                    id="NrDocs.Deposit.SubjectCategoriesField.container"
                    fieldPath="metadata.subjectCategories"
                  >
                    <LocalVocabularySelectField
                      fieldPath="metadata.subjectCategories"
                      multiple={true}
                      label={
                        <FieldLabel
                          htmlFor={"metadata.subjectCategories"}
                          icon="tag"
                          label={i18next.t("Subject Categories")}
                        />
                      }
                      placeholder={i18next.t("Choose subject categories")}
                      clearable
                      optionsListName="subject-categories"
                      helpText={i18next.t(
                        "Select the subject field(s) to which the resource belongs."
                      )}
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.MethodsField.container"
                    fieldPath="metadata.methods"
                  >
                    <MultilingualTextInput
                      labelIcon="pencil"
                      label={i18next.t("Methods")}
                      fieldPath="metadata.methods"
                      rich={true}
                      required
                      textFieldLabel={i18next.t("Description")}
                      lngFieldWidth={4}
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.TechnicalInfoField.container"
                    fieldPath="metadata.technicalInfo"
                  >
                    <MultilingualTextInput
                      textFieldLabel={i18next.t("Description")}
                      labelIcon="pencil"
                      label={i18next.t("Technical info")}
                      fieldPath="metadata.technicalInfo"
                      rich={true}
                      required
                      helpText={i18next.t(
                        "Detailed information that may be associated with design, implementation, operation, use, and/or maintenance of a process or system"
                      )}
                      lngFieldWidth={4}
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.NotesField.container"
                    fieldPath="metadata.notes"
                  >
                    <StringArrayField
                      fieldPath="metadata.notes"
                      helpText={i18next.t(
                        "Free-form note for any comment that couldn't be inserted in any other fields."
                      )}
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.SubjectsField.container"
                    fieldPath="metadata.subjects"
                  >
                    <SubjectsField fieldPath="metadata.subjects" />
                  </Overridable>
                </AccordionField>
              </Overridable>
              <Overridable id="NrDocs.Deposit.AccordionAdditionalInformation.container">
                <AccordionField
                  includesPaths={[
                    "metadata.geoLocations",
                    "metadata.accessibility",
                    "metadata.fundingReferences",
                    "metadata.externalLocation",
                    "metadata.series",
                    "metadata.events",
                  ]}
                  active
                  label={i18next.t("Additional information")}
                >
                  <Overridable
                    id="NrDocs.Deposit.GeoLocationsField.container"
                    fieldPath="metadata.geoLocations"
                  >
                    <GeoLocationsField
                      fieldPath="metadata.geoLocations"
                      helpText={i18next.t(
                        "Free description of the location; ie. Atlantic Ocean. Longitude must be a number between -180 and 180 and latitude between -90 and 90."
                      )}
                    />
                  </Overridable>
                  {/* as I understand shoul exist only for items with restricted access as additional explanation why it is restricted? */}
                  {/* still not clear what this field does exactly */}
                  <Overridable
                    id="NrDocs.Deposit.AccessibilityField.container"
                    fieldPath="metadata.accessibility"
                  >
                    {/* TODO: not clear how this input is going to work i.e. our access is within metadata */}
                    <MultilingualTextInput
                      className="accessibility"
                      labelIcon="pencil"
                      label={i18next.t("Accessibility")}
                      textFieldLabel={i18next.t("Description")}
                      fieldPath="metadata.accessibility"
                      helpText={i18next.t(
                        "Explanation regarding restricted status of an item"
                      )}
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.FundersField.container"
                    fieldPath="metadata.fundingReferences"
                  >
                    <FundersField fieldPath="metadata.fundingReferences" />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.ExternalLocationField.container"
                    fieldPath="metadata.externalLocation"
                  >
                    <ExternalLocationField fieldPath="metadata.externalLocation" />
                  </Overridable>

                  <Overridable
                    id="NrDocs.Deposit.SeriesField.container"
                    fieldPath="metadata.series"
                  >
                    <SeriesField fieldPath="metadata.series" />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.EventsField.container"
                    fieldPath="metadata.events"
                  >
                    <EventsField fieldPath="metadata.events" />
                  </Overridable>
                </AccordionField>
              </Overridable>
              <Overridable id="NrDocs.Deposit.AccordionFieldIdentifiersInformation.container">
                <AccordionField
                  includesPaths={[
                    "metadata.objectIdentifiers",
                    "metadata.systemIdentifiers",
                  ]}
                  label={i18next.t("Identifiers information")}
                  // if you don't put active to true, semantic UI throws error if I dont't set
                  // defaultActiveIndex to some number, because in invenio's accordion field
                  // they are setting it to null if active is not true and this throws error
                  // in the console
                  defaultActiveIndex={2}
                >
                  <Overridable
                    id="NrDocs.Deposit.ObjectIdentifiersField.container"
                    fieldPath="metadata.objectIdentifiers"
                  >
                    <IdentifiersField
                      options={objectIdentifiersSchema}
                      fieldPath="metadata.objectIdentifiers"
                      identifierLabel={i18next.t("Object identifier")}
                      label={i18next.t("Object identifiers")}
                      helpText={i18next.t(
                        "Persistent identifier/s of object as ISBN, DOI, etc."
                      )}
                    />
                  </Overridable>
                  <Overridable
                    id="NrDocs.Deposit.SystemIdentifiersField.container"
                    fieldPath="metadata.systemIdentifiers"
                  >
                    <IdentifiersField
                      options={systemIdentifiersSchema}
                      fieldPath="metadata.systemIdentifiers"
                      identifierLabel={i18next.t("System identifier")}
                      label={i18next.t("System identifiers")}
                    />
                  </Overridable>
                </AccordionField>
              </Overridable>
              {process.env.NODE_ENV === "development" && <FormikStateLogger />}
            </Grid.Column>
          </Ref>

          <Ref innerRef={sidebarRef}>
            <Grid.Column
              id="control-panel"
              mobile={16}
              tablet={16}
              computer={5}
            >
              <Sticky context={sidebarRef} offset={20}>
                <Overridable id="NrDocs.Deposit.ControlPanel.container">
                  <Card fluid>
                    {/* <Card.Content>
                      <DepositStatusBox />
                    </Card.Content> */}
                    <Card.Content>
                      <Grid>
                        <Grid.Column
                          computer={8}
                          mobile={16}
                          className="left-btn-col"
                        >
                          <SaveButton fluid />
                        </Grid.Column>

                        <Grid.Column
                          computer={8}
                          mobile={16}
                          className="right-btn-col"
                        >
                          <PreviewButton fluid />
                        </Grid.Column>

                        <Grid.Column width={16} className="pt-10">
                          <PublishButtonComponent />
                        </Grid.Column>
                        <Grid.Column width={16} className="pt-10">
                          <ValidateButton />
                        </Grid.Column>
                        {/* TODO:see if there is a better way to provide URL here, seems that UI links are empty in the form */}
                        <Grid.Column width={16} className="pt-10">
                          <DeleteButtonComponent redirectUrl="/docs/" />
                        </Grid.Column>
                      </Grid>
                    </Card.Content>
                  </Card>
                </Overridable>
              </Sticky>
            </Grid.Column>
          </Ref>
        </Grid>
      </BaseForm>
    </Container>
  );
};

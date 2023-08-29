import React, { useRef } from "react";
import {
  useFormConfig,
  useOnSubmit,
  submitContextType,
  MultilingualTextInput,
  I18nTextInputField,
  BaseForm,
  useSubmitConfig,
} from "@js/oarepo_ui";
import { AccordionField, FieldLabel, TextField } from "react-invenio-forms";
import { Container, Grid, Ref, Sticky, Form, Card } from "semantic-ui-react";
import { NRDocumentValidationSchema } from "./NRDocumentValidationSchema";
import {
  DateField,
  LocalVocabularySelectField,
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
} from "../components/";
import Overridable from "react-overridable";
import { i18next } from "@translations/docs_app/i18next";
import { FormikStateLogger, PublishButton } from "@js/oarepo_vocabularies";
import { useLocation } from "react-router-dom";
import _has from "lodash/has";
import _omitBy from "lodash/omitBy";
import _omit from "lodash/omit";
import _isObject from "lodash/isObject";
import _mapValues from "lodash/mapValues";
import _isArray from "lodash/isArray";

// not sure if these should come from formConfig better to not clutter the code
const objectIdentifiersSchema = [
  { value: "DOI", text: "DOI" },
  { value: "Handle", text: "Handle" },
  { value: "ISBN", text: "ISBN" },
  { value: "ISSN", text: "ISSN" },
  { value: "RIV", text: "RIV" },
];

const systemIdentifiersSchema = [
  { value: "nusl", text: "nusl" },
  { value: "nuslOAI", text: "nuslOAI" },
  { value: "originalRecordOAI", text: "originalRecordOAI" },
  { value: "catalogueSysNo", text: "catalogueSysNo" },
  { value: "nrOAI", text: "nrOAI" },
];

// testing purposes removing __keys from arrayfield items

const removeKeyFromNestedObjects = (inputObject) => {
  const processArray = (arr) => {
    return arr.map((item) => {
      if (_isObject(item)) {
        return _omit(item, "__key");
      }
      return item;
    });
  };

  const processObject = (obj) => {
    return _mapValues(obj, (value) => {
      if (_isArray(value)) {
        return processArray(value);
      }
      return value;
    });
  };

  return processObject(inputObject);
};

// duplicate function from vocabularies just for testing purposes, probably will need a different kind for deposits
// in case this one works out, then we maybe hoist it to oarepoui utils
const removeNullAndUnderscoreProperties = (values, formik) => {
  const newValues = _omitBy(
    values,
    (value, key) =>
      value === null ||
      (Array.isArray(value) && value.every((item) => item === null)) ||
      key.startsWith("_") ||
      key === "revision_id" ||
      key === "links" ||
      key === "updated" ||
      key === "created"
  );
  console.log(newValues);
  newValues.metadata = removeKeyFromNestedObjects(newValues.metadata);
  console.log(newValues);
  return newValues;
};

export const DepositForm = () => {
  const { submitConfig } = useSubmitConfig();
  const { record, formConfig } = useFormConfig();
  const { pathname: currentPath } = useLocation();
  console.log(formConfig, record);
  const context = formConfig.createUrl
    ? submitContextType.create
    : submitContextType.update;

  // need to have edit tag in the code. Context is not reliable enough
  // as it can have other values than
  // update and create when we will support all features?
  // Maybe we shoud consider simply providing editMode or edit boolean as part of formConfig?

  const editMode = _has(formConfig, "updateUrl");

  // const { onSubmit, submitError } = useOnSubmit({
  //   apiUrl: formConfig.createUrl || "/api/nr-documents/" + formConfig.updateUrl,
  //   context: context,
  //   onBeforeSubmit: removeNullAndUnderscoreProperties,
  // onSubmitSuccess: (result) => {
  //   console.log(result);
  //   window.location.href = result.links.self_html;
  // },
  //   onSubmitError: (error, formik) => {
  //     if (
  //       error &&
  //       error.status === 400 &&
  //       error.message === "A validation error occurred."
  //     ) {
  //       error.errors?.forEach((err) =>
  //         formik.setFieldError(err.field, err.messages.join(" "))
  //       );
  //     }
  //   },
  // });
  const { onSubmit, submitError } = useOnSubmit(submitConfig);
  console.log(submitError);
  const sidebarRef = useRef(null);
  // const initialValues = {
  //   metadata: {
  //     additionalTitles: [
  //       {
  //         title: {
  //           lang: "ab",
  //           value: "dwadaw",
  //         },
  //         titleType: "alternativeTitle",
  //       },
  //       {
  //         title: {
  //           lang: "ab",
  //           value: "dwadwad",
  //         },
  //         titleType: "alternativeTitle",
  //       },
  //       { title: { value: "" } },
  //     ],
  //     abstract: [
  //       { lang: "cs", value: "ducciano" },
  //       { lang: "en", value: "Ducciano" },
  //     ],
  //     notes: ["dwadwadwad", "dawdadwad", "dadwada"],
  //     geoLocations: [
  //       {
  //         geoLocationPlace: "Ducica's place",
  //         geoLocationPoint: {
  //           pointLongitude: 130.3232,
  //           pointLatitude: 82.44242,
  //         },
  //       },
  //     ],
  //   },
  // };
  return (
    <Container>
      <BaseForm
        onSubmit={onSubmit}
        formik={{
          initialValues: record,
          validationSchema: NRDocumentValidationSchema,
          validateOnChange: false,
          validateOnBlur: false,
          enableReinitialize: true,
        }}
      >
        <Grid>
          <Grid.Column mobile={16} tablet={16} computer={11}>
            <Overridable id="NrDocs.Deposit.AccordionFieldFiles.container">
              <AccordionField
                includesPaths={["files.enabled"]}
                active
                label={i18next.t("Files")}
              ></AccordionField>
            </Overridable>
            <Overridable id="NrDocs.Deposit.AccordionFieldBasicInformation.container">
              <AccordionField
                includesPaths={[
                  "metadata.resourceType",
                  "metadata.title",
                  "metadata.additionalTitles",
                  "metadata.dateModified",
                  "metadata.publicationDate",
                  "metadata.abstract",
                  "metadata.rights",
                  "metadata.languages",
                  "metadata.accessRights",
                  "metadata.objectIdentifiers",
                  "metadata.systemIdentifiers",
                  "metadata.publishers",
                ]}
                active
                label={i18next.t("Basic information")}
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

                <Overridable
                  id="NrDocs.Deposit.AccessRightsField.container"
                  fieldPath="metadata.accessRights"
                >
                  <LocalVocabularySelectField
                    //TODO: shouldn't access rights be required?
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
                    optionsListName="accessRights"
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
                    optionsListName="resourceTypes"
                  />
                </Overridable>

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
                  id="NrDocs.Deposit.DateAvailableField.container"
                  fieldPath="metadata.dateAvailable"
                >
                  <DateField
                    fieldPath="metadata.dateAvailable"
                    label={i18next.t("Date available")}
                  />
                </Overridable>
                <Overridable
                  id="NrDocs.Deposit.DateModifiedField.container"
                  fieldPath="metadata.dateModified"
                >
                  {editMode && (
                    <DateField
                      fieldPath="metadata.dateModified"
                      label={i18next.t("Date modified")}
                      helpText=""
                    />
                  )}
                </Overridable>
                <Overridable
                  id="NrDocs.Deposit.CreatorsField.container"
                  fieldPath="metadata.creators"
                ></Overridable>
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
                    helpText={i18next.t(
                      "Detailed description of the methodology and technical information should be specified in the 'Dataset Description' section"
                    )}
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
                      "If a Creative Commons license is associated with the dataset, select the appropriate license option from the menu. We recommend choosing the latest versions, namely 3.0 Czech and 4.0 International."
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
                label={i18next.t("Dataset description")}
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
                    optionsListName="subjectCategories"
                    helpText={i18next.t(
                      "Select the subject field(s) to which the dataset belongs."
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
                  <Form.Field>
                    <label>{i18next.t("Resource accessibility")}</label>
                    <I18nTextInputField
                      label={i18next.t("Description")}
                      fieldPath="metadata.accessibility"
                    />
                  </Form.Field>
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

            <FormikStateLogger />
          </Grid.Column>
          <Ref innerRef={sidebarRef}>
            <Grid.Column mobile={16} tablet={16} computer={5}>
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
                          className="pb-0 left-btn-col"
                        >
                          <SaveButton fluid />
                        </Grid.Column>

                        <Grid.Column
                          computer={8}
                          mobile={16}
                          className="pb-0 right-btn-col"
                        >
                          <PreviewButton fluid />
                        </Grid.Column>

                        <Grid.Column width={16} className="pt-10">
                          <PublishButton fluid />
                        </Grid.Column>
                        <Grid.Column width={16} className="pt-10">
                          <ValidateButton fluid />
                        </Grid.Column>
                      </Grid>
                    </Card.Content>
                  </Card>
                </Overridable>
                {/* <Overridable
                    id="NrDocs.Deposit.AccessRightField.container"
                    fieldPath="access"
                  >
                    <AccessRightField
                      label={i18next.t("Visibility")}
                      labelIcon="shield"
                      fieldPath="access"
                      showMetadataAccess={permissions?.can_manage_record_access}
                    />
                  </Overridable> */}
                {/* {permissions?.can_delete_draft && (
                    <Overridable
                      id="InvenioAppRdm.Deposit.CardDeleteButton.container"
                      record={record}
                    >
                      <Card>
                        <Card.Content>
                          <DeleteButton fluid />
                        </Card.Content>
                      </Card>
                    </Overridable>
                  )} */}
              </Sticky>
            </Grid.Column>
          </Ref>
        </Grid>
      </BaseForm>
    </Container>
  );
};

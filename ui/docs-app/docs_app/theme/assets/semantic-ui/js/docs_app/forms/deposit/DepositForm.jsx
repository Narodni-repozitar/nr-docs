import React, { useRef } from "react";
import {
  useFormConfig,
  useOnSubmit,
  submitContextType,
  MultilingualTextInput,
  I18nTextInputField,
} from "@js/oarepo_ui";
import {
  BaseForm,
  AccordionField,
  FieldLabel,
  TextField,
} from "react-invenio-forms";
import { Container, Grid, Ref, Sticky, Form } from "semantic-ui-react";
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
} from "../components/";
import Overridable from "react-overridable";
import { i18next } from "@translations/docs_app/i18next";
import { FormikStateLogger } from "@js/oarepo_vocabularies";

export const DepositForm = () => {
  const { record, formConfig } = useFormConfig();
  const context = formConfig.createUrl
    ? submitContextType.create
    : submitContextType.update;
  const { onSubmit, onSubmitError } = useOnSubmit({
    apiUrl: formConfig.createUrl || formConfig.updateUrl,
    context: context,
    onSubmitSuccess: (result) => {
      window.location.href = editMode
        ? currentPath.replace("/edit", "")
        : currentPath.replace("_new", result.id);
    },
  });
  const sidebarRef = useRef(null);
  const initialValues = {
    ...record,
    metadata: {
      additionalTitles: [
        {
          __key: -1,
          title: {
            lang: "ab",
            value: "dwadaw",
          },
          titleType: "alternative-title",
        },
        {
          __key: -2,
          title: {
            lang: "ab",
            value: "dwadwad",
          },
          titleType: "alternative-title",
        },
      ],
      // abstract: [
      //   { lang: "cs", value: "ducciano" },
      //   { lang: "en", value: "Ducciano" },
      // ],
      notes: ["dwadwadwad", "dawdadwad", "dadwada"],
      geoLocations: [
        {
          geoLocationPlace: "Ducica's place",
          geoLocationPoint: {
            pointLongitude: 130.3232,
            pointLatitude: 82.44242,
          },
        },
      ],
    },
  };
  // fake boolean to simulate if we are editing existing or creating new item
  const editMode = false;
  return (
    <Container>
      <BaseForm
        onSubmit={onSubmit}
        formik={{
          initialValues: {},
          validationSchema: NRDocumentValidationSchema,
          validateOnChange: false,
          validateOnBlur: false,
          enableReinitialize: true,
        }}
      >
        <Grid>
          <Grid.Column mobile={16} tablet={16} computer={12}>
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
                  "metadata.publicationDate",
                  "metadata.abstract",
                  "metadata.rights",
                ]}
                active
                label={i18next.t("Basic information")}
              >
                <Overridable id="NrDocs.Deposit.PIDField.container"></Overridable>

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
                    required
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
                      required
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
                    fieldPath="metadata.abstract"
                    hasRichInput={true}
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
                    required
                    label={
                      <FieldLabel
                        htmlFor={"metadata.rights"}
                        icon="drivers license"
                        label={i18next.t("License")}
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
                    required
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
                    hasRichInput={true}
                    required={false}
                  />
                </Overridable>
                <Overridable
                  id="NrDocs.Deposit.TechnicalInfoField.container"
                  fieldPath="metadata.technicalInfo"
                >
                  <MultilingualTextInput
                    labelIcon="pencil"
                    label={i18next.t("Technical info")}
                    fieldPath="metadata.technicalInfo"
                    hasRichInput={true}
                    required={false}
                  />
                </Overridable>
                <Overridable
                  id="NrDocs.Deposit.NotesField.container"
                  fieldPath="metadata.notes"
                >
                  <StringArrayField fieldPath="metadata.notes" />
                </Overridable>
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
              </AccordionField>
            </Overridable>

            <FormikStateLogger />
          </Grid.Column>
          <Ref innerRef={sidebarRef}>
            <Grid.Column mobile={16} tablet={16} computer={4}>
              <Sticky context={sidebarRef} offset={20}>
                <Overridable id="FormApp.buttons">
                  <React.Fragment>
                    <ValidateButton />
                    {/* <PublishButton />
                    <ResetButton /> */}
                  </React.Fragment>
                </Overridable>
              </Sticky>
            </Grid.Column>
          </Ref>
        </Grid>
      </BaseForm>
    </Container>
  );
};

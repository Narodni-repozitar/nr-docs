import React, { useRef } from "react";
import {
  useFormConfig,
  useOnSubmit,
  submitContextType,
  MultiLingualTextInput,
} from "@js/oarepo_ui";
import {
  BaseForm,
  AccordionField,
  FieldLabel,
  TextField,
} from "react-invenio-forms";
import { Container, Grid, Ref, Sticky } from "semantic-ui-react";
import { NRDocumentValidationSchema } from "./NRDocumentValidationSchema";
import {
  DateField,
  LocalVocabularySelectField,
  NotesField,
  AdditionalTitlesField,
} from "../components/";
import Overridable from "react-overridable";
import { i18next } from "@translations/docs_app/i18next";
import { FormikStateLogger, VocabularySelect } from "@js/oarepo_vocabularies";

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
    additionalTitles: [
      {
        title: {
          cs: "wadawdwadwad",
          ab: "dwadawdadw",
        },
        titleType: "alternative-title",
      },
      {
        title: {
          ab: "dwadadawda",
          am: "dwadawdadwadwa",
        },
        titleType: "subtitle",
      },
    ],
  };
  // fake boolean to simulate if we are editing existing or creating new item
  const editMode = false;
  return (
    <Container>
      <BaseForm
        onSubmit={onSubmit}
        formik={{
          initialValues: initialValues,
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
                  "resourceType",
                  "title",
                  "additionalTitles",
                  "publicationDate",
                  "abstract",
                  "rights",
                ]}
                active
                label={i18next.t("Basic information")}
              >
                <Overridable id="NrDocs.Deposit.PIDField.container"></Overridable>

                <Overridable
                  id="NrDocs.Deposit.ResourceTypeField.container"
                  fieldPath="resourceType"
                >
                  <LocalVocabularySelectField
                    fieldPath="resourceType"
                    required
                    clearable
                    label={
                      <FieldLabel
                        htmlFor={"resourceType"}
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
                  fieldPath="title"
                >
                  <TextField
                    fieldPath="title"
                    required
                    label={
                      <FieldLabel
                        htmlFor={"title"}
                        icon="pencil"
                        label={i18next.t("Title")}
                      />
                    }
                  />
                </Overridable>

                <Overridable
                  id="NrDocs.Deposit.AdditionalTitlesField.container"
                  fieldPath="additionalTitles"
                >
                  <AdditionalTitlesField fieldPath="additionalTitles" />
                </Overridable>

                <Overridable
                  id="NrDocs.Deposit.DateAvailableField.container"
                  fieldPath="dateAvailable"
                >
                  <DateField
                    fieldPath="dateAvailable"
                    required
                    label={i18next.t("Date available")}
                  />
                </Overridable>
                <Overridable
                  id="NrDocs.Deposit.DateModifiedField.container"
                  fieldPath="dateModified"
                >
                  {editMode && (
                    <DateField
                      fieldPath="dateModified"
                      required
                      label={i18next.t("Date modified")}
                      helpText=""
                    />
                  )}
                </Overridable>
                <Overridable
                  id="NrDocs.Deposit.CreatorsField.container"
                  fieldPath="creators"
                ></Overridable>
                <Overridable
                  id="NrDocs.Deposit.AbstractField.container"
                  fieldPath="abstract"
                >
                  <MultiLingualTextInput
                    labelIcon="pencil"
                    label={i18next.t("Abstract")}
                    fieldPath="abstract"
                    hasRichInput={true}
                    required={false}
                  />
                </Overridable>
                <Overridable
                  id="NrDocs.Deposit.LanguagesField.container"
                  fieldPath="languages"
                >
                  <LocalVocabularySelectField
                    fieldPath="languages"
                    multiple={true}
                    required
                    label={
                      <FieldLabel
                        htmlFor={"languages"}
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
                  fieldPath="rights"
                >
                  <LocalVocabularySelectField
                    fieldPath="rights"
                    multiple={true}
                    required
                    label={
                      <FieldLabel
                        htmlFor={"rights"}
                        icon="drivers license"
                        label={i18next.t("Licenses")}
                      />
                    }
                    placeholder={i18next.t("Choose licenses")}
                    clearable
                    optionsListName="licenses"
                  />
                </Overridable>
              </AccordionField>
            </Overridable>
            <Overridable id="NrDocs.Deposit.AccordionFieldDescription.container">
              <AccordionField
                includesPaths={[
                  "technicalInfo",
                  "methods",
                  "notes",
                  "subjects",
                  "subjectCategories",
                ]}
                active
                label={i18next.t("Dataset description")}
              >
                <Overridable
                  id="NrDocs.Deposit.SubjectCategoriesField.container"
                  fieldPath="title"
                >
                  <LocalVocabularySelectField
                    fieldPath="subjectCategories"
                    multiple={true}
                    required
                    label={
                      <FieldLabel
                        htmlFor={"subjectCategories"}
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
                  fieldPath="title"
                >
                  <MultiLingualTextInput
                    labelIcon="pencil"
                    label={i18next.t("Methods")}
                    fieldPath="methods"
                    hasRichInput={true}
                    required={false}
                  />
                </Overridable>
                <Overridable
                  id="NrDocs.Deposit.TechnicalInfoField.container"
                  fieldPath="title"
                >
                  <MultiLingualTextInput
                    labelIcon="pencil"
                    label={i18next.t("Technical info")}
                    fieldPath="technicalInfo"
                    hasRichInput={true}
                    required={false}
                  />
                </Overridable>
                <Overridable
                  id="NrDocs.Deposit.NotesField.container"
                  fieldPath="notes"
                >
                  <NotesField fieldPath="notes" />
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

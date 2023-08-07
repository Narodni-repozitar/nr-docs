import React, { useRef } from "react";
import _isEmpty from "lodash/isEmpty";
import { useFormConfig, useOnSubmit, submitContextType } from "@js/oarepo_ui";
import { BaseForm, AccordionField } from "react-invenio-forms";
import { Container, Grid, Ref, Sticky } from "semantic-ui-react";
import { NRDocumentValidationSchema } from "./NRDocumentValidationSchema";
import {
  ResourceTypeField,
  PublicationDateField,
  MultiLingualRichInputField,
  LanguageSelectField,
  NotesField,
  MultiLingualTextInput,
} from "../components/";
import Overridable from "react-overridable";
import { i18next } from "@translations/docs_app/i18next";
import { options } from "./fakeData";
import { FormikStateLogger } from "@js/oarepo_vocabularies_ui/form/components";

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
                  "metadata.resource_type",
                  "metadata.title",
                  "metadata.additional_titles",
                  "metadata.publication_date",
                  "metadata.creators",
                  "metadata.description",
                  "metadata.additional_descriptions",
                  "metadata.rights",
                ]}
                active
                label={i18next.t("Basic information")}
              >
                <Overridable id="NrDocs.Deposit.PIDField.container"></Overridable>

                <Overridable
                  id="NrDocs.Deposit.ResourceTypeField.container"
                  fieldPath="metadata.resource_type"
                >
                  <ResourceTypeField
                    options={options.resourceTypes}
                    fieldPath="metadata.resourceType"
                    required
                    clearable
                  />
                </Overridable>

                <Overridable
                  id="NrDocs.Deposit.TitlesField.container"
                  fieldPath="metadata.title"
                >
                  <MultiLingualTextInput
                    fieldPath="title"
                    options={options}
                    width={3}
                  />
                </Overridable>

                <Overridable
                  id="NrDocs.Deposit.PublicationDateField.container"
                  fieldPath="metadata.publication_date"
                >
                  <PublicationDateField
                    fieldPath="metadata.publicationDate"
                    required
                    clearable
                  />
                </Overridable>

                <Overridable
                  id="NrDocs.Deposit.CreatorsField.container"
                  fieldPath="metadata.creators"
                ></Overridable>

                <Overridable
                  id="NrDocs.Deposit.DescriptionsField.container"
                  fieldPath="metadata.description"
                >
                  <MultiLingualRichInputField
                    label={i18next.t("Abstract")}
                    options={options}
                    fieldPath="metadata.abstract"
                    editorConfig={{
                      removePlugins: [
                        "Image",
                        "ImageCaption",
                        "ImageStyle",
                        "ImageToolbar",
                        "ImageUpload",
                        "MediaEmbed",
                        "Table",
                        "TableToolbar",
                        "TableProperties",
                        "TableCellProperties",
                      ],
                    }}
                  />
                </Overridable>

                <Overridable
                  id="NrDocs.Deposit.LicenseField.container"
                  fieldPath="metadata.rights"
                ></Overridable>
                <Overridable
                  id="NrDocs.Deposit.LanguageField.container"
                  fieldPath="metadata.language"
                >
                  <LanguageSelectField
                    fieldPath="metadata.language"
                    multiple={true}
                    required
                    label={i18next.t("Language")}
                    placeholder={i18next.t("Choose languages")}
                    clearable
                  />
                </Overridable>
              </AccordionField>
            </Overridable>
            {/* <NotesField
              fieldPath="metadata.notes"
              addButtonLabel={i18next.t("Add note")}
            /> */}

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

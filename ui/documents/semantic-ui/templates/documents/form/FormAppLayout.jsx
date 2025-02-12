import React, { useState } from "react";
import { BaseFormLayout } from "@js/oarepo_ui";
import { NRDocumentValidationSchema } from "@nr/validationschemas";

const accordionData = [
  {
    id: "basic-information",
    name: "Basic information",
    includesPaths: [
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
    ],
  },
  {
    id: "creators",
    name: "Creators",
    includesPaths: ["metadata.creators", "metadata.contributors"],
  },
  {
    id: "document-description",
    name: "Document description",
    includesPaths: [
      "metadata.subjects",
      "metadata.subjectCategories",
      "metadata.abstract",
      "metadata.series",
      "metadata.externalLocation",
      "metadata.notes",
    ],
  },
  {
    id: "financing-information",
    name: "Financing information",
    includesPaths: ["metadata.fundingReferences"],
  },
  {
    id: "related-items",
    name: "Related items",
    includesPaths: ["metadata.relatedItems"],
  },
  {
    id: "events",
    name: "Events",
    includesPaths: ["metadata.events"],
  },
  {
    id: "files-upload",
    name: "Files upload",
    includesPaths: ["files.enabled"],
  },
];

export const FormAppLayout = () => {
  const formikProps = {
    validationSchema: NRDocumentValidationSchema,
  };
  const [activeAccordion, setActiveAccordion] = useState(accordionData[0]);
  const handleAccordionChange = (accordionId) => {
    setActiveAccordion(accordionData.find((item) => item.id === accordionId));
  };
  return (
    <BaseFormLayout
      formikProps={formikProps}
      accordionData={accordionData}
      activeAccordion={activeAccordion}
      handleAccordionChange={handleAccordionChange}
    />
  );
};
export default FormAppLayout;

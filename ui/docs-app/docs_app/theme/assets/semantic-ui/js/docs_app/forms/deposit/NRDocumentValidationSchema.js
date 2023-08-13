import * as Yup from "yup";
import { i18next } from "@translations/docs_app/i18next";
import _uniqBy from "lodash/uniqBy";

// const checkDuplicateLanguage = (array) => {
//   const uniqueArray = _uniqWith(
//     array,
//     (itemA, itemB) => itemA.language === itemB.language
//   );
//   return uniqueArray.length === array.length;
// };

// "__key": -1,
// "title": {
//   "lang": "ab",
//   "value": "adsada"
// },
// "titleType": "alternative-title"

const requiredMessage = i18next.t("This field is required");
export const NRDocumentValidationSchema = Yup.object().shape({
  metadata: Yup.object().shape({
    title: Yup.string()
      .required(requiredMessage)
      .min(10, i18next.t("Must be at least 10 characters")),
    resourceType: Yup.object().required(requiredMessage),
    additionalTitles: Yup.array()
      .of(
        Yup.object().shape({
          title: Yup.object().shape({
            lang: Yup.string().required(requiredMessage),
            value: Yup.string().required(requiredMessage),
          }),
          titleType: Yup.string().required(requiredMessage),
        })
      )
      .test("unique-titles", i18next.t("Titles must be unique"), (value) => {
        console.log(value);
        if (!value || value.length < 2) {
          return true;
        }

        return (
          _uniqBy(value, (item) => item.title.value).length === value.length
        );
      }),
    // dateAvailable: "",
    // dateModified: "",
    // creators: "",
    // abstract: "",
    languages: Yup.array().required(requiredMessage),
    // rights: "",
    // publishers: "",
    // technicalInfo: "",
    // methods: "",
    // notes: "",
    // subjectCategories: "",
    // geoLocations: "",
    // accessibility: "",
    // fundingReferences: "",
    // externalLocation: "",
  }),
});

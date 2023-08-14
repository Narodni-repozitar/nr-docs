import * as Yup from "yup";
import { i18next } from "@translations/docs_app/i18next";
import _uniqBy from "lodash/uniqBy";

const requiredMessage = i18next.t("This field is required");
const stringLengthMessage = ({ length }) =>
  i18next.t("Must have at least x characters", { length: length });

export const NRDocumentValidationSchema = Yup.object().shape({
  metadata: Yup.object().shape({
    title: Yup.string().required(requiredMessage).min(6, stringLengthMessage),
    resourceType: Yup.object().required(requiredMessage),
    additionalTitles: Yup.array()
      .of(
        Yup.object().shape({
          title: Yup.object().shape({
            lang: Yup.string().required(requiredMessage),
            value: Yup.string()
              .required(requiredMessage)
              .min(6, stringLengthMessage),
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
    // creators: "",
    languages: Yup.array().required(requiredMessage),
    // publishers: "",
    // notes: "",
    geoLocations: Yup.array().of(
      Yup.object().shape({
        geoLocationPlace: Yup.string().required(requiredMessage),
        geoLocationPoint: Yup.object().shape({
          pointLongitude: Yup.number()
            .required(requiredMessage)
            .test(
              "range",
              i18next.t("Must be between -180 and 180"),
              (value) => {
                return value >= -180 && value <= 180;
              }
            ),
          pointLatitude: Yup.number()
            .required(requiredMessage)
            .test("range", i18next.t("Must be between -90 and 90"), (value) => {
              return value >= -90 && value <= 90;
            }),
        }),
      })
    ),
    accessibility: Yup.object()
      .shape({
        lang: Yup.string().nullable(),
        value: Yup.string().nullable(),
      })
      .test(
        "has-lang-or-value",
        "Either language or value is required",
        function (value) {
          const { lang, value: fieldValue } = value;

          // Check if either lang or value is filled, but not both
          if ((lang && !fieldValue) || (!lang && fieldValue)) {
            return false;
          }
          return true;
        }
      ),
    // externalLocation: "",
  }),
});
// dateAvailable: "",
// dateModified: "",
// abstract: "",
// technicalInfo: "",
// methods: "",
// rights: "", as you are choosing from options, I don't see how it is possible to choose same item twice
// fundingReferences: "",  as you are choosing from options, I don't see how it is possible to choose same item twice
// subjectCategories: "",as you are choosing from options, I don't see how it is possible to choose same item twice

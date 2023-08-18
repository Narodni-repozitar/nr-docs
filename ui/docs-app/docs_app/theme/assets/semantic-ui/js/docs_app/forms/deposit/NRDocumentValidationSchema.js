import * as Yup from "yup";
import { i18next } from "@translations/docs_app/i18next";
import _uniqBy from "lodash/uniqBy";

const requiredMessage = i18next.t("This field is required");
const stringLengthMessage = ({ min }) =>
  i18next.t("Must have at least x characters", { min: min });

const returnGroupError = () => {
  return { groupError: i18next.t("Items must be unique") };
};

export const NRDocumentValidationSchema = Yup.object().shape({
  metadata: Yup.object().shape({
    // not sure but I assume it would be good idea to ask for a minimum length of title
    title: Yup.string().required(requiredMessage).min(10, stringLengthMessage),
    resourceType: Yup.object().required(requiredMessage),
    additionalTitles: Yup.array()
      .of(
        Yup.object().shape({
          title: Yup.object().shape({
            lang: Yup.string().required(requiredMessage),
            value: Yup.string()
              .required(requiredMessage)
              .min(10, stringLengthMessage),
          }),
          titleType: Yup.string().required(requiredMessage),
        })
      )
      .test("unique-titles", returnGroupError, (value, context) => {
        if (!value || value.length < 2) {
          return true;
        }

        if (
          _uniqBy(value, (item) => item.title.value).length !== value.length
        ) {
          console.log("Items are not unique");
          return false;
        }

        return true;
      }),
    // creators: "",
    // contributors:"",
    languages: Yup.array().required(requiredMessage),
    publishers: Yup.array()
      .of(Yup.string().required(requiredMessage))
      .test("unique-items", returnGroupError, (value, context) => {
        if (!value || value.length < 2) {
          return true;
        }
        return _uniqBy(value, (item) => item).length === value?.length ?? 0;
      }),
    notes: Yup.array()
      .of(Yup.string().required(requiredMessage))
      .test("unique-items", returnGroupError, (value, context) => {
        if (!value || value.length < 2) {
          return true;
        }
        return _uniqBy(value, (item) => item).length === value?.length ?? 0;
      }),
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
    // fundingReferences: "",
    // subjects:"",
    // accessRights:"",
    // relatedItems:"",
    // version:"",
    // accessibility"",
    // series:""
    // events:"",
    objectIdentifiers: Yup.array().of(
      Yup.object().shape({
        identifier: Yup.string().required(requiredMessage),
        scheme: Yup.string().required(requiredMessage),
      })
    ),
    // systemIdentifiers:""
  }),
});

// rights: "", as you are choosing from options, I don't see how it is possible to choose same item twice
// subjectCategories: "",as you are choosing from options, I don't see how it is possible to choose same item twice
// abstract, method and technical info seem to not have any validation at all
// arrayFields -> need __key or some such identifier i.e. need to use serialization/deserialization
// additionalTitles
// creators
// geoLocations
// fundingReferences
// subjects
// relatedItems
// series
// events
// objectIdentifiers
// dateAvailable/modified - maybe use some regexp?

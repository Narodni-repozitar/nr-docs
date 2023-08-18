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
      .test("unique-additional-titles", returnGroupError, (value) => {
        if (!value || value.length < 2) {
          return true;
        }

        return (
          _uniqBy(value, (item) => item.title.value).length === value.length
        );
      }),
    // creators: "",
    // contributors:"",
    languages: Yup.array().required(requiredMessage),
    publishers: Yup.array()
      .of(Yup.string().required(requiredMessage))
      .test("unique-publishers", returnGroupError, (value) => {
        if (!value || value.length < 2) {
          return true;
        }
        return _uniqBy(value, (item) => item).length === (value?.length ?? 0);
      }),
    notes: Yup.array()
      .of(Yup.string().required(requiredMessage))
      .test("unique-notes", returnGroupError, (value) => {
        if (!value || value.length < 2) {
          return true;
        }
        return _uniqBy(value, (item) => item).length === (value?.length ?? 0);
      }),
    geoLocations: Yup.array()
      .of(
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
              .test(
                "range",
                i18next.t("Must be between -90 and 90"),
                (value) => {
                  return value >= -90 && value <= 90;
                }
              ),
          }),
        })
      )
      .test("unique-locations", returnGroupError, (value) => {
        if (!value || value.length < 2) {
          return true;
        }

        return (
          _uniqBy(value, (item) => item.geoLocationPlace).length ===
          value.length
        );
      }),
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

          return (lang && !fieldValue) || (!lang && fieldValue);
        }
      ),
    // externalLocation: "",
    fundingReferences: Yup.array()
      .of(
        Yup.object().shape({
          projectID: Yup.string().required(requiredMessage),
          projectName: Yup.string(),
          fundingProgram: Yup.string(),
          funder: Yup.object(),
        })
      )
      .test("unique-project-codes", returnGroupError, (value) => {
        if (!value || value.length < 2) {
          return true;
        }

        return _uniqBy(value, (item) => item.projectID).length === value.length;
      }),
    // subjects:"",
    // accessRights:"",
    // relatedItems:"",
    // version:"",
    // accessibility"",
    series: Yup.array()
      .of(
        Yup.object().shape({
          seriesTitle: Yup.string().required(requiredMessage),
          seriesVolume: Yup.string(),
        })
      )
      .test("unique-series", returnGroupError, (value) => {
        if (!value || value.length < 2) {
          return true;
        }

        return (
          _uniqBy(value, (item) => item.seriesTitle).length === value.length
        );
      }),
    events: Yup.array().of(
      Yup.object().shape({
        eventNameOriginal: Yup.string().required(requiredMessage),
        eventNameAlternate: Yup.array().of(Yup.string()),
        eventDate: Yup.string().required(requiredMessage),
        eventLocation: Yup.object()
          .shape({
            place: Yup.string().required(requiredMessage),
            country: Yup.object().required(requiredMessage),
          })
          .required(requiredMessage),
      })
    ),
    objectIdentifiers: Yup.array()
      .of(
        Yup.object().shape({
          identifier: Yup.string().required(requiredMessage),
          scheme: Yup.string().required(requiredMessage),
        })
      )
      .test("unique-objectIdentifiers", returnGroupError, (value) => {
        if (!value || value.length < 2) {
          return true;
        }

        return (
          _uniqBy(value, (item) => item.identifier).length !== value.length
        );
      }),
    systemIdentifiers: Yup.array().of(
      Yup.object().shape({
        identifier: Yup.string().required(requiredMessage),
        scheme: Yup.string().required(requiredMessage),
      })
    ),
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

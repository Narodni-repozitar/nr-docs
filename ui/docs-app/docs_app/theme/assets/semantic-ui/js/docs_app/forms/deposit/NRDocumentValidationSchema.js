import * as Yup from "yup";
import { i18next } from "@translations/docs_app/i18next";
import _uniqBy from "lodash/uniqBy";

const requiredMessage = i18next.t("This field is required");

const stringLengthMessage = ({ min }) =>
  i18next.t("Must have at least x characters", { min: min });

const returnGroupError = (value, context) => {
  console.log(value, context);
  return { groupError: i18next.t("Items must be unique") };
};
const edtfRegEx = /^(\d{4})(-(\d{2})(-(\d{2}))?)?(\/\d{4}(-\d{2}(-\d{2})?)?)?$/;

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
    abstract: Yup.array().of(
      Yup.object().shape({
        lang: Yup.string().required(requiredMessage),
        value: Yup.string().required(requiredMessage),
      })
    ),
    methods: Yup.array().of(
      Yup.object().shape({
        lang: Yup.string().required(requiredMessage),
        value: Yup.string().required(requiredMessage),
      })
    ),
    technicalInfo: Yup.array().of(
      Yup.object().shape({
        lang: Yup.string().required(requiredMessage),
        value: Yup.string().required(requiredMessage),
      })
    ),
    dateModified: Yup.string().matches(
      edtfRegEx,
      i18next.t("Invalid date format")
    ),
    dateAvailable: Yup.string().matches(
      edtfRegEx,
      i18next.t("Invalid date format")
    ),
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
    accessibility: Yup.object().shape({
      lang: Yup.string(),
      value: Yup.string(),
    }),
    externalLocation: Yup.object()
      .shape({
        externalLocationURL: Yup.string().url(
          i18next.t("Please provide an URL in valid format")
        ),
        externalLocationNote: Yup.string(),
      })
      .test(
        "must-have-url-if-used",
        () => {
          return {
            groupError: i18next.t(
              "URL must be provided for this field if used"
            ),
          };
        },
        (value) => !(value.externalLocationNote && !value.externalLocationURL)
      ),
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
        eventDate: Yup.string()
          .required(requiredMessage)
          .matches(edtfRegEx, i18next.t("Invalid date format")),
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
          _uniqBy(value, (item) => item.identifier).length === value.length
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

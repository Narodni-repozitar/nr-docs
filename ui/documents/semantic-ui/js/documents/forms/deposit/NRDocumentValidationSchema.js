import * as Yup from "yup";
import { i18next } from "@translations/i18next";
import { requiredMessage, returnGroupError, unique } from "@js/oarepo_ui";

const edtfRegEx = /^(\d{4})(-(\d{2})(-(\d{2}))?)?(\/\d{4}(-\d{2}(-\d{2})?)?)?$/;

export const NRDocumentValidationSchema = Yup.object().shape({
  metadata: Yup.object().shape({
    title: Yup.string().required(requiredMessage).label(i18next.t("Title")),
    resourceType: Yup.object()
      .test(
        "is-non-empty",
        requiredMessage,
        (value) => value && Object.keys(value).length > 0 && value?.id
      )
      .label(i18next.t("Resource type")),
    additionalTitles: Yup.array()
      .of(
        Yup.object().shape({
          title: Yup.object()
            .shape({
              lang: Yup.string()
                .required(requiredMessage)
                .label(i18next.t("Language")),
              value: Yup.string().required(requiredMessage),
            })
            .label(i18next.t("Title")),
          titleType: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Title type")),
        })
      )
      .label(i18next.t("Additional titles")),

    abstract: Yup.array()
      .of(
        Yup.object().shape({
          lang: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Language")),
          value: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Abstract")),
        })
      )
      .label(i18next.t("Abstract")),
    methods: Yup.array()
      .of(
        Yup.object().shape({
          lang: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Language")),
          value: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Methods")),
        })
      )
      .label(i18next.t("Methods")),
    technicalInfo: Yup.array()
      .of(
        Yup.object().shape({
          lang: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Language")),
          value: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Technical info")),
        })
      )
      .label(i18next.t("Technical info")),
    accessRights: Yup.object()
      .test(
        "is-non-empty",
        requiredMessage,
        (value) => value && Object.keys(value).length > 0 && value?.id
      )
      .label(i18next.t("Access rights")),
    dateModified: Yup.string()
      .matches(edtfRegEx, i18next.t("Invalid date format"))
      .label(i18next.t("Date modified")),
    dateAvailable: Yup.string()
      .matches(edtfRegEx, i18next.t("Invalid date format"))
      .label(i18next.t("Date available")),
    creators: Yup.array()
      .required(requiredMessage)
      .label(i18next.t("Creators")),
    languages: Yup.array()
      .min(1, requiredMessage)
      .required(requiredMessage)
      .label(i18next.t("Language")),
    publishers: Yup.array()
      .of(Yup.string().required(requiredMessage))
      .test("unique-publishers", returnGroupError, (value, context) =>
        unique(
          value,
          context,
          undefined,
          i18next.t("Publishers must be unique")
        )
      )
      .label(i18next.t("Publishers")),
    notes: Yup.array()
      .of(Yup.string().required(requiredMessage))
      .test("unique-notes", returnGroupError, (value, context) =>
        unique(value, context, undefined, i18next.t("Notes must be unique"))
      )
      .label(i18next.t("Notes")),
    geoLocations: Yup.array()
      .of(
        Yup.object().shape({
          geoLocationPlace: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Location")),
          geoLocationPoint: Yup.object().shape({
            pointLongitude: Yup.number()
              .required(requiredMessage)
              .test(
                "range",
                i18next.t("Longitude must be between -180 and 180"),
                (value) => {
                  return value >= -180 && value <= 180;
                }
              )
              .label(i18next.t("Longitude")),
            pointLatitude: Yup.number()
              .required(requiredMessage)
              .test(
                "range",
                i18next.t("Latitude must be between -90 and 90"),
                (value) => {
                  return value >= -90 && value <= 90;
                }
              )
              .label(i18next.t("Latitude")),
          }),
        })
      )
      .test("unique-locations", returnGroupError, (value, context) =>
        unique(
          value,
          context,
          "geoLocationPlace",
          i18next.t("Locations must be unique")
        )
      )
      .label(i18next.t("Geolocation")),
    accessibility: Yup.array()
      .of(
        Yup.object().shape({
          lang: Yup.string().label(i18next.t("Language")),
          value: Yup.string().label(i18next.t("Accessibility")),
        })
      )
      .label(i18next.t("Accessibility")),
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
        (value, context) => {
          if (value.externalLocationNote && !value.externalLocationURL) {
            return new Yup.ValidationError(
              i18next.t("URL must be provided for this field if used"),
              value,
              `${context.path}.externalLocationURL`
            );
          }
          return true;
        }
      )
      .label(i18next.t("External location")),
    fundingReferences: Yup.array()
      .of(
        Yup.object().shape({
          projectID: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Project code")),
          projectName: Yup.string(),
          fundingProgram: Yup.string(),
          funder: Yup.object(),
        })
      )
      .test("unique-project-codes", returnGroupError, (value, context) =>
        unique(
          value,
          context,
          "projectID",
          i18next.t("Project codes must be unique")
        )
      )
      .label(i18next.t("Funding")),
    subjects: Yup.array()
      .of(
        Yup.object().shape({
          subjectScheme: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Subject scheme")),
          subject: Yup.array()
            .of(
              Yup.object().shape({
                lang: Yup.string()
                  .required(requiredMessage)
                  .label(i18next.t("Language")),
                value: Yup.string()
                  .required(requiredMessage)
                  .label(i18next.t("Subject")),
              })
            )
            .test("unique-subjects", returnGroupError, (value, context) =>
              unique(
                value,
                context,
                "value",
                i18next.t("Subjects must be unique")
              )
            ),
        })
      )
      .label(i18next.t("Subjects")),
    // relatedItems:"",
    // version:"",
    series: Yup.array()
      .of(
        Yup.object().shape({
          seriesTitle: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Series title")),
          seriesVolume: Yup.string(),
        })
      )
      .test("unique-series", returnGroupError, (value, context) =>
        unique(
          value,
          context,
          "seriesTitle",
          i18next.t("Series titles must be unique")
        )
      )
      .label(i18next.t("Series")),
    events: Yup.array()
      .of(
        Yup.object().shape({
          eventNameOriginal: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Event name")),
          eventNameAlternate: Yup.array().of(Yup.string()),
          eventDate: Yup.string()
            .required(requiredMessage)
            .matches(edtfRegEx, i18next.t("Invalid date format"))
            .label(i18next.t("Event date")),
          eventLocation: Yup.object()
            .shape({
              place: Yup.string()
                .required(requiredMessage)
                .label(i18next.t("Place")),
              country: Yup.object()
                .required(requiredMessage)
                .label(i18next.t("Country")),
            })
            .required(requiredMessage),
        })
      )
      .label(i18next.t("Events")),
    objectIdentifiers: Yup.array()
      .of(
        Yup.object().shape({
          identifier: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Identifier type")),
          scheme: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Object identifier")),
        })
      )
      .test("unique-objectIdentifiers", returnGroupError, (value, context) =>
        unique(
          value,
          context,
          "identifier",
          i18next.t("Object identifiers must be unique")
        )
      )
      .label(i18next.t("Object identifiers")),
    systemIdentifiers: Yup.array()
      .of(
        Yup.object().shape({
          identifier: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("Identifier type")),
          scheme: Yup.string()
            .required(requiredMessage)
            .label(i18next.t("System identifier")),
        })
      )
      .label(i18next.t("System identifier")),
  }),
  // .nullable(),
});

export const options = {
  resourceTypes: [
    {
      props: {
        coarType: "report",
        dataCiteType: "Report",
      },
      hierarchy: {
        parent: "reports",
        ancestors: ["reports"],
        ancestors_or_self: ["annual", "reports"],
        level: 2,
        title: [
          {
            cs: "Výroční zpráva",
            en: "Annual report",
          },
          {
            cs: "Zprávy",
            en: "Reports",
          },
        ],
      },
      relatedURI: {},
      revision_id: 1,
      id: "annual",
      type: "resource-types",
      title: {
        cs: "Výroční zpráva",
        en: "Annual report",
      },
      links: {
        self: "https://0.0.0.0:5000/api/vocabularies/resource-types/annual",
        vocabulary: "https://0.0.0.0:5000/api/vocabularies/resource-types",
        parent: "https://0.0.0.0:5000/api/vocabularies/resource-types/reports",
        children:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-parent=annual",
        descendants:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-ancestor=annual",
      },
      updated: "2023-07-03T13:07:21.061652+00:00",
      created: "2023-07-03T13:07:21.050925+00:00",
    },
    {
      props: {
        coarType: "journal article",
        dataCiteType: "JournalArticle",
      },
      hierarchy: {
        ancestors: [],
        ancestors_or_self: ["article"],
        level: 1,
        title: [
          {
            cs: "Článek",
            en: "Article",
          },
        ],
      },
      relatedURI: {},
      revision_id: 1,
      id: "article",
      type: "resource-types",
      title: {
        cs: "Článek",
        en: "Article",
      },
      links: {
        self: "https://0.0.0.0:5000/api/vocabularies/resource-types/article",
        vocabulary: "https://0.0.0.0:5000/api/vocabularies/resource-types",
        children:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-parent=article",
        descendants:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-ancestor=article",
      },
      updated: "2023-07-03T13:07:20.223484+00:00",
      created: "2023-07-03T13:07:20.219013+00:00",
    },
    {
      props: {
        coarType: "bachelor thesis",
        dataCiteType: "Dissertation",
      },
      hierarchy: {
        parent: "theses",
        ancestors: ["theses"],
        ancestors_or_self: ["bachelor", "theses"],
        level: 2,
        title: [
          {
            cs: "Bakalářská práce",
            en: "Bachelor thesis",
          },
          {
            cs: "Závěrečné práce",
            en: "Theses (etds)",
          },
        ],
      },
      relatedURI: {},
      revision_id: 1,
      id: "bachelor",
      type: "resource-types",
      title: {
        cs: "Bakalářská práce",
        en: "Bachelor thesis",
      },
      links: {
        self: "https://0.0.0.0:5000/api/vocabularies/resource-types/bachelor",
        vocabulary: "https://0.0.0.0:5000/api/vocabularies/resource-types",
        parent: "https://0.0.0.0:5000/api/vocabularies/resource-types/theses",
        children:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-parent=bachelor",
        descendants:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-ancestor=bachelor",
      },
      updated: "2023-07-03T13:07:20.691181+00:00",
      created: "2023-07-03T13:07:20.680933+00:00",
    },
    {
      props: {
        coarType: "book",
        dataCiteType: "Book",
      },
      hierarchy: {
        ancestors: [],
        ancestors_or_self: ["book"],
        level: 1,
        title: [
          {
            cs: "Kniha",
            en: "Book",
          },
        ],
      },
      relatedURI: {},
      revision_id: 1,
      id: "book",
      type: "resource-types",
      nonpreferredLabels: [
        {
          cs: "monografie",
        },
      ],
      title: {
        cs: "Kniha",
        en: "Book",
      },
      links: {
        self: "https://0.0.0.0:5000/api/vocabularies/resource-types/book",
        vocabulary: "https://0.0.0.0:5000/api/vocabularies/resource-types",
        children:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-parent=book",
        descendants:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-ancestor=book",
      },
      updated: "2023-07-03T13:07:20.101752+00:00",
      created: "2023-07-03T13:07:20.097509+00:00",
    },
    {
      props: {
        coarType: "book part",
        dataCiteType: "BookChapter",
      },
      hierarchy: {
        ancestors: [],
        ancestors_or_self: ["book-chapter"],
        level: 1,
        title: [
          {
            cs: "Kapitola v knize",
            en: "Book chapter",
          },
        ],
      },
      relatedURI: {},
      revision_id: 1,
      id: "book-chapter",
      type: "resource-types",
      nonpreferredLabels: [
        {
          cs: "kapitoly v monografiích",
        },
      ],
      title: {
        cs: "Kapitola v knize",
        en: "Book chapter",
      },
      links: {
        self: "https://0.0.0.0:5000/api/vocabularies/resource-types/book-chapter",
        vocabulary: "https://0.0.0.0:5000/api/vocabularies/resource-types",
        children:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-parent=book-chapter",
        descendants:
          "https://0.0.0.0:5000/api/vocabularies/resource-types?h-ancestor=book-chapter",
      },
      updated: "2023-07-03T13:07:20.194203+00:00",
      created: "2023-07-03T13:07:20.189272+00:00",
    },
  ],
};

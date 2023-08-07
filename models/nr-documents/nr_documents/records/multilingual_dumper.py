from oarepo_runtime.i18n.dumper import MultilingualDumper


class MultilingualSearchDumper(MultilingualDumper):
    """NrDocumentsRecord search dumper."""

    """Multilingual search dumper."""

    paths = [
        "/metadata/additionalTitles/title",
        "/metadata/subjects/subject",
        "/metadata/abstract",
        "/metadata/methods",
        "/metadata/technicalInfo",
        "/metadata/accessibility",
        "/metadata/abstract",
        "/metadata/accessibility",
        "/metadata/additionalTitles/title",
        "/metadata/methods",
        "/metadata/subjects/subject",
        "/metadata/technicalInfo",
        "/metadata/abstract",
        "/metadata/accessibility",
        "/metadata/additionalTitles/title",
        "/metadata/methods",
        "/metadata/subjects/subject",
        "/metadata/technicalInfo",
    ]
    SUPPORTED_LANGS = ["cs", "en", "cs", "en", "cs", "en"]

    def dump(self, record, data):
        super().dump(record, data)

    def load(self, record, data):
        super().load(record, data)

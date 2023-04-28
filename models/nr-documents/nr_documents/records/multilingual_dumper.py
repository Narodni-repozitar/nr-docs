from oarepo_runtime.i18n.dumper import MultilingualDumper


class MultilingualSearchDumper(MultilingualDumper):
    """NrDocumentsRecord search dumper."""

    paths = [
        "/metadata/additionalTitles/title",
        "/metadata/subjects/subject",
        "/metadata/abstract",
        "/metadata/methods",
        "/metadata/technicalInfo",
        "/metadata/accessibility",
    ]
    SUPPORTED_LANGS = ["cs", "en"]

    def dump(self, record, data):
        super().dump(record, data)

    def load(self, record, data):
        super().load(record, data)

from oarepo_runtime.i18n.dumper import MultilingualDumper


class MultilingualSearchDumper(MultilingualDumper):
    """Multilingual search dumper."""

    paths = [
        "/metadata/abstract",
        "/metadata/accessibility",
        "/metadata/additionalTitles/title",
        "/metadata/methods",
        "/metadata/subjects/subject",
        "/metadata/technicalInfo",
    ]
    SUPPORTED_LANGS = ["cs", "en"]

    def dump(self, record, data):
        super().dump(record, data)

    def load(self, record, data):
        super().load(record, data)

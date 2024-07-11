from collections import defaultdict

from oarepo_runtime.records.systemfields import PathSelector


def keyword_mapper(subjects):
    subject_list = subjects.get("subject", {})
    if not isinstance(subject_list, list):
        subject_list = [subject_list]
    ret = [y.get("value") for y in subject_list]
    return ret


class KeywordsFieldSelector(PathSelector):
    def select(self, record):
        ret = super().select(record)
        by_language = defaultdict(list)
        for r in ret:
            lang = r.get("lang", "en")
            value = r.get("value")
            if not value:
                continue
            by_language[lang].append(value)
        return [by_language]


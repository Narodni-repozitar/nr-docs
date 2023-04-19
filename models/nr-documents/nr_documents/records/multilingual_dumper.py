import operator
from copy import deepcopy
from functools import reduce

from deepmerge import always_merger
from invenio_records.dumpers import SearchDumperExt


def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


class MultilingualDumper(SearchDumperExt):
    """NrDocumentsRecord search dumper."""

    def dump(self, record, data):
        paths = [
            "/metadata/additionalTitles/title",
            "/metadata/subjects/subject",
            "/metadata/abstract",
            "/metadata/methods",
            "/metadata/technicalInfo",
            "/metadata/accessibility",
        ]
        SUPPORTED_LANGS = ["cs", "en"]

        for path in paths:
            new_elements = {}
            record2 = record
            path_array = path.split("/")
            path_array2 = []

            for x in path_array:
                path_array2.append(x)

            path_array2.pop(0)
            path_array2 = path_array2[:-1]

            for x in path_array2:
                record2 = record2[x]
            path_array.pop(0)
            multilingual_element = getFromDict(record, path_array)

            for rec in multilingual_element:
                if rec["lang"] in SUPPORTED_LANGS:
                    el_name = path_array[-1] + "_" + rec["lang"]
                    always_merger.merge(new_elements, {el_name: rec["value"]})

            always_merger.merge(record2, new_elements)
        data.update(deepcopy(dict(record)))
        return data

    def load(self, record, data):
        paths = [
            "/metadata/additionalTitles/title",
            "/metadata/subjects/subject",
            "/metadata/abstract",
            "/metadata/methods",
            "/metadata/technicalInfo",
            "/metadata/accessibility",
        ]
        SUPPORTED_LANGS = ["cs", "en"]
        for path in paths:
            record2 = record
            path_array = path.split("/")
            path_array2 = []
            for x in path_array:
                path_array2.append(x)

            path_array2.pop(0)
            path_array2 = path_array2[:-1]

            for x in path_array2:
                record2 = record2[x]

            path_array.pop(0)
            multilingual_element = getFromDict(record, path_array)
            for rec in multilingual_element:
                if rec["lang"] in SUPPORTED_LANGS:
                    el_name = path_array[-1] + "_" + rec["lang"]
                    del record2[el_name]
        return data

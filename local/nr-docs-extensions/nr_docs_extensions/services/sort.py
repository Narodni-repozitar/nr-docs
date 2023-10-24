from oarepo_runtime.records.icu import ICUSortField
from oarepo_runtime.relations.lookup import lookup_key


class TitleICUSortField(ICUSortField):

    def get_values(self, data, language):
        ret = []
        for l in lookup_key(data, f"{self.source_field}"):
            if l.value:
                ret.append(l.value)
        return ret
